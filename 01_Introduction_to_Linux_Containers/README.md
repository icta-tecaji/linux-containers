# Introduction to Linux Containers

Sources:
- ✅ [LXD vs Docker](https://ubuntu.com/blog/lxd-vs-docker)

Nowadays, deploying applications inside some sort of a Linux container is a widely adopted practice, primarily due to the evolution of the tooling and the ease of use it presents.

## Introduction to Linux Containers
Containerization is the next logical step in virtualization, and there is a huge buzz around this technology. Containers can **provide virtualization at both the operating system level and the application level.**

Some of the possibilities with containers are as follows:
- Provide a complete operating system environment that is sandboxed (isolated)
- Allow packaging and isolation of applications with their entire runtime environment
- Provide a portable and lightweight environment
- Help to maximize resource utilization in data centers
- Aid different development, test, and production deployment workflows

## Container Definition
A **container can be defined as a single operating system image, bundling a set of isolated applications and their dependent resources so that they run separated from the host machine.** There may be multiple such containers running within the same host machine.

Containers can be classified into two types:
- **Operating system level**: An entire operating system runs in an isolated space within the host machine, sharing the same kernel as the host machine.
- **Application level**: An application or service, and the minimal processes required by that application, runs in an isolated space within the host machine.

## What types of containers are there?
- **System containers** (as run by LXD) are similar to virtual or physical machines. They **run a full operating system inside them**, you can run any type of workload, and you manage them exactly as you would a virtual or a physical machine. System containers are usually **long-lasting** and you could host **several applications** within a single system container.
- **Application containers** (such as Docker), also known as process containers, are containers that **package and run a single process or a service** per container. They run **stateless types of workloads** that are meant to be ephemeral. This means that these containers are temporary, and you can create, delete and replace containers easily as needed.

> A common confusion for potential users of LXD is that LXD is an alternative to Docker or Kubernetes. However, LXD and Docker are not competing container technologies, and they tend to serve completely different purposes.

![LXD vs Docker](./images/system_vs_app_cont.png)
<!-- Source: https://ubuntu.com/blog/lxd-vs-docker -->

Both application and system containers share a kernel with the host operating system and utilize it to create isolated processes.
- Application containers run a single app/process.
- System containers run a full operating system giving them flexibility for the workload types they support.

## Containerization vs traditional virtualization
Virtualization was developed as an effort to **fully utilize available computing resources**. Virtualization enables multiple virtual machines to run on a single host for different purposes with their own isolated space. 

Virtualization achieved such isolated operating system environments using hypervisors, computer software that sits in between the host operating system and the guest or the virtual machine’s operating system.

Containerization differs from traditional virtualization technologies and offers many advantages over traditional virtualization:
- Containers are **lightweight** compared to traditional virtual machines.
- Unlike containers, virtual machines require emulation layers (either software or hardware), which consume more resources and add additional overhead.
- Containers share resources with the underlying host machine, with user space and process isolations.
- Due to the lightweight nature of containers, more containers can be run per host than virtual machines per host.
- Starting a container happens nearly instantly compared to the slower boot process of virtual machines.
- Containers are portable and can reliably regenerate a system environment with required software packages, irrespective of the underlying host operating system.

## Container History
Container technology has existed for a long time in different forms, but it has significantly gained popularity recently in the Linux world with the introduction of native containerization support in the Linux kernel.
- 1982: Chroot (Unix-like operating systems)
- 2000: Jail (FreeBSD)
- 2000: Virtuozzo containers (Linux, Windows (Parallels Inc. version))
- 2001: Linux VServer (Linux, Windows)
- 2004: Solaris containers (zones) (Sun Solaris, Open Solaris)
- 2005: OpenVZ Linux (open source version of Virtuozzo)
- 2008: LXC (Linux)
- 2013: Docker (Linux, FreeBSD, Windows)

## Features to Enable Containers
Containers rely on the following features in the Linux kernel to get a contained or isolated area within the host machine. This area is closely related to a virtual machine, but without the need for a hypervisor.
- Control groups (cgroups)
- Namespaces
- Filesystem or rootfs

### Control Groups (cgroups)
- Google presented a new generic method to solve the resource control problem with the cgroups project in 2007.
- Control groups allow resources to be controlled and accounted for based on process groups. 
- The mainline Linux kernel first included a cgroups implementation in 2008, and this paved the way for LXC.
- Cgroups provide a mechanism to aggregate sets of tasks or processes and their future children into hierarchical groups. These groups may be configured to have specialized behavior as desired.

Cgroups are listed within the pseudo filesystem subsystem in the directory `/sys/fs/cgroup`, which gives an overview of all the cgroup subsystems available or mounted in
the currently running system:
- `ls -alh /sys/fs/cgroup`

Let’s take a look at an example of the memory subsystem hierarchy of cgroups. It is available in the following location:
- `cd /sys/fs/cgroup/memory`
- `ls`

Each of the files listed contains information on the control group for which it has been created. For example, the maximum memory usage in bytes is given by the following command (since this is the top-level hierarchy, it lists the default setting for the current host system):
- `cat memory.max_usage_in_bytes` (that is available for use by the currently running system)

The preceding value is in bytes. You can create your own cgroups within `/sys/fs/cgroup` and control each of the subsystems.

### Namespaces
- At the Ottawa Linux Symposium held in 2006, Eric W. Bierderman presented his paper “Multiple Instances of the Global Linux Namespaces”
- This paper proposed the addition of ten namespaces to the Linux kernel. His inspiration for these additional namespaces was the existing filesystem namespace for mounts, which was introduced in 2002. 

**A namespace provides an abstraction to a global system resource that will appear to the processes within the defined namespace as its own isolated instance of a specific global resource.**

Namespaces are used to implement containers; they provide the required isolation between a container and the host system.

Over time, different namespaces have been implemented in the Linux kernel:
- Cgroup: `CLONE_NEWCGROUP` - Cgroup root directory
- IPC: `CLONE_NEWIPC` - System V IPC, POSIX message queues
- Network: `CLONE_NEWNET` - Network devices, stacks, ports, etc.
- Mount: `CLONE_NEWNS`- Mount points
- PID: `CLONE_NEWPID`- Process IDs
- User: `CLONE_NEWUSER` - User and group IDs
- UTS: `CLONE_NEWUTS` - Hostname and NIS domain name

### Filesystem or rootfs

The next component needed for a container is the **disk image, which provides the root filesystem (rootfs) for the container**. 

The rootfs consists of a set of files, similar in structure to the filesystem mounted at root on any GNU/Linux-based machine. 

The size of rootfs is smaller than a typical OS disk image, since it does not contain the kernel. **The container shares the same kernel as the host machine.**

A rootfs can further be reduced in size by making it contain just the application and configuring it to share the rootfs of the host machine. Using copy-on-write (COW) techniques, a single reduced read-only disk image may be shared between multiple containers.



## TODO
https://www.redhat.com/en/topics/containers?sc_cid=70160000000x4xDAAQ


Benefits:
-offering speed, flexibility, and isolation from the underlying system



## Docker vs Linux Containers
- https://earthly.dev/blog/lxc-vs-docker/
- https://www.upguard.com/blog/docker-vs-lxc
- https://ubuntu.com/blog/lxd-vs-docker
- https://www.redswitches.com/blog/lxc-vs-docker/
- https://www.section.io/engineering-education/lxc-vs-docker-what-is-the-difference-and-why-docker-is-better/

LXD utilises LXC for running system containers. LXC is the technology allowing the segmentation of your system into independent containers, whereas LXD is a daemon running on top of it allowing you to manage and operate these instances in an easy and unified way. When it comes to storage, networking, and logging, LXD supports a variety of interfaces and features that the user can control and interact with. LXD is image-based and you can utilise it to run any kind of workload, including traditional systems you would otherwise run in physical or virtual machines. Overall, functionality-wise, LXD is similar to VMWare or KVM hypervisors, but is much lighter on resources and removes the usual virtualization overhead.

Docker is a containerisation platform, it can be installed on a machine (workstation or a server) and provides a variety of tools for developing and operating containers. One of those tools is containerd – a daemon-based runtime that manages the complete lifecycle of Docker containers, including overall running and monitoring of containers. Docker abstracts away storage, networking, and logging, making it easy for developers that don’t have much prior Linux knowledge. Docker was specifically designed for microservice architecture, providing a way to decompose and isolate individual processes, which can then be scaled independently from the rest of the application or system they are a part of. 

> Up to version 0.8, Docker was essentially based on LXC.