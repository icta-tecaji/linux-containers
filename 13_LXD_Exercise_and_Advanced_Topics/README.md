# Exercise

## LXD Example: OpenWRT with Luci

Find suitable remote:
- `lxc remote list`

Find openwrt container image:
- `lxc image list images:openwrt`

Launch new instance:
- `lxc launch images:openwrt/23.05 openwrt`

Enter sh:
- `lxc exec openwrt -- /bin/sh`

Install luci:
- `opkg update && opkg install luci nano`

Launch uhttpd:
- `/etc/init.d/uhttpd start`

Configure firewall:
- `nano /etc/config/firewall`
```
config rule
	option enabled '1'
	option target 'ACCEPT'
	option src 'wan'
	option proto 'tcp'
	option dest_port '80'
	option name 'AllowWANWeb'
```
- `/etc/init.d/firewall restart`

Forward ports:
- `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination <container_ip>`


# Resources for Advanced Topics

## Clustering

To spread the total workload over several servers, LXD can be run in clustering mode. In this scenario, any number of LXD servers share the same distributed database that holds the configuration for the cluster members and their instances. The LXD cluster can be managed uniformly using the lxc client or the REST API.

A LXD cluster consists of one bootstrap server and at least two further cluster members. It stores its state in a distributed database, which is a Dqlite database replicated using the Raft algorithm.

While you could create a cluster with only two members, it is strongly recommended that the number of cluster members be at least three. With this setup, the cluster can survive the loss of at least one member and still be able to establish quorum for its distributed state.

When you create the cluster, the Dqlite database runs on only the bootstrap server until a third member joins the cluster. Then both the second and the third server receive a replica of the database.

> If a cluster member is down for more than the configured offline threshold, its status is marked as offline. In this case, no operations are possible on this member, and neither are operations that require a state change across all members.

> Clusters configured with Ceph storage allow for high availability of containers.

LXD cluster members are generally assumed to be identical systems. This means that all LXD servers joining a cluster must have an identical configuration to the bootstrap server, in terms of storage pools and networks.

To accommodate things like slightly different disk ordering or network interface naming, there is an exception for some configuration options related to storage and networks, which are member-specific.

Further resources:

- https://documentation.ubuntu.com/lxd/en/latest/explanation/clustering/
- https://documentation.ubuntu.com/lxd/en/latest/explanation/performance_tuning/
- https://documentation.ubuntu.com/lxd/en/latest/production-setup/


## Security

> IMPORTANT: Local access to LXD through the Unix socket always grants full access to LXD. This includes the ability to attach file system paths or devices to any instance as well as tweak the security features on any instance.

LXC (Linux Containers) is a powerful technology for creating and managing containers, which are lightweight, isolated environments for running applications. However, like any technology that involves isolation and resource sharing, security is a crucial consideration. Here's an overview of LXC's security model and some best practices:

**LXC Security Model:**

- Namespaces: LXC relies heavily on Linux namespaces for isolation. Namespaces ensure that containers have their own isolated view of the system, including processes, network interfaces, mounts, and more.

- Control Groups (cgroups): cgroups are used to limit and isolate resource usage (CPU, memory, I/O, etc.) of containers. This prevents a single container from exhausting the host's resources and affecting other containers.

- Capabilities: Linux capabilities partition the privileges traditionally associated with the superuser (root), allowing for more fine-grained control over what containers can do.

- Mandatory Access Control (MAC): Technologies like SELinux and AppArmor are used to restrict the actions a container can perform, adding an additional layer of security.

- Filesystem Isolation: Filesystem isolation (using chroot and mount namespaces) ensures that containers cannot access each other's files or the host's files unless explicitly allowed.

**Security Concerns and Best Practices:**

- Running Containers as Non-Root: Whenever possible, run containers as non-root users to limit the potential damage if the container is compromised.

- Container Images Security: Use trusted sources for container images and regularly update them to ensure they include the latest security patches.

- Network Isolation and Firewalling: Configure network namespaces and use firewalls (like iptables or nftables) to control network traffic to and from containers.

- Regular Updates and Patching: Regularly update the host system and the container environment to ensure you have the latest security fixes.

- Restricting Capabilities: Limit the Linux capabilities that are available to containers to reduce the risk of privilege escalation attacks.

- Use MAC Policies: Employ Mandatory Access Control systems like SELinux or AppArmor to enforce security policies on containers.

- Resource Limits: Set appropriate resource limits using cgroups to prevent Denial of Service (DoS) attacks from over-consuming system resources.

- Isolate Sensitive Workloads: For highly sensitive workloads, consider stronger isolation solutions like virtual machines or dedicated hosts.

- Security Monitoring and Auditing: Implement security monitoring and auditing tools to detect suspicious activities within containers or on the host system.

- Understanding Shared Kernel Model: Remember that all containers on a host share the same kernel. A vulnerability in the kernel can potentially impact all containers.

- LXC vs. Other Container Technologies: Compared to Docker or Kubernetes, LXC is often seen as providing a lower-level interface to containers, which can offer more control but might require more effort to secure. Docker, for instance, comes with its own set of security enhancements and defaults that are tailored to its way of container management.

**Apparmor**

LXD confines containers by default with an apparmor profile which protects containers from each other and the host from containers. For instance this will prevent root in one container from signaling root in another container, even though they have the same uid mapping. It also prevents writing to dangerous, un-namespaced files such as many sysctls and /proc/sysrq-trigger.

If the apparmor policy for a container needs to be modified for a container c1, specific apparmor policy lines can be added in the raw.apparmor configuration key.

**Seccomp**

All containers are confined by a default seccomp policy. This policy prevents some dangerous actions such as forced umounts, kernel module loading and unloading, kexec, and the open_by_handle_at system call. The seccomp configuration cannot be modified, however a completely different seccomp policy – or none – can be requested using raw.lxc.

Resources:

- https://documentation.ubuntu.com/lxd/en/latest/explanation/projects/
- https://documentation.ubuntu.com/lxd/en/latest/explanation/security/
- https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/container_security_guide/linux_capabilities_and_seccomp
- https://earthly.dev/blog/intro-to-linux-capabilities/


## Running Docker in LXD

While LXD and Docker often get compared, they shouldn’t be seen as competing technologies. As illustrated above, they each have their own purpose and place in the digital world. In fact, even running Docker using LXD is possible and suitable in certain circumstances.

You can use LXD to create your virtual systems running inside the containers, segment them as you like, and easily use Docker to get the actual service running inside of the container.

In order to learn more about Docker in LXD watch the video below:
- https://youtu.be/_fCSSEyiGro


## Device passthrough

Passing through a USB device to LXD is simple:
- `lsusb`
    ```
    Bus 002 Device 003: ID 0451:8041 Texas Instruments, Inc. 
    Bus 002 Device 002: ID 0451:8041 Texas Instruments, Inc. 
    Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
    Bus 001 Device 021: ID 17ef:6047 Lenovo 
    Bus 001 Device 031: ID 046d:082d Logitech, Inc. HD Pro Webcam C920
    Bus 001 Device 004: ID 0451:8043 Texas Instruments, Inc. 
    Bus 001 Device 005: ID 046d:0a01 Logitech, Inc. USB Headset
    Bus 001 Device 033: ID 0fce:51da Sony Ericsson Mobile Communications AB 
    Bus 001 Device 003: ID 0451:8043 Texas Instruments, Inc. 
    Bus 001 Device 002: ID 072f:90cc Advanced Card Systems, Ltd ACR38 SmartCard Reader
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    ```
- `lxc config device add c1 sony usb vendorid=0fce productid=51da`

Passing through a PCI device to an LXC (Linux Containers) container involves several steps, including identifying the PCI device, ensuring the host system is configured to allow PCI passthrough (IOMMU etc.), and configuring the LXC container to use the device.


## Nesting, Limits, and Privileged Containers

Containers all share the same host kernel. This means that there is always an inherent trade-off between features exposed to the container and host security from malicious containers. Containers by default are therefore restricted from features needed to nest child containers. In order to run `lxc` or `lxd` containers under a `lxd` container, the `security.nesting` feature must be set to true:
- `lxc config set container1 security.nesting true`

Once this is done, container1 will be able to start sub-containers.

In order to run unprivileged (the default in LXD) containers nested under an unprivileged container, you will need to ensure a wide enough UID mapping.


## UID Mappings and Privileged Containers

By default, LXD creates unprivileged containers. This means that root in the container is a non-root UID on the host. It is privileged against the resources owned by the container, but unprivileged with respect to the host, making root in a container roughly equivalent to an unprivileged user on the host. (The main exception is the increased attack surface exposed through the system call interface)

Briefly, in an unprivileged container, 65536 UIDs are ‘shifted’ into the container. For instance, UID 0 in the container may be 100000 on the host, UID 1 in the container is 100001, etc, up to 165535. The starting value for UIDs and GIDs, respectively, is determined by the ‘root’ entry the /etc/subuid and /etc/subgid files. (See the subuid(5) man page.)

It is possible to request a container to run without a UID mapping by setting the `security.privileged` flag to true:
- `lxc config set c1 security.privileged true`

Note however that in this case the root user in the container is the root user on the host.

## Booting Containers with Kernel Command Line Parameters

You can explicitly change the init system in a container using the `raw.lxc` configuration parameter. This is equivalent to setting `init=/bin/bash` on the Linux kernel command line.
- `lxc config set <container> raw.lxc 'lxc.init.cmd = /bin/bash'`
- `lxc start <container>`
- `lxc console --show-log <container>`
 