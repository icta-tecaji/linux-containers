# Installing and Running LXC

Sources:
- [What's LXC?](https://linuxcontainers.org/lxc/introduction/)
- [Github LXC](https://github.com/lxc/lxc)
- [Install LXC and LXC UI on Ubuntu 22.04|20.04|18.04|16.04](https://computingforgeeks.com/how-to-install-lxc-lxc-ui-on-ubuntu/?expand_article=1)
- [Introduction to security](https://linuxcontainers.org/lxc/security/)
- [Containers - LXC](https://ubuntu.com/server/docs/containers-lxc)
- [How to Use Linux Containers With LXC and LXD](https://www.freecodecamp.org/news/linux-containers-lxc-lxd/)
- [How to Manage Linux Containers using LXC](https://www.geeksforgeeks.org/how-to-manage-linux-containers-using-lxc/)
- [LXC: Linux container tools](https://developer.ibm.com/tutorials/l-lxc-containers/)


## Introduction
LXC is a userspace interface for the Linux kernel containment features. Through a powerful API and simple tools, it lets Linux users easily create and manage system or application containers.

Current LXC uses the following kernel features to contain processes:
- Kernel namespaces (ipc, uts, mount, pid, network and user)
- Apparmor and SELinux profiles
- Seccomp policies
- Chroots (using pivot_root)
- Kernel capabilities
- CGroups (control groups)

LXC containers are often considered as something in the middle between a [chroot](https://securityqueens.co.uk/im-in-chroot-jail-get-me-out-of-here/) and a full fledged virtual machine. The goal of LXC is to create **an environment as close as possible to a standard Linux installation but without the need for a separate kernel**.

> LXC is free software, most of the code is released under the terms of the GNU LGPLv2.1+ license

LXC is currently made of a few separate components:
- The liblxc library
- Several language bindings for the API (python3, lua, go, ruby, haskell)
- A set of standard tools to control the containers
- Distribution container templates


## Releases
LXC is supported by all modern GNU/Linux distributions, and there should already be an LXC package available from the standard package repositories for your distro.

- [Info about releases](https://linuxcontainers.org/lxc/news/)

LXC 5.0 and 4.0 are long term support releases:
- LXC 5.0 will be supported until June 1st 2027 (current: LXC 5.0.3)
- LXC 4.0 will be supported until June 1st 2025 (current: LXC 4.0.12)


## Installation
[Requirements](https://linuxcontainers.org/lxc/getting-started/#requirements):
- One of glibc, musl libc, uclib or bionic as your C library
- Linux kernel >= 3.8 (for all features to be available)

In most cases, you'll find recent versions of LXC available for your Linux distribution. Either directly in the distribution's package repository or through some backport channel.

> For your first LXC experience, we recommend you use a recent supported release, such as a recent bugfix release of LXC 4.0.

Ubuntu is also one of the few (if not only) Linux distributions to come by default with everything that's needed for safe, unprivileged LXC containers.

On such an Ubuntu system, installing LXC is as simple as:
```bash
sudo apt-get update
sudo apt-get upgrade # (optional but recommended)
sudo apt-get install lxc
```

This will pull in the required and recommended dependencies, as well as set up a network bridge for containers to use.

Your system will then have all the LXC commands available, all its templates as well as the python3 binding should you want to script LXC.

After installing LXC, the following commands will be available in the host system:
```
lxc-attach         lxc-create      lxc-snapshot
lxc-autostart      lxc-destroy     lxc-start
lxc-cgroup         lxc-device      lxc-start-ephemeral
lxc-checkconfig    lxc-execute     lxc-stop
lxc-checkpoint     lxc-freeze      lxc-top
lxc-clone          lxcfs           lxc-unfreeze
lxc-config         lxc-info        lxc-unshare
lxc-console        lxc-ls          lxc-usernsexec
lxc-copy           lxc-monitor     lxc-wait
```

Each of the preceding commands has its own [dedicated manual (man) page](https://linuxcontainers.org/lxc/manpages/), which provides a handy reference for the usage of, available options for, and additional information about the command.

For LXC userspace tools to work properly in the host operating system, you must **ensure that all the kernel features required for LXC support are enabled** in the running host kernel. This can be verified using `lxc-checkconfig`.

> Everything listed in the `lxc-checkconfig` command output should have the status enabled; otherwise, try restarting the system.


## LXC Default Configuration
`/etc/lxc/default.conf` is the default configuration file for LXC installed using the standard Ubuntu packages. This configuration file supplies the default configuration for all containers created on the host system.
- `cat /etc/lxc/default.conf`

The networking will be set up as a virtual Ethernet connection type—that is, veth from the network bridge lxcbr0 for each container that will get created.

The installation will also configure a default container network. The name of the bridge is `lxcbr0`:
- `ip addr | grep lxc`

LXC supports **user namespaces, and this is the recommended way to secure LXC containers.** User namespaces are configured by assigning user ID (UID) and group ID (GID) ranges for existing users, where an existing system user except root will be mapped to these UID/GID ranges for the users within the LXC container.

Based on user namespaces, LXC containers can be classified into two types:
- Privileged containers
- Unprivileged containers


## Privileged LXC containers
**Privileged** - This is when you run lxc commands as root user.
  - The old-style containers, they're not safe at all and should only be used in environments where unprivileged containers aren't available and where you would trust your container's user with root access to the host.
  - As privileged containers are considered unsafe, new container escape exploits won't be worthy of quick fix.

Privileged containers are **defined as any container where the container uid 0 is mapped to the host's uid 0.** In such containers, protection of the host and prevention of escape is entirely done through Mandatory Access Control (apparmor, selinux), seccomp filters, dropping of capabilities and namespaces.

Those technologies combined will typically prevent any accidental damage of the host, where damage is defined as things like reconfiguring host hardware, reconfiguring the host kernel or accessing the host filesystem.

**LXC upstream's position is that those containers aren't and cannot be root-safe.**

> They are still valuable in an environment where you are running trusted workloads or where no untrusted task is running as root in the container.

We are aware of a number of exploits which will let you escape such containers and get full root privileges on the host. 

The only way to restrict that access is by using the methods previously described, such as seccomp, SELinux, and AppArmor. But writing a policy that applies the desired security that is required can be complicated.

Some of those exploits can be trivially blocked and so we do update our different policies once made aware of them. Some others aren't blockable as they would require blocking so many core features that the average container would become completely unusable.

Privileged containers are **started by the host’s root user**; once the container starts, the **container’s root user is mapped to the host’s root user which has UID 0.** This is the default when an LXC container is created in most of the distros, where there is no default security policy applied.

Create, run and attach to a privileged container:
```bash
# Create a container with the given OS template and options.
sudo lxc-create -t download \
  -n my-first-debian -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Start running the container that was just created.
sudo lxc-start -d -n my-first-debian
# List all the containers in the host system.
sudo lxc-ls --fancy
# Obtain detailed container information
sudo lxc-info -n my-first-debian
# Get a default shell session inside the container.
sudo lxc-attach -n my-first-debian
# Run ID and exit
id
ps axfwwu
exit
# Stop the container.
sudo lxc-stop -n my-first-debian
# Permanently delete the container. Removes the container, including its rootfs.
sudo lxc-destroy -n my-first-debian
```


## Building a LXC container
We can create our first container using a template. The lxc-download file, like the rest of the templates in the templates directory, is a script written in bash:
- `ls -la /usr/share/lxc/templates/`
- [Image server for Incus and LXC](https://images.linuxcontainers.org/). In LXC, this image server can be used by selecting the `lxc-download` template. 

List all available images from download template:
- `/usr/share/lxc/templates/lxc-download -l`

Let's start by building a container using the lxc-download template, which will ask for the distribution, release, and architecture, then use the appropriate template to create the filesystem and configuration for us:
- `sudo lxc-create -t download -n my-first-ctr`
- Choose the following options:
  - Distribution: ubuntu
  - Release: jammy
  - Architecture: amd64
- Let's list all containers: `sudo lxc-ls -f`
- Our container is currently not running; let's start it in the background and increase the log level to DEBUG: `sudo lxc-start -n my-first-ctr -d -l DEBUG`
- Let's list all containers: `sudo lxc-ls -f`
- To obtain more information about the container run the following: `sudo lxc-info -n my-first-ctr`
- The new container is now connected to the host bridge `lxcbr0`:
  - `brctl show`
  - `ip a s lxcbr0`
  - `ip a s <container-veth-name>`

Using the download template and not specifying any network settings, the container obtains its IP address from a dnsmasq server that runs on a private network, `10.0.3.0/24` in this case. The host allows the container to connect to the rest of the network and the Internet using NAT rules in iptables:
  - `sudo iptables -L -n -t nat`

Other containers connected to the bridge will have access to each other and to the host, as long as they are all connected to the same bridge and are not tagged with different VLAN IDs.

Let's run attach with the container, list all processes, and network interfaces, and check connectivity:
  - `sudo lxc-attach -n my-first-ctr`
  - `ps axfw`
  - `ip a s`
  - `ping -c 3 google.com`
  - `exit`

> Notice how the hostname changed on the terminal once we attached to the container. This is an example of how LXC uses the UTS namespaces.

Let's examine the directory that was created after building the container: 
- `sudo ls -la /var/lib/lxc/my-first-ctr`
- `sudo ls -la /var/lib/lxc/my-first-ctr/rootfs`

The rootfs directory looks like a regular Linux filesystem. You can manipulate the container directly by making changes to the files there.
- `sudo touch /var/lib/lxc/my-first-ctr/rootfs/test-file`
- `sudo lxc-attach -n my-first-ctr`
- `ls -al`
- `exit`


## Unprivileged LXC containers
Unprivileged containers are more limited, for instance being unable to create device nodes or mount block-backed filesystems. However they are less dangerous to the host, as the root UID in the container is mapped to a non-root UID on the host.

- **Unprivileged** – This is when you run commands as a non-root user.
  - Using unprivileged containers is the **recommended way of creating and running containers for most configurations.**
  - Unprivileged containers are **safe by design**. 
  - The container uid 0 is mapped to an unprivileged user outside of the container and only has extra rights on resources that it owns itself.
  - That means that uid 0 (root) in the container is actually something like uid 100000 outside the container. So should something go very wrong and an attacker manages to escape the container, they'll find themselves with about as many rights as a nobody user.
  - With such container, the use of SELinux, AppArmor, Seccomp and capabilities isn't necessary for security. 

> LXC will still use those to add an extra layer of security which may be handy in the event of a kernel security issue but the security model isn't enforced by them. Most security issues (container escape, resource abuse, ...) in those containers would be a generic kernel security bug rather than a LXC issue.

Unprivileged containers are implemented with the following three methods:
- `lxc-user-net`: A Ubuntu-specific script to create veth pair and bridge the same on the host machine.
- `newuidmap`: Used to set up a UID map
- `newgidmap`: Used to set up a GID map

To make unprivileged containers work, the **host machine’s Linux kernel should support user namespaces.** User namespaces are supported well after Linux kernel version 3.12. Use the following command to check if the user namespace is enabled: `lxc-checkconfig | grep "User namespace"`

Unfortunately the following common operations aren't allowed:
- mounting of most filesystems
- creating device nodes
- any operation against a uid/gid outside of the mapped set

Because of that, most distribution templates simply won't work with those. Instead you should use the **"download" template which will provide you with pre-built images of the distributions that are known to work in such an environment.**

### Creating unprivileged containers as a user
- ✅ [Ubuntu 18.04 and unprivileged LXC](https://www.kubos.cz/2018/07/20/ubuntu-unprivileged-lxc)

[Follow the steps](https://linuxcontainers.org/lxc/getting-started/#creating-unprivileged-containers-as-a-user) to setup the host:
1. Make sure your user has a uid and gid map defined in `/etc/subuid` and `/etc/subgid`.
    - On Ubuntu systems, a default allocation of 65536 uids and gids is given to every new user on the system, so you should already have one. If not, you'll have to use usermod to give yourself one.
2. Next up is `/etc/lxc/lxc-usernet` which is used to set network devices quota for unprivileged users. By default, your user isn't allowed to create any network device on the host, to change that, add:
  - `echo "$(id -un) veth lxcbr0 10" | sudo tee -a /etc/lxc/lxc-usernet` (This means that "your-username" is allowed to create up to 10 veth devices connected to the lxcbr0 bridge.)
3. The last step is to create an LXC configuration file.
```bash
mkdir -p ~/.config/lxc
echo "lxc.include = /etc/lxc/default.conf" >> ~/.config/lxc/default.conf
MS_UID="$(grep "$(id -un)" /etc/subuid  | cut -d : -f 2)"
ME_UID="$(grep "$(id -un)" /etc/subuid  | cut -d : -f 3)"
MS_GID="$(grep "$(id -un)" /etc/subgid  | cut -d : -f 2)"
ME_GID="$(grep "$(id -un)" /etc/subgid  | cut -d : -f 3)"
echo "lxc.idmap = u 0 $MS_UID $ME_UID" >> ~/.config/lxc/default.conf
echo "lxc.idmap = g 0 $MS_GID $ME_GID" >> ~/.config/lxc/default.conf
```
4. Check the configuration file:
  - `cat ~/.config/lxc/default.conf`
5. Add (as host computer root) ACL for AppArmor. It adds execution right (to allow traversal) for user 100000 (proces with PID 0 in container):
  - `sudo apt install acl`
  - `setfacl -m u:100000:x /home/administrator/`
  - `setfacl -m u:100000:x /home/administrator/.local`
  - `setfacl -m u:100000:x /home/administrator/.local/share`
6. And now, create your first container with:
```bash
# Create a container with the given OS template and options.
lxc-create -t download \
  -n my-first-debian -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Start running the container that was just created.
lxc-start -d -n my-first-debian
# List all the containers in the host system.
lxc-ls --fancy
# Get a default shell session inside the container.
lxc-attach -n my-first-debian
# Run ID and exit
id
ps axfwwu
exit
# Stop the container.
lxc-stop -n my-first-debian
# Permanently delete the container.
lxc-destroy -n my-first-debian
```
