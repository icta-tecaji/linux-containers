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