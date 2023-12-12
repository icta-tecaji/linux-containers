# Introduction to Linux Containers

Sources:
- ✅ [LXD vs Docker](https://ubuntu.com/blog/lxd-vs-docker)
- ✅ [What's a Linux container?](https://www.redhat.com/en/topics/containers/whats-a-linux-container)
- ✅ [What are Linux containers?](https://ubuntu.com/blog/what-are-linux-containers)

--- 

Nowadays, deploying applications inside some sort of a Linux container is a widely adopted practice, primarily due to the evolution of the tooling and the ease of use it presents.


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
- **System containers** (as run by LXD) are similar to virtual or physical machines. They **run a full operating system inside them**, you can run any type of workload, and you manage them exactly as you would a virtual or a physical machine. System containers are usually **long-lasting** and you could host **several applications** within a single system container. That means you can install packages inside them, you can manage services, define backup policies, monitoring, and all other aspects as you usually would with a virtual machine.
- **Application containers** (such as Docker), also known as process containers, are containers that **package and run a single process or a service** per container. They run **stateless types of workloads** that are meant to be ephemeral. This means that these containers are temporary, and you can create, delete and replace containers easily as needed. Usually, you don’t need to care about the lifecycle of those containers.

> A common confusion for potential users of LXD is that LXD is an alternative to Docker or Kubernetes. However, LXD and Docker are not competing container technologies, and they tend to serve completely different purposes.

![LXD vs Docker](./images/system_vs_app_cont.png)
<!-- Source: https://ubuntu.com/blog/lxd-vs-docker -->

Both application and system containers share a kernel with the host operating system and utilize it to create isolated processes.
- Application containers run a single app/process.
- System containers run a full operating system giving them flexibility for the workload types they support.


## Container History
Container technology has existed for a long time in different forms, but it has significantly gained popularity recently in the Linux world with the introduction of native containerization support in the Linux kernel. System containers are technically the oldest type of containers. 
- 1982: Chroot (Unix-like operating systems)
- 1999: **BSD introduced jails**, a way of running a second BSD system on the same kernel as the main system.
- 2001: Linux implementation of the concept through Linux **vServer**. This was a separate project with a big patch set towards Linux kernel aimed at implementing a functionality similar to BSD jails.
- 2004: Solaris (Sun Solaris, Open Solaris) grew Zones which was the same concept but a part of Solaris OS.
- 2005: OpenVZ project started to implement multiple VPSs (virtual private servers) on Linux.
- 2008: LXC (Linux)
- 2013: Docker (Linux, FreeBSD, Windows)


## LXC and linuxcontainers.org

Linux containers, also known as LXC, was the first implementation of system containers that was entirely based on mainline Linux features. This means that you could take a completely clean upstream kernel, or the kernel as distributed by any Linux distribution, and use that to create containers on Linux. LXC itself is a low-level tool that can create both system containers and application containers.
- LXC containers are often considered as something in the middle between a chroot and a full-fledged virtual machine.
- The goal of LXC is to create an environment as close as possible to a standard Linux installation but without the need for a separate kernel.
- LXC containers are essentially a copy of an operating system running on the same kernel as its host, so in this case, you don’t virtualise anything, and there are no overhead processes.

**[linuxcontainers.org](https://linuxcontainers.org/) is the umbrella project** behind Incus, LXC, LXCFS, Distrobuilder and more.

The goal is to offer a **distro and vendor neutral environment** for the development of Linux container technologies. The focus is providing containers and virtual machines that run full Linux systems. While VMs supply a complete environment, system containers offer an environment as close as possible to the one you'd get from a VM, but without the overhead that comes with running a separate kernel and simulating all the hardware.

**When should you use Linux containers?**
- Anytime when you’re running Linux on Linux, you should be considering using containers instead of virtual machines.
- For almost any use case, you could run the exact same workload in a system container and not get any of the overhead that you usually get when using virtual machines.
- The only exception would be if you needed a specific version of the kernel different from the kernel of the host, for a specific feature of that virtual machine.
- System containers are much easier to manage than virtual machines.


## What is LXD?
**LXD is a system container and a virtual machine manager** that runs on top of LXC, enhancing the experience and enabling **easier control** and maintenance. LXD is image-based and provides images for a wide number of different Linux distributions. A simple command-line tool enables you to easily manage your instances, and it is easy to integrate it with third-party orchestration and management tools. LXD can run **clusters**, it provides support for different storage backends and network types and scales easily from one instance on your laptop to a full rack in a data center.

LXC:
- Linux container runtime allowing creation of multiple isolated Linux systems (containers) on a control host using a single Linux kernel
- Only supports containers
- Low-level tool requiring expertise

LXD:
- System container and virtual machine manager built on top of LXC, enabling easier management, control and integration
- Supports container and VMs
- Better user experience through a simple REST API


## Docker vs Linux Containers
- ✅ [Linux Containers vs Docker - What is the Difference](https://www.section.io/engineering-education/lxc-vs-docker-what-is-the-difference-and-why-docker-is-better/)
- ✅ [Unveiling the Differences: LXC vs Docker – An In-Depth Comparison](https://www.redswitches.com/blog/lxc-vs-docker/)
- ✅ [LXD vs Docker](https://ubuntu.com/blog/lxd-vs-docker)
- ✅ [LXC vs Docker: Why Docker is Better in 2023](https://www.upguard.com/blog/docker-vs-lxc)
- ✅ [LXC vs Docker: Which Container Platform Is Right for You?](https://earthly.dev/blog/lxc-vs-docker/)

> Up to version 0.8, Docker was essentially based on LXC.

- **Host-Machine Utilization**:
    - Docker: utilizes application-level virtualization
    - LXC: provides a lightweight OS-level virtualization, making LXC more efficient in resource utilization
- **Simplicity**:
    - Docker shines in simplicity and flexibility in design and usage. Its user-friendly interface and irregular approach through Dockerfiles make it easy for developers to create and manage containers.
    - LXC is a low-level tool that requires expertise in Linux administration and containerization. It is not as user-friendly as Docker.
- **Tooling**:
    - Docker offers a rich set of commands and tools for managing containers, making it highly versatile for various use cases.
    - LXC, while functional, may need more of the user-friendly tooling.
- **Use Cases**:
    - Docker Use Cases: Microservices Architecture, Continuous Integration and Continuous Deployment (CI/CD), DevOps Environments
    - LXC Use Cases: Heavy Resource Utilization Applications, Virtual Desktop Infrastructure (VDI),  System-Level Testing


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


