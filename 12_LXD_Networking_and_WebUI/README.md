# LXD Networking, API and WebGUI

- https://documentation.ubuntu.com/lxd/en/latest/explanation/networks/
- https://documentation.ubuntu.com/lxd/en/latest/networks/


## LXD Networking Basics

### Host Port Forwarding

Add port forward rule:
- `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination <container_ip>`

Remove port forward rule:
- `sudo iptables -t nat -L -n --line-numbers`
- `sudo iptables -t nat -D PREROUTING <number>`


### Masquerading Guest IP

> This is done by default if using lxdbr0

Enable IP forwarding and set up NAT using masquerade rule to enable Internet connectivity:

```bash
sudo echo 1 > /proc/sys/net/ipv4/ip_forward # enable ip forwarding
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE # masquerade
```

### Debugging

nc -l xx
tcpdump -i eth0 icmp
wireshark
burpsuite


## LXD WebUI

## API and WebUI

- [How to access the LXD web UI](https://documentation.ubuntu.com/lxd/en/latest/howto/access_ui/)

https://10.0.2.169:8443/ui/project/default/instances

### LXD Server Configuration
By default, LXD is socket activated and configured to listen only on a local UNIX socket. While LXD may not be running when you first look at the process listing, any LXC command will start it up. For instance:

lxc list
This will create your client certificate and contact the LXD server for a list of containers. To make the server accessible over the network you can set the http port using:

lxc config set core.https_address :8443
This will tell LXD to listen to port 8443 on all addresses.

### Authentication

By default, LXD will allow all members of group lxd to talk to it over the UNIX socket. Communication over the network is authorized using server and client certificates.

Before client c1 wishes to use remote r1, r1 must be registered using:

lxc remote add r1 r1.example.com:8443
The fingerprint of r1’s certificate will be shown, to allow the user at c1 to reject a false certificate. The server in turn will verify that c1 may be trusted in one of two ways. The first is to register it in advance from any already-registered client, using:

lxc config trust add r1 certfile.crt
Now when the client adds r1 as a known remote, it will not need to provide a password as it is already trusted by the server.

The other step is to configure a ‘trust password’ with r1, either at initial configuration using lxd init, or after the fact using:

lxc config set core.trust_password PASSWORD
The password can then be provided when the client registers r1 as a known remote.


## LXD API


## Example: OpenWRT with Luci

### Luci Over WAN

### Add a Local Interface