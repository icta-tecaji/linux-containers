- https://documentation.ubuntu.com/lxd/en/latest/explanation/performance_tuning/
- https://documentation.ubuntu.com/lxd/en/latest/production-setup/



## Security
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


## Running Docker in LXD
While LXD and Docker often get compared, they shouldn’t be seen as competing technologies. As illustrated above, they each have their own purpose and place in the digital world. In fact, even running Docker using LXD is possible and suitable in certain circumstances.

You can use LXD to create your virtual systems running inside the containers, segment them as you like, and easily use Docker to get the actual service running inside of the container.

If you are curious about how to do this, please take a look at this tutorial.

Or you can watch the video below, where Stéphane Graber leads you through the process.

https://www.youtube.com/watch?time_continue=1&v=_fCSSEyiGro&embeds_referring_euri=https%3A%2F%2Fubuntu.com%2F&embeds_referring_origin=https%3A%2F%2Fubuntu.com&source_ve_path=Mjg2NjY&feature=emb_logo
