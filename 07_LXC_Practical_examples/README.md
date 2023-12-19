# LXC Practical examples

## OpenWRT container with public access
```bash
# Run an OpenWRT container
sudo lxc-create -t download -n openwrt -- -d openwrt -r 23.05 -a amd64
sudo lxc-start -n openwrt
sudo lxc-ls -f

sudo lxc-info -n openwrt

# Making a container publicly accessible
sudo iptables -t nat -A PREROUTING -i ens160 -p tcp --dport 80 -j DNAT --to-destination 10.0.3.223:80
sudo iptables -t nat -A PREROUTING -i ens160 -p tcp --dport 443 -j DNAT --to-destination 10.0.3.223:443

# Attach to the container
sudo lxc-attach -n openwrt

# start the web server in the container if it is not already running
ps | grep uhttpd

# if the web server is not running, start it
opkg update
opkg install luci
opkg install curl
/etc/init.d/uhttpd start
ps | grep uhttpd

# set the openwrt firewall to allow access to the web server
vi /etc/config/firewall

# add the following lines to the config file
config rule
	option enabled '1'
	option target 'ACCEPT'
	option src 'wan'
	option proto 'tcp'
	option dest_port '80'
	option name 'AllowWANWeb'

# exit vi and save the file with :wq

exit
```
- Go to http://<IP> to see the OpenWRT web page.
- Login with username: root and password: root

Remove the container
```bash
sudo lxc-stop -n openwrt
sudo lxc-destroy -n openwrt
```
