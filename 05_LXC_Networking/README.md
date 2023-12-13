# LXC Networking

https://ubuntu.com/server/docs/containers-lxc - LXC Networking




Networking
As you may have noticed in the configuration file while you were setting the auto-start settings, LXC has a relatively flexible network configuration.
By default in Ubuntu we allocate one “veth” device per container which is bridged into a “lxcbr0” bridge on the host on which we run a minimal dnsmasq dhcp server.

While that’s usually good enough for most people. You may want something slightly more complex, such as multiple network interfaces in the container or passing through physical network interfaces, … The details of all of those options are listed in lxc.conf(5) so I won’t repeat them here, however here’s a quick example of what can be done.

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