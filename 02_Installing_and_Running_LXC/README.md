# Installing and Running LXC

Sources:
- [What's LXC?](https://linuxcontainers.org/lxc/introduction/)
- [Github LXC](https://github.com/lxc/lxc)
- [Install LXC and LXC UI on Ubuntu 22.04|20.04|18.04|16.04](https://computingforgeeks.com/how-to-install-lxc-lxc-ui-on-ubuntu/?expand_article=1)


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
sudo apt-get upgrade (optional)
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

LXC containers can be of two kinds:
- Privileged containers
- Unprivileged containers

## Privileged LXC containers
- https://linuxcontainers.org/lxc/security/
- https://linuxcontainers.org/lxc/getting-started/#creating-unprivileged-containers-as-a-user
- https://computingforgeeks.com/how-to-install-lxc-lxc-ui-on-ubuntu/?expand_article=1
- SK - 143
- KI - 316
## Unprivileged LXC containers

## Creating unprivileged containers as a user
[You can use LXC in two modes](https://linuxcontainers.org/lxc/security/):
- **Privileged** – This is when you run lxc commands as root user.
  - The old-style containers, they're not safe at all and should only be used in environments where unprivileged containers aren't available and where you would trust your container's user with root access to the host.
  - As privileged containers are considered unsafe, new container escape exploits won't be worthy of quick fix.
- **Unprivileged** – This is when you run commands as a non-root user.

**Unprivileged containers are the safest containers**. Those use a map of uid and gid to allocate a range of uids and gids to a container. That means that uid 0 (root) in the container is actually something like uid 100000 outside the container. So should something go very wrong and an attacker manages to escape the container, they'll find themselves with about as many rights as a nobody user.

Unfortunately this also means that the following common operations aren't allowed:
- mounting of most file systems
- creating device nodes
- any operation against a uid/gid outside of the mapped set

Because of that, most distribution templates simply won't work with those. Instead you should use the **"download" template which will provide you with pre-built images of the distributions that are known to work in such an environment.**






lxc-create -t lxc-download \
  -n my-first-debian -- \
  --dist debian \
  --release bookworm \
  --arch amd64



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


## linuxcontainers.org

[linuxcontainers.org](https://linuxcontainers.org/) is the umbrella project behind Incus, LXC, LXCFS, Distrobuilder and more.

The goal is to offer a **distro and vendor neutral environment** for the development of Linux container technologies.

Our focus is providing containers and virtual machines that run full Linux systems. While VMs supply a complete environment, system containers offer an environment as close as possible to the one you'd get from a VM, but without the overhead that comes with running a separate kernel and simulating all the hardware.

- https://ubuntu.com/blog/what-are-linux-containers





https://www.redhat.com/en/topics/containers/whats-a-linux-container
https://ubuntu.com/blog/what-are-linux-containers


https://ubuntu.com/server/docs/containers-lxc
https://developer.ibm.com/tutorials/l-lxc-containers/