- https://documentation.ubuntu.com/lxd/en/latest/explanation/performance_tuning/
- https://documentation.ubuntu.com/lxd/en/latest/production-setup/

https://ubuntu.com/server/docs/containers-lxd


## Security

- https://documentation.ubuntu.com/lxd/en/latest/explanation/projects/
- https://documentation.ubuntu.com/lxd/en/latest/explanation/security/


Consider the following aspects to ensure that your LXD installation is secure:

Keep your operating system up-to-date and install all available security patches.
Use only supported LXD versions (LTS releases or monthly feature releases).
Restrict access to the LXD daemon and the remote API.
Do not use privileged containers unless required. If you use privileged containers, put appropriate security measures in place. See the LXD security page for more information.
Configure your network interfaces to be secure.
See Security for detailed information.

IMPORTANT:

Local access to LXD through the Unix socket always grants full access to LXD. This includes the ability to attach file system paths or devices to any instance as well as tweak the security features on any instance.

Therefore, you should only give such access to users who you'd trust with root access to your system.

<!-- TODO -->
LXC (Linux Containers) is a powerful technology for creating and managing containers, which are lightweight, isolated environments for running applications. However, like any technology that involves isolation and resource sharing, security is a crucial consideration. Here's an overview of LXC's security model and some best practices:

LXC Security Model:
Namespaces:
LXC relies heavily on Linux namespaces for isolation. Namespaces ensure that containers have their own isolated view of the system, including processes, network interfaces, mounts, and more.
Control Groups (cgroups):
cgroups are used to limit and isolate resource usage (CPU, memory, I/O, etc.) of containers. This prevents a single container from exhausting the host's resources and affecting other containers.
Capabilities:
Linux capabilities partition the privileges traditionally associated with the superuser (root), allowing for more fine-grained control over what containers can do.
Mandatory Access Control (MAC):
Technologies like SELinux and AppArmor are used to restrict the actions a container can perform, adding an additional layer of security.
Filesystem Isolation:
Filesystem isolation (using chroot and mount namespaces) ensures that containers cannot access each other's files or the host's files unless explicitly allowed.
Security Concerns and Best Practices:
Running Containers as Non-Root:
Whenever possible, run containers as non-root users to limit the potential damage if the container is compromised.
Container Images Security:
Use trusted sources for container images and regularly update them to ensure they include the latest security patches.
Network Isolation and Firewalling:
Configure network namespaces and use firewalls (like iptables or nftables) to control network traffic to and from containers.
Regular Updates and Patching:
Regularly update the host system and the container environment to ensure you have the latest security fixes.
Restricting Capabilities:
Limit the Linux capabilities that are available to containers to reduce the risk of privilege escalation attacks.
Use MAC Policies:
Employ Mandatory Access Control systems like SELinux or AppArmor to enforce security policies on containers.
Resource Limits:
Set appropriate resource limits using cgroups to prevent Denial of Service (DoS) attacks from over-consuming system resources.
Isolate Sensitive Workloads:
For highly sensitive workloads, consider stronger isolation solutions like virtual machines or dedicated hosts.
Security Monitoring and Auditing:
Implement security monitoring and auditing tools to detect suspicious activities within containers or on the host system.
Understanding Shared Kernel Model:
Remember that all containers on a host share the same kernel. A vulnerability in the kernel can potentially impact all containers.
LXC vs. Other Container Technologies:
Compared to Docker or Kubernetes, LXC is often seen as providing a lower-level interface to containers, which can offer more control but might require more effort to secure.
Docker, for instance, comes with its own set of security enhancements and defaults that are tailored to its way of container management.
In summary, while LXC provides robust tools for isolating and managing containers, ensuring security in an LXC-based environment requires a comprehensive approach, including proper configuration, regular maintenance, and adherence to security best practices. As with any technology, staying informed about potential vulnerabilities and updates is crucial for maintaining a secure environment.


### Linux capabilities and Seccomp

DAC security. MAC security.
- chown
- chmod
- acl
- suid
- attr

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/container_security_guide/linux_capabilities_and_seccomp

https://earthly.dev/blog/intro-to-linux-capabilities/

### SELinux and AppArmor


## Running Docker in LXD
While LXD and Docker often get compared, they shouldn’t be seen as competing technologies. As illustrated above, they each have their own purpose and place in the digital world. In fact, even running Docker using LXD is possible and suitable in certain circumstances.

You can use LXD to create your virtual systems running inside the containers, segment them as you like, and easily use Docker to get the actual service running inside of the container.

If you are curious about how to do this, please take a look at this tutorial.

Or you can watch the video below, where Stéphane Graber leads you through the process.

https://www.youtube.com/watch?time_continue=1&v=_fCSSEyiGro&embeds_referring_euri=https%3A%2F%2Fubuntu.com%2F&embeds_referring_origin=https%3A%2F%2Fubuntu.com&source_ve_path=Mjg2NjY&feature=emb_logo


### Device passthrough


ChatGPT
Passing through a PCI device to an LXC (Linux Containers) container involves several steps, including identifying the PCI device, ensuring the host system is configured to allow PCI passthrough, and configuring the LXC container to use the device. Here's a step-by-step guide to accomplish this:

Step 1: Identify the PCI Device
List PCI Devices: On the host machine, use lspci to list all PCI devices and identify the one you want to pass through. The command is:
bash
Copy code
lspci
Get Detailed Information: Once you find the device, note down its PCI address, which is typically in the form 0000:00:1f.0. You can get more detailed information about the device using:
bash
Copy code
lspci -v -s 0000:00:1f.0
Step 2: Prepare the Host for PCI Passthrough
Enable IOMMU: Ensure that IOMMU (Input-Output Memory Management Unit) is enabled in the BIOS/UEFI settings of your host machine. This is necessary for PCI passthrough.
Configure the Kernel: Modify the GRUB configuration to enable IOMMU on the Linux kernel. This usually involves adding parameters like intel_iommu=on or amd_iommu=on to the GRUB command line. After editing /etc/default/grub, update GRUB with:
bash
Copy code
update-grub
Bind the PCI Device: Before passing the device to the container, it needs to be unbound from the host. This might involve unloading the driver or using tools like vfio-pci.
Step 3: Configure the LXC Container
Edit Container Configuration: Locate the LXC container configuration file, typically found in /var/lib/lxc/<container-name>/config.
Add PCI Device to the Configuration: You need to add lines to the container's configuration to allow it to use the PCI device. Add the following:
bash
Copy code
lxc.cgroup.devices.allow = c <major>:<minor> rwm
lxc.mount.entry = /dev/bus/pci/0000/00/1f.0 dev/bus/pci/0000/00/1f.0 none bind,optional,create=file
Replace 0000:00:1f.0 with your device's actual PCI address and <major>:<minor> with the device's major and minor numbers.
Restart the Container: For the changes to take effect, restart the container:
bash
Copy code
lxc-stop -n <container-name> && lxc-start -n <container-name>

## Apparmor
LXD confines containers by default with an apparmor profile which protects containers from each other and the host from containers. For instance this will prevent root in one container from signaling root in another container, even though they have the same uid mapping. It also prevents writing to dangerous, un-namespaced files such as many sysctls and /proc/sysrq-trigger.

If the apparmor policy for a container needs to be modified for a container c1, specific apparmor policy lines can be added in the raw.apparmor configuration key.

## Seccomp
All containers are confined by a default seccomp policy. This policy prevents some dangerous actions such as forced umounts, kernel module loading and unloading, kexec, and the open_by_handle_at system call. The seccomp configuration cannot be modified, however a completely different seccomp policy – or none – can be requested using raw.lxc (see below).

## Raw LXC configuration
LXD configures containers for the best balance of host safety and container usability. Whenever possible it is highly recommended to use the defaults, and use the LXD configuration keys to request LXD to modify as needed. Sometimes, however, it may be necessary to talk to the underlying lxc driver itself. This can be done by specifying LXC configuration items in the ‘raw.lxc’ LXD configuration key. These must be valid items as documented in the lxc.container.conf(5) manual page.

## Nesting, Limits, and Privileged Containers
Containers all share the same host kernel. This means that there is always an inherent trade-off between features exposed to the container and host security from malicious containers. Containers by default are therefore restricted from features needed to nest child containers. In order to run lxc or lxd containers under a lxd container, the security.nesting feature must be set to true:

lxc config set container1 security.nesting true
Once this is done, container1 will be able to start sub-containers.

In order to run unprivileged (the default in LXD) containers nested under an unprivileged container, you will need to ensure a wide enough UID mapping. Please see the ‘UID mapping’ section below.


### UID mappings and Privileged containers
By default, LXD creates unprivileged containers. This means that root in the container is a non-root UID on the host. It is privileged against the resources owned by the container, but unprivileged with respect to the host, making root in a container roughly equivalent to an unprivileged user on the host. (The main exception is the increased attack surface exposed through the system call interface)

Briefly, in an unprivileged container, 65536 UIDs are ‘shifted’ into the container. For instance, UID 0 in the container may be 100000 on the host, UID 1 in the container is 100001, etc, up to 165535. The starting value for UIDs and GIDs, respectively, is determined by the ‘root’ entry the /etc/subuid and /etc/subgid files. (See the subuid(5) man page.)

It is possible to request a container to run without a UID mapping by setting the security.privileged flag to true:

lxc config set c1 security.privileged true
Note however that in this case the root user in the container is the root user on the host.

### Aliases and Projects

name rename
alias
project

### init=/bin/bash in cmdline equivalent

The container requirements specify that every container must come with an empty /dev, /proc and /sys directory, and that /sbin/init must exist. If those directories don’t exist, LXD cannot mount them, and systemd will then try to do so. As this is an unprivileged container, systemd does not have the ability to do this, and it then freezes.

So you can see the environment before anything is changed, and you can explicitly change the init system in a container using the raw.lxc configuration parameter. This is equivalent to setting init=/bin/bash on the Linux kernel command line.

lxc config set systemd raw.lxc 'lxc.init.cmd = /bin/bash'

Here is what it looks like:

user@host:~$ lxc config set systemd raw.lxc 'lxc.init.cmd = /bin/bash'
user@host:~$ lxc start systemd
user@host:~$ lxc console --show-log systemd
 
Console log:
 
[root@systemd /]#
Now that the container has started, you can check it and see that things are not running as well as expected:

user@host:~$ lxc exec systemd -- bash
[root@systemd ~]# ls
[root@systemd ~]# mount
mount: failed to read mtab: No such file or directory
[root@systemd ~]# cd /
[root@systemd /]# ls /proc/
sys
[root@systemd /]# exit
Because LXD tries to auto-heal, it created some of the directories when it was starting up. Shutting down and restarting the container fixes the problem, but the original cause is still there - the template does not contain the required files.