# LXD

Sources:
- [Run system containers with LXD](https://ubuntu.com/lxd)
- ✅ [LXD Docs](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/)
- [LXD Github](https://github.com/canonical/lxd)
- [Containers - LXD](https://ubuntu.com/server/docs/containers-lxd)

## LXD Introduction

LXD (`lɛks'di:`) is a modern, secure and powerful system **container and virtual machine manager**.

It provides a unified experience for running and **managing full Linux systems** inside containers or virtual machines. LXD supports images for a large number of Linux distributions (official Ubuntu images and images provided by the community) and is built around a very powerful, yet pretty simple, REST API. 

LXD scales from one instance on **a single machine to a cluster** in a full data center rack, making it suitable for running workloads both for development and in production.

LXD allows you to easily set up a system that feels like a small private cloud. You can run any type of workload in an efficient way while keeping your resources optimized.

You should consider using LXD if you want to containerize different environments or run virtual machines, or in general run and manage your infrastructure in a cost-effective way.

> **[LXD is now under Canonical](https://linuxcontainers.org/lxd/)** Canonical, the creator and main contributor of the LXD project has decided that after over 8 years as part of the Linux Containers community, the project would now be better served directly under Canonical’s own set of projects.

LXD provides **a better user experience to LXC** by building on top of LXC. LXD
uses `liblxc` and its Go language bindings to create and manage containers.

## Releases
The current LTS releases are `LXD 5.0.x` (snap channel 5.0/stable) and `LXD 4.0.x` (snap channel 4.0/stable).
- The latest available version of the LXD package in Ubuntu is `5.19` (nov 2023).

The LTS releases **follow the Ubuntu release schedule and are released every two years**:
- `LXD 5.0` is supported until June 2027 and gets frequent bugfix and security updates, but does not receive any feature additions. Updates to this release happen approximately every six months, but this schedule should be seen as a rough estimation that can change based on priorities and discovered bugs.
- `LXD 4.0` is supported until June 2025.
- `LXD 6.0` is planned for April 2024 and will be supported until June 2029.

LTS releases are recommended for production environments, because they benefit from regular bugfix and security updates. However, there are no new features added to an LTS release, nor any kind of behavioral change.

## About lxd and lxc
- [About lxd and lxc](https://documentation.ubuntu.com/lxd/en/latest/explanation/lxd_lxc/#lxd-lxc)

LXD is frequently confused with LXC, and the fact that LXD provides both a lxd command and a lxc command doesn’t make things easier.

> **Somewhat confusingly, LXD also provides an lxc command. This is different from the lxc command in the LXC package.**

<!-- TODO -->
<!-- TODO -->
<!-- TODO -->

## Install LXD
- ✅ [How to install LXD](https://documentation.ubuntu.com/lxd/en/latest/installing/)

The easiest way to install LXD is to install the snap package.
- Run `snap version` to find out if snap is installed on your system:
    - `snap version`: If you see a table of version numbers, snap is installed and you can continue with the next step of installing LXD. Otherwise install snap using the [guide](./snap.md).
    - Enter the following command to install LXD: `sudo snap install lxd`
        - If you get an error message that the snap is already installed, run the following command to refresh it and ensure that you are running an up-to-date version: `sudo snap refresh lxd`
    - Check the installed snaps: `snap list`
    - Check the version of LXD that you have installed: `lxd --version`

For managing the LXD snap package, see [Manage the LXD Snap](./manage_lxd_snap.md).

## Initialize LXD
- ✅ [How to initialize LXD](https://documentation.ubuntu.com/lxd/en/latest/howto/initialize/)

Before you can create a LXD instance, you must configure and initialize LXD. Enter the following command to initialize LXD with a **minimal setup** and default options: `lxd init --minimal`

> For simple configurations, you can run this command as a normal user. However, some more advanced operations during the initialization process (for example, joining an existing cluster) require root privileges. In this case, run the command with sudo or as root.

Run the following command to start the **interactive configuration process**: `lxd init`

The tool asks a series of questions to determine the required configuration. The questions are dynamically adapted to the answers that you give. They cover the following areas:
- **Clustering**: A cluster combines several LXD servers.The default answer is `no`, which means clustering is not enabled.
- **MAAS support**: MAAS is an open-source tool that lets you build a data center from bare-metal servers. The default answer is `no`, which means MAAS support is not enabled.
- **Networking**: Provides network access for the instances. You can let LXD create a new bridge (recommended) or use an existing network bridge or interface.
- **Storage pools**: Instances (and other data) are stored in storage pools. For testing purposes, you can create a loop-backed storage pool.
- **Remote access**: Allows remote access to the server over the network. The default answer is `no`, which means remote access is not allowed. 
- **Automatic image update**: You can download images from image servers. In this case, images can be updated automatically. The default answer is `yes`, which means that LXD will update the downloaded images regularly.

## Remote image servers
- [Remote image servers](https://documentation.ubuntu.com/lxd/en/latest/reference/remote_image_servers/)
- [How to use remote images](https://documentation.ubuntu.com/lxd/en/latest/howto/images_remote/)

Unlike LXC, which uses an operating system template script to create its container, **LXD uses an image as the basis for its container**. It will download base images from a remote image store or make use of available images from a local image store. The image stores are simply LXD servers exposed over a network.

The image store that will be used by LXD can be populated using three methods:
- **Using the built-in image remotes**
- Using a remote LXD as an image server
- Manually importing an image

The lxc CLI command comes pre-configured with the following **default remote image servers** - `lxc remote list`:
- `ubuntu:`: This server provides official stable Ubuntu images. (https://cloud-images.ubuntu.com/releases/)
- `ubuntu-daily:`: This server provides official daily Ubuntu images.
- `ubuntu-minimal`: This server provides official Ubuntu Minimal images. (https://cloud-images.ubuntu.com/minimal/releases/)
- `ubuntu-minimal-daily`: This server provides official daily Ubuntu Minimal images.
- `images:`: This server provides unofficial images for a variety of Linux distributions. The images are maintained by the Linux Containers team and are built to be compact and minimal. (https://images.linuxcontainers.org/)

Remote servers that use the simple streams format are pure image servers. LXD supports the [following types](https://documentation.ubuntu.com/lxd/en/latest/reference/remote_image_servers/#remote-server-types) of remote image servers:
- Simple streams servers
- Public LXD servers
- LXD servers

## LXD instances (containers and VMs)
- [About containers and VMs](https://documentation.ubuntu.com/lxd/en/latest/explanation/containers_and_vms/#containers-and-vms)
- [About instances](https://documentation.ubuntu.com/lxd/en/latest/explanation/instances/)

LXD provides support for two different types of instances: system containers and virtual machines.
- When running a **system container**, LXD simulates a virtual version of a full operating system. To do this, it uses the functionality provided by the kernel running on the host system.
- When running a **virtual machine**, LXD uses the hardware of the host system, but the kernel is provided by the virtual machine. Therefore, virtual machines can be used to run, for example, a different operating system.

<!-- TODO -->
<!-- TODO -->
<!-- TODO -->


## Running Your First System Container with LXD

For managing instances, we use the LXD command line client lxc.
- You can list all images that are available locally by running the following command: `lxc image list local:`
- Launch a container called `first` using the `Ubuntu 22.04` image:
    - `lxc launch ubuntu:22.04 first`

The preceding command will **create and start** a new Ubuntu container named first, which can be confirmed with the following command:
- `lxc list`
- `lxc image list`: new images are downloaded automatically when you launch a container from an image that is not available locally.

If the container name is not given, then LXD will give it a random name.
- `lxc launch ubuntu:22.04`
- `lxc list`
- Launching this container is quicker than launching the first, because the image is already available.

Query more **information** about each container with:
- `lxc info first`
- `lxc info <container_name>`

To **stop a running container**, use the following command, which will stop the container but keep the image so it may be restarted again later: 
- `lxc stop <container_name>`
- `lxc list`

To permanently remove or delete the container, use the following command:
- `lxc delete <container_name>`
- `lxc list`

Delete the `first` container: `lxc delete first`

Since this container is running, you get an error message that you must stop it first. Alternatively, you can force-delete it: `lxc delete first --force`
- `lxc list`

## Interact with Containers
- ✅ [How to run commands in an instance](https://documentation.ubuntu.com/lxd/en/latest/instance-exec/#run-commands)
- ✅ [How to access files in an instance](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_access_files/#instances-access-files)

LXD allows to run commands inside an instance using the LXD client, without needing to access the instance through the network.

You can interact with your instances by running commands in them (including an interactive shell) or accessing the files in the instance. To run commands inside your instance, use the `lxc exec` command.

Start by **launching an interactive shell** in your instance:
- `lxc launch ubuntu:22.04 first`
- `lxc exec first -- bash`
- `ls /`
- Display information about the operating system: `cat /etc/*release`
- `apt update`
- Exit the interactive shell: `exit`

Instead of logging on to the instance and running commands there, you can **run commands directly from the host**.
- `lxc exec first -- apt upgrade -y`

You can manage files inside an instance using the LXD client without needing to access the instance through the network. Files can be individually edited or deleted, pushed from or pulled to the local machine.

You can also **access the files** from your instance and interact with them:
- Pull a file from the container: `lxc file pull first/etc/hosts .`
- `cat hosts`
- Add an entry to the file: `echo "1.2.3.4 my-example" >> hosts`
- `cat hosts`
- Push the file back to the container: `lxc file push hosts first/etc/hosts`
- `lxc exec first -- cat /etc/hosts`

Instead of pulling the instance file into a file on the local system, you can also pull it to stdout and pipe it to stdin of another command. This can be useful, for example, to **check a log file**:
- `lxc file pull first/var/log/syslog - | less`

> To pull/push a directory with all contents, enter the following command: `lxc file [pull|push] -r <instance_name>/<path_to_directory> <local_location>`

To **edit an instance file** from your local machine, enter the following command:
- `lxc file edit first/etc/hosts` (The file must already exist on the instance. You cannot use the edit command to create a file on the instance.)

To **delete a file** from your instance, enter the following command:
`lxc file delete <instance_name>/<path_to_file>`

## Running Your First Virtual Machine with LXD
Launch a VM called ubuntu-vm using the Ubuntu 22.04 image:
- lxc launch ubuntu:22.04 ubuntu-vm --vm

> Even though you are using the same image name to launch the instance, LXD downloads a slightly different image that is compatible with VMs.

Commands: For containers, this always works and is handled directly by LXD. For virtual machines, the lxd-agent process must be running inside of the virtual machine for this to work.

Files: For virtual machines, the lxd-agent process must be running inside of the virtual machine for them to work.


<!-- TODO -->
<!-- TODO -->
<!-- TODO -->


## Images
- https://documentation.ubuntu.com/lxd/en/latest/image-handling/

## Create instances
- [How to create instances](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_create/#instances-create)

To create an instance, you can use either the `lxc init` or the `lxc launch` command. The `lxc init` command only creates the instance, while the `lxc launch` command creates and starts it.

Enter the following command to create a container: `lxc launch|init <image_server>:<image_name> <instance_name> [flags]`

<!-- TODO -->
<!-- TODO -->
<!-- TODO -->

## Instance configuration
- https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/#configure-instances
- https://documentation.ubuntu.com/lxd/en/latest/reference/instance_options/#instance-options


## Mounting storage volumes
- [Mount a file system from the instance](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_access_files/#mount-a-file-system-from-the-instance)


## Manage snapshots
- https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/#manage-snapshots
- https://documentation.ubuntu.com/lxd/en/latest/migration/

## Copying Containers

Copy the first container into a container called third:
- lxc copy first third

You will see that all but the third container are running. This is because you created the third container by copying the first, but you didn’t start it.

You can start the third container with:

lxc start third

https://ubuntu.com/server/docs/containers-lxd

https://ubuntu.com/lxd


https://linuxcontainers.org/lxd/
https://linuxcontainers.org/incus/


## LXD Images

## Running Docker in LXD
While LXD and Docker often get compared, they shouldn’t be seen as competing technologies. As illustrated above, they each have their own purpose and place in the digital world. In fact, even running Docker using LXD is possible and suitable in certain circumstances.

You can use LXD to create your virtual systems running inside the containers, segment them as you like, and easily use Docker to get the actual service running inside of the container.

If you are curious about how to do this, please take a look at this tutorial.

Or you can watch the video below, where Stéphane Graber leads you through the process.

https://www.youtube.com/watch?time_continue=1&v=_fCSSEyiGro&embeds_referring_euri=https%3A%2F%2Fubuntu.com%2F&embeds_referring_origin=https%3A%2F%2Fubuntu.com&source_ve_path=Mjg2NjY&feature=emb_logo


## Manage LXD
- https://documentation.ubuntu.com/lxd/en/latest/installing/#manage-access-to-lxd
If the lxd group is missing on your system, create it and restart the LXD daemon. You can then add trusted users to the group. Anyone added to this group will have full control over LXD.

Because group membership is normally only applied at login, you might need to either re-open your user session or use the newgrp lxd command in the shell you’re using to talk to LXD.

Access control for LXD is based on group membership. The root user and all members of the lxd group can interact with the local daemon. See Access to the LXD daemon for more information.

- https://documentation.ubuntu.com/lxd/en/latest/explanation/security/#security-daemon-access

<!-- TODO -->
<!-- TODO -->
<!-- TODO -->