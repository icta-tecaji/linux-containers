# LXC usage

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

Use the following command to check whether the Linux kernel has the required configuration: `lxc-checkconfig`

The above command will also configure a default container network. The name of the bridge is `lxcbr0`:
- `ip addr | grep lxc`

### Creating unprivileged containers as a user


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