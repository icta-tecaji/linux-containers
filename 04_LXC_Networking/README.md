# LXC Networking

- [LXC Networking](https://ubuntu.com/server/docs/containers-lxc#:~:text=the%20root%20user.-,Networking,-By%20default%20LXC)
- [LXC Manpages: NETWORK](https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=container%20on%20shutdown.-,NETWORK,-The%20network%20section)
- [Network configuration examples](https://github.com/lxc/lxc/tree/main/doc/examples)
- [Setup a network bridge for your LXC containers with lxc-net](https://stanislas.blog/2018/02/setup-network-bridge-lxc-net/)

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


## Making a container publicly accessible

Containers can access to the internet, but cannot be accessed.

We can use the iptables NAT routing table to map a host’s port to a container’s port, with the following command: 
```
sudo iptables -t nat -A PREROUTING -i <host_nic> -p tcp --dport <host_port> -j DNAT --to-destination <ct_ip>:<ct_port> 
```

To be more specific, we’re mapping a port from the host’s public interface to the container’s IP. Obviously, if you want your container to be accessible from the internet, use the interface (host_nic) where you public IPv4 is mounted.

As an exemple, for our container br1:
- `host_nic`: ens160
- `ct_ip`: 10.0.3.15
- `host_port`: 80
- `ct_port`: 80

Install Nginx on the container: 
- `sudo lxc-attach -n br1`
- `apt update && apt install nginx`
- `apt install curl`
- `curl http://localhost:80`
- `exit`

Make the container publicly accessible:
- Try to access the container from the remote host: `curl http://<HOST_IP>
- Add the following rule to the host's iptables: `sudo iptables -t nat -A PREROUTING -i ens160 -p tcp --dport 80 -j DNAT --to-destination 10.0.3.15:80`
- Try to access the container from the remote host: `curl http://<HOST_IP>`. The container is now accessible from the remote host.
- Get the rule ID: `sudo iptables -t nat -L PREROUTING --line-numbers`
- Remove the rule from the host's iptables: `sudo iptables -t nat -D PREROUTING <ID>`


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
```bash
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

The empty mode only creates the loopback interface in the container. The networking configuration file looks similar to the following output:
- `sudo nano /var/lib/lxc/br1/config`
```bash
# Network configuration
lxc.net.0.type = empty
lxc.net.0.flags = up
```
- `sudo lxc-stop --name br1 && sleep 5 && sudo lxc-start --name br1`
- `sudo lxc-ls -f`
- `sudo lxc-attach --name br1`
- `ifconfig`
- `route -n`
- `ping 8.8.8.8`
- `exit`

Only the loopback interface is present and no routes are configured.

Reset the container's network configuration to the default settings: `sudo nano /var/lib/lxc/br1/config`
```bash
# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:69:28:4c
```
- `sudo lxc-stop --name br1 && sleep 5 && sudo lxc-start --name br1 && sleep 5 && sudo lxc-ls -f`


## Configuring LXC using veth mode
The NAT mode is the default network mode when creating containers using the LXC template scripts or the libvirt userspace tools. In this mode, the container can reach the outside world using IP masquerading with iptables rules applied on the host.

In this mode, LXC creates a virtual interface on the host named something like veth366R6F. This is one end of the virtual connection from the container and it should be connected to the software bridge. The other end of the connection is the interface inside the container, by default named eth0.

<!-- ### Using a different bridge

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
- Start the container: `sudo lxc-start -n br1` -->


## Configuring LXC using phys mode

In this mode, we specify a physical interface from the host with the lxc.net.0.link configuration option, which will get assigned to the network namespace of the container and then **make it unavailable for use by the host**.

If we need to have multiple containers using the phys mode, then we'll need that many physical interfaces, which is not always practical.


## Configuring LXC using ipvlan mode

Finally, you can ask LXC to use macvlan for the container’s NIC. Note that this has limitations and depending on configuration may not allow the container to talk to the host itself. Therefore the other two options are preferred and more commonly used.

## Configuring LXC using macvlan mode

The macvlan network mode allows for a single physical interface on the host to be associated with multiple virtual interfaces having different IP and MAC addresses. There
are three modes that macvlan can operate in:
- **Private**: This mode disallows communication between LXC containers
- **Virtual Ethernet Port Aggregator (VEPA)**: This mode disallows communication between LXC containers unless there's a switch that works as a reflective relay
- **Bridge**: This mode creates a simple bridge (not to be confused with the Linux bridge or OVS), which allows containers to talk to each other, but it isolates them
from the host.

