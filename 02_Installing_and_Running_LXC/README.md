# Installing and Running LXC

Sources:
- [What's LXC?](https://linuxcontainers.org/lxc/introduction/)
- [Github LXC](https://github.com/lxc/lxc)
- [Install LXC and LXC UI on Ubuntu 22.04|20.04|18.04|16.04](https://computingforgeeks.com/how-to-install-lxc-lxc-ui-on-ubuntu/?expand_article=1)
- [Introduction to security](https://linuxcontainers.org/lxc/security/)
- [Containers - LXC](https://ubuntu.com/server/docs/containers-lxc)

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
# Get a default shell session inside the container.
sudo lxc-attach -n my-first-debian
# Run ID and exit
id
ps axfwwu
exit
# Stop the container.
sudo lxc-stop -n my-first-debian
# Permanently delete the container.
sudo lxc-destroy -n my-first-debian
```

## Unprivileged LXC containers
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
[Follow the steps](https://linuxcontainers.org/lxc/getting-started/#creating-unprivileged-containers-as-a-user) to setup the host:
1. Make sure your user has a uid and gid map defined in `/etc/subuid` and `/etc/subgid`.
    - On Ubuntu systems, a default allocation of 65536 uids and gids is given to every new user on the system, so you should already have one. If not, you'll have to use usermod to give yourself one.
2. Next up is `/etc/lxc/lxc-usernet` which is used to set network devices quota for unprivileged users. By default, your user isn't allowed to create any network device on the host, to change that, add:
  - `echo "$(id -un) veth lxcbr0 10" | sudo tee -a /etc/lxc/lxc-usernet` (This means that "your-username" is allowed to create up to 10 veth devices connected to the lxcbr0 bridge.)
3. The last step is to create an LXC configuration file.
```bash
mkdir -p ~/.config/lxc
cp /etc/lxc/default.conf ~/.config/lxc/default.conf
MS_UID="$(grep "$(id -un)" /etc/subuid  | cut -d : -f 2)"
ME_UID="$(grep "$(id -un)" /etc/subuid  | cut -d : -f 3)"
MS_GID="$(grep "$(id -un)" /etc/subgid  | cut -d : -f 2)"
ME_GID="$(grep "$(id -un)" /etc/subgid  | cut -d : -f 3)"
echo "lxc.idmap = u 0 $MS_UID $ME_UID" >> ~/.config/lxc/default.conf
echo "lxc.idmap = g 0 $MS_GID $ME_GID" >> ~/.config/lxc/default.conf
```

And now, create your first container with:
```bash
# Create a container with the given OS template and options.
systemd-run --unit=my-unit --user --scope -p "Delegate=yes" -- lxc-create -t download \
  -n my-first-debian -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Start running the container that was just created.
systemd-run --unit=my-unit --user --scope -p "Delegate=yes" -- lxc-start -d -n my-first-debian
# List all the containers in the host system.
lxc-ls --fancy
# Get a default shell session inside the container.
sudo lxc-attach -n my-first-debian
# Run ID and exit
id
ps axfwwu
exit
# Stop the container.
sudo lxc-stop -n my-first-debian
# Permanently delete the container.
lxc-destroy -n my-first-debian
```









## Images
- https://images.linuxcontainers.org/
Templates: 
- ls /usr/share/lxc/templates/
- list all available images from download template:
- /usr/share/lxc/templates/lxc-download -l


https://www.freecodecamp.org/news/linux-containers-lxc-lxd/

https://www.thegeekstuff.com/2016/01/create-lxc-containers/

https://www.thegeekstuff.com/2016/01/install-lxc-linux-containers/

https://www.geeksforgeeks.org/how-to-manage-linux-containers-using-lxc/



## Python API
- https://github.com/lxc/python3-lxc


# Linux Containers

Sources:
- [Unveiling the Differences: LXC vs Docker – An In-Depth Comparison](https://www.redswitches.com/blog/lxc-vs-docker/)

## Attach 
https://www.cyberciti.biz/faq/how-to-update-debian-or-ubuntu-linux-containers-lxc/

## linuxcontainers.org

[linuxcontainers.org](https://linuxcontainers.org/) is the umbrella project behind Incus, LXC, LXCFS, Distrobuilder and more.

The goal is to offer a **distro and vendor neutral environment** for the development of Linux container technologies.

Our focus is providing containers and virtual machines that run full Linux systems. While VMs supply a complete environment, system containers offer an environment as close as possible to the one you'd get from a VM, but without the overhead that comes with running a separate kernel and simulating all the hardware.

- https://ubuntu.com/blog/what-are-linux-containers





https://www.redhat.com/en/topics/containers/whats-a-linux-container
https://ubuntu.com/blog/what-are-linux-containers


https://ubuntu.com/server/docs/containers-lxc
https://developer.ibm.com/tutorials/l-lxc-containers/
- https://computingforgeeks.com/how-to-install-lxc-lxc-ui-on-ubuntu/?expand_article=1 -->

