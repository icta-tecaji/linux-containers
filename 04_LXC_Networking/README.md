# LXC Networking

- [LXC Networking](https://ubuntu.com/server/docs/containers-lxc#:~:text=the%20root%20user.-,Networking,-By%20default%20LXC)
- [LXC Manpages: NETWORK](https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=container%20on%20shutdown.-,NETWORK,-The%20network%20section)
- [Network configuration examples](https://github.com/lxc/lxc/tree/main/doc/examples)


## Default networking

By default LXC creates a private network namespace for each container, which includes a layer 2 networking stack.
1. The template script sets up networking by configuring a software bridge `lxcbr0` on the host OS using Network Address Translation (NAT) rules in iptables.
2. Containers created using the default configuration will have one veth NIC with the remote end plugged into the lxcbr0 bridge.
3. The container gets its IP address from a dnsmasq server that LXC starts. 

However, we have full control on what bridge, mode, or routing we would like to use, by means of the container's configuration file.


## Connecting LXC to the host network

The network virtualization acts at layer two. In order to use the network virtualization, parameters must be specified to define the network interfaces of the container. Several virtual interfaces can be assigned and used in a container even if the system has only one physical network interface.

There are three main modes of connecting LXC containers to the host network:
- Using a **physical network interface on the host OS**, which requires one physical interface on the host for each container.
- Using a **virtual interface connected to the host** software bridge using NAT.
- **Sharing the same network namespace as the host**, using the host network device in the container.

The container configuration file provides the `lxc.net.[i].type` option. Must be specified before any other option(s) on the net device. Multiple networks can be specified by using an additional index i after all lxc.net.* keys. Currently, the different virtualization types can be:

| Option      | Description |
| ----------- | ----------- |
| `none`     | Will cause the container to share the host's network namespace. This means the host network devices are usable in the container.      |
| `empty`   | LXC will create only the loopback interface.       |
| `veth`   | A virtual ethernet pair device is created with one side assigned to the container and the other side on the host.       |
| `vlan`   | A vlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.       |
| `macvlan`   | A macvlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.      |
| `ipvlan`   | An ipvlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.       |
| `phys`   | An already existing interface specified by the `lxc.net.[i].link` is assigned to the container.      |


### Configuring LXC using none network mode

> **WARNING: If both the container and host have upstart as init, 'halt' in a container (for instance) will shut down the host.**


Note that unprivileged containers do not work with this setting due to an inability to mount sysfs. An unsafe workaround would be to bind mount the host's sysfs.

### Configuring LXC using empty network mode


## Giving a container a persistent IP address
To give containers on lxcbr0 a persistent ip address based on domain name, you can write entries to /etc/lxc/dnsmasq.conf like:

dhcp-host=lxcmail,10.0.3.100
dhcp-host=ttrss,10.0.3.101


https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=container%20on%20shutdown.-,NETWORK,-The%20network%20section


## Making a container publicly accessible
If it is desirable for the container to be publicly accessible, there are a few ways to go about it. One is to use iptables to forward host ports to the container, for instance

iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 587 -j DNAT \
    --to-destination 10.0.3.100:587
Then, specify the host’s bridge in the container configuration file in place of lxcbr0, for instance

lxc.network.type = veth
lxc.network.link = br0


## Using a different bridge


## macvlan and ipvlan
Finally, you can ask LXC to use macvlan for the container’s NIC. Note that this has limitations and depending on configuration may not allow the container to talk to the host itself. Therefore the other two options are preferred and more commonly used.

## Passing a physical network interface to a container

Containers usually connect to the outside world by either having a physical NIC or a veth tunnel endpoint passed into the container. 
A NIC can only exist in one namespace at a time, so a physical NIC passed into the container is not usable on the host.


## Multiple network interfaces in a container

lxc.network.type = veth
lxc.network.hwaddr = 00:16:3e:3a:f1:c1
lxc.network.flags = up
lxc.network.link = lxcbr0
lxc.network.name = eth0

lxc.network.type = veth
lxc.network.link = virbr0
lxc.network.name = virt0

lxc.network.type = phys
lxc.network.link = eth2
lxc.network.name = eth1
With this setup my container will have 3 interfaces, eth0 will be the usual veth device in the lxcbr0 bridge, eth1 will be the host’s eth2 moved inside the container (it’ll disappear from the host while the container is running) and virt0 will be another veth device in the virbr0 bridge on the host.

Those last two interfaces don’t have a mac address or network flags set, so they’ll get a random mac address at boot time (non-persistent) and it’ll be up to the container to bring the link up.



## Raw network access
In the previous post I mentioned passing raw devices from the host inside the container. One such container I use relatively often is when working with a remote network over a VPN. That network uses OpenVPN and a raw ethernet tap device.

I needed to have a completely isolated system access that VPN so I wouldn’t get mixed routes and it’d appear just like any other machine to the machines on the remote site.

All I had to do to make this work was set my container’s network configuration to:

lxc.network.type = phys
lxc.network.hwaddr = 00:16:3e:c6:0e:04
lxc.network.flags = up
lxc.network.link = tap0
lxc.network.name = eth0
Then all I have to do is start OpenVPN on my host which will connect and setup tap0, then start the container which will steal that interface and use it as its own eth0.The container will then use DHCP to grab an IP and will behave just like if it was a physical machine connect directly in the remote network.