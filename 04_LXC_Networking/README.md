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

The host OS, requires the ability to bridge traffic between the containers/VMs and the outside world. Software bridging in Linux has been supported since the kernel version 2.4. To take advantage of this functionality, bridging needs to be enabled in the kernel by setting Networking support | Networking options | 802.1d Ethernet Bridging to yes, or as a kernel module when configuring the kernel.

To verify that bridging is enabled, run the following command: `lsmod | grep bridge`

The built-in Linux bridge is a software layer 2 device. OSI layer 2 devices provide a way of
connecting multiple Ethernet segments together and forward traffic based on MAC
addresses, effectively creating separate broadcast domains.

Let's take a look at the default lxc-net file: `cat /etc/default/lxc-net`

LXC on Ubuntu is packaged in such a way that it also creates the bridge for us: `brctl show`


## Using dnsmasq service to obtain an IP address in the container

The dnsmasq service that was started after installing the lxc package on Ubuntu should look similar to the following: `pgrep -lfaww dnsmasq`

> Note, the dhcp-range parameter matches what was defined in the `/etc/default/lxc-net` file.

Let's create a new container and explore its network settings:
```bash
# Create and start a new container
sudo lxc-create -t download \
  -n br1 -- \
  --dist debian \
  --release bookworm \
  --arch amd64

sudo lxc-start -n br1
sudo lxc-ls -f
sudo lxc-info -n br1
```

Notice the name of the virtual interface that was created on the host OS – veth<ID>, from the output of the lxc-info command. The interface should have been added as a port to the bridge. Let's confirm this using the brctl utility: `brctl show`

Listing all interfaces on the host shows the bridge and the virtual interface associated with the container: `ifconfig`

Notice the IP address assigned to the lxcbr0 interface, it's the same IP address passed as the listen-address argument to the dnsmasq process. Let's examine the network interface and the routes inside the container by attaching to it first:
```bash
sudo lxc-attach -n br1
ifconfig
route -n
```

The IP address assigned to the eth0 interface by dnsmasq is part of the 10.0.3.0/24
subnet and the default gateway is the IP of the bridge interface on the host.

`eth0` is configured to use DHCP. If we would rather use statically assigned addresses, we only have to change that file and specify whatever IP address we would like to use. Using DHCP with dnsmasq is not required for LXC networking, but it can be a convenience.

Let's change the range of IPs that dnsmasq offers, by not assigning the first one hundred IPs
in the `/etc/default/lxc-net` file: 
- `sudo sed -i 's/LXC_DHCP_RANGE="10.0.3.2,10.0.3.254"/LXC_DHCP_RANGE="10.0.3.100,10.0.3.254"/g' /etc/default/lxc-net`
- `grep LXC_DHCP_RANGE /etc/default/lxc-net`
- `sudo systemctl restart lxc-net`
- `pgrep -lfaww dnsmasq`

The next time we build a container using the Ubuntu template, the IP address that will be assigned to the container will start from 100 for the fourth octet. This is handy if we want to use the first 100 IPs for manual assignment.

## Giving a container a persistent IP address

To set a static IP address for an LXC container, you need to modify the container's network configuration.
1. Stop the container if it's currently running: `sudo lxc-stop -n br1`
2. Open the container's configuration file in a text editor: `sudo nano /var/lib/lxc/br1/config`
3. Add the following lines tt the network section of the configuration file:
```bash
lxc.net.0.ipv4.address = 10.0.3.15/24
lxc.net.0.ipv4.gateway = 10.0.3.1
```
4. Save the changes and exit the text editor.
5. Start the container: `sudo lxc-start -n br1`
6. Check the IP address of the container: `sudo lxc-info -n br1`

## Connecting LXC to the host network

The network virtualization acts at layer two. In order to use the network virtualization, parameters must be specified to define the network interfaces of the container. Several virtual interfaces can be assigned and used in a container even if the system has only one physical network interface.

There are three main modes of connecting LXC containers to the host network:
- Using a **physical network interface on the host OS**, which requires one physical interface on the host for each container.
- Using a **virtual interface connected to the host** software bridge using NAT.
- **Sharing the same network namespace as the host**, using the host network device in the container.

Let's examine the network configuration for a container: `sudo cat /var/lib/lxc/br1/config`

All of the configuration options can be changed, before or after the creation of the container.

- **lxc.net.[i].type**

The type of network virtualization to be used.

The container configuration file provides the `lxc.net.[i].type` option. Must be specified before any other option(s) on the net device. Multiple networks can be specified by using an additional index i after all lxc.net.* keys. Currently, the different virtualization types can be:

| Option      | Description |
| ----------- | ----------- |
| `none`     | Will cause the container to share the host's network namespace. This means the host network devices are usable in the container.      |
| `empty`   | LXC will create only the loopback interface.       |
| `veth`   | A virtual ethernet pair device is created with one side assigned to the container and the other side on the host.       |
| `vlan`   | A vlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.       |
| `macvlan`   | A macvlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.      |
| `ipvlan`   | An ipvlan interface is linked with the interface specified by the `lxc.net.[i].link` and assigned to the container.       |
| `phys`   | An already existing interface specified by the `lxc.net.[i].link` is assigned to the container.    |

- **lxc.net.[i].flags**: Specify an action to do for the network (up: activates the interface.).
- **lxc.net.[i].link**: Specify the interface to be used for real network traffic.
- **lxc.net.[i].l2proxy**: Controls whether layer 2 IP neighbour proxy entries will be added to the lxc.net.[i].link interface for the IP addresses of the container.
- **lxc.net.[i].mtu**: Specify the maximum transfer unit for this interface.
- **lxc.net.[i].name**: The interface name is dynamically allocated, but if another name is needed because the configuration files being used by the container use a generic name, eg. eth0, this option will rename the interface in the container.
- **lxc.net.[i].hwaddr**: The interface mac address is dynamically allocated by default to the virtual interface, but in some cases, this is needed to resolve a mac address conflict or to always have the same link-local ipv6 address.
- **lxc.net.[i].ipv4.address**: Specify the ipv4 address to assign to the virtualized interface. Several lines specify several ipv4 addresses. The address is in format x.y.z.t/m, eg. 192.168.1.123/24.
- **lxc.net.[i].ipv4.gateway**: Specify the ipv4 address to use as the gateway inside the container.
- **lxc.net.[i].ipv6.address**: Specify the ipv6 address to assign to the virtualized interface.
- **lxc.net.[i].ipv6.gateway**: Specify the ipv6 address to use as the gateway inside the container.
- **lxc.net.[i].script.up**: Add a configuration option to specify a script to be executed after creating and configuring the network used from the host side.
- **lxc.net.[i].script.down**: Add a configuration option to specify a script to be executed before destroying the network used from the host side.


## Configuring LXC using none network mode

In this mode, the container will share the same network namespace as the host. Change the following lines to the container's configuration file: `sudo nano /var/lib/lxc/br1/config`
```bash
# Network configuration
lxc.net.0.type = none
lxc.net.0.flags = up
```

> **WARNING: If both the container and host have upstart as init, 'halt' in a container (for instance) will shut down the host.**

Stop and start the container for the new network options to take effect, and attach to the
container:
- `sudo lxc-stop -n br1`
- `sudo lxc-start -n br1`
- `sudo lxc-ls -f`
- `sudo lxc-attach -n br1`
- `ifconfig`
- `route -n`
- `ping 8.8.8.8`


Not surprisingly, the network interfaces and routes inside the container are the same as
those on the host OS, since both share the same root network namespace.

> Note that unprivileged containers do not work with this setting due to an inability to mount sysfs. An unsafe workaround would be to bind mount the host's sysfs.

Reset the container's network configuration to the default settings: `sudo nano /var/lib/lxc/br1/config`
```
# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:69:28:4c
```
- `sudo lxc-stop -n br1`
- `sudo lxc-start -n br1`
- `sudo lxc-ls -f`

## Configuring LXC using empty network mode







https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=container%20on%20shutdown.-,NETWORK,-The%20network%20section


## Making a container publicly accessible
If it is desirable for the container to be publicly accessible, there are a few ways to go about it. One is to use iptables to forward host ports to the container, for instance

iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 587 -j DNAT \
    --to-destination 10.0.3.100:587
Then, specify the host’s bridge in the container configuration file in place of lxcbr0, for instance

lxc.network.type = veth
lxc.network.link = br0




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


## Using a different bridge

- Start by showing the bridge on the host: `brctl show`
- Stop the container if it's currently running: `sudo lxc-stop -n br1`
- Create a new bridge: `sudo brctl addbr lxcbr1`
- Show the bridge: `brctl show`
- Add the following lines to the container's configuration file: `sudo nano /var/lib/lxc/br1/config`
```bash
lxc.net.1.type = veth
lxc.net.1.link = lxcbr1
lxc.net.1.flags = up
lxc.net.1.ipv4.address = 10.0.4.13/24
lxc.net.1.ipv4.gateway = 10.0.4.1
lxc.net.1.hwaddr = 00:16:3e:69:28:5c
```
- Save the changes and exit the text editor.
- Assign an IP address to the bridge that the containers can use as their default gateway: `sudo ifconfig lxcbr1 10.0.4.1 netmask 255.255.255.0`
- Start the container: `sudo lxc-start -n br1`
