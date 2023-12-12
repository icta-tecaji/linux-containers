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

## Running Docker in LXD
While LXD and Docker often get compared, they shouldn’t be seen as competing technologies. As illustrated above, they each have their own purpose and place in the digital world. In fact, even running Docker using LXD is possible and suitable in certain circumstances.

You can use LXD to create your virtual systems running inside the containers, segment them as you like, and easily use Docker to get the actual service running inside of the container.

If you are curious about how to do this, please take a look at this tutorial.

Or you can watch the video below, where Stéphane Graber leads you through the process.

https://www.youtube.com/watch?time_continue=1&v=_fCSSEyiGro&embeds_referring_euri=https%3A%2F%2Fubuntu.com%2F&embeds_referring_origin=https%3A%2F%2Fubuntu.com&source_ve_path=Mjg2NjY&feature=emb_logo
