# LXD Introduction, Installation and Usage

Sources:
- ✅ [Run system containers with LXD](https://ubuntu.com/lxd)
- ✅ [LXD Docs](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/)
- ✅ [LXD Github](https://github.com/canonical/lxd)
- ✅ [LXD 2.0: Blog post series](https://stgraber.org/2016/03/11/lxd-2-0-blog-post-series-012/)
- ✅ [Containers - LXD](https://ubuntu.com/server/docs/containers-lxd)
- ✅ [About lxd and lxc](https://documentation.ubuntu.com/lxd/en/latest/explanation/lxd_lxc/#lxd-lxc)
- ✅ [About containers and VMs](https://documentation.ubuntu.com/lxd/en/latest/explanation/containers_and_vms/#containers-and-vms)
- ✅ [About instances](https://documentation.ubuntu.com/lxd/en/latest/explanation/instances/)


## LXD Introduction

LXD (`lɛks'di:`) is a modern, secure and powerful **container and virtual machine manager**, also sometimes referred to as "lightervisor" (lightweight hypervisor).

It provides a unified experience for running and **managing full Linux systems** inside containers or virtual machines. LXD supports images for a large number of Linux distributions (official Ubuntu images and images provided by the community) and is built around a very powerful, yet pretty simple, REST API. 

LXD scales from one instance on **a single machine to a cluster** in a full data center rack, making it suitable for running workloads both for development and in production.

LXD allows you to easily set up a system that feels like a small private cloud. You can run any type of workload in an efficient way while keeping your resources optimized.

You should consider using LXD if you want to containerize different environments or run virtual machines, or in general run and manage your infrastructure in a cost-effective way.

> **[LXD is now under Canonical](https://linuxcontainers.org/lxd/)** Canonical, the creator and main contributor of the LXD project has decided that after over 8 years as part of the Linux Containers community, the project would now be better served directly under Canonical’s own set of projects.

LXD provides **a better user experience to LXC** by building on top of LXC. LXD uses `liblxc` and its Go language bindings to create and manage containers.


### Releases

The current LTS releases are `LXD 5.0.x` (snap channel 5.0/stable) and `LXD 4.0.x` (snap channel 4.0/stable).
- The latest available version of the LXD package in Ubuntu is `5.19` (nov 2023).

The LTS releases **follow the Ubuntu release schedule and are released every two years**:
- `LXD 5.0` is supported until June 2027 and gets frequent bugfix and security updates, but does not receive any feature additions. Updates to this release happen approximately every six months, but this schedule should be seen as a rough estimation that can change based on priorities and discovered bugs.
- `LXD 4.0` is supported until June 2025.
- `LXD 6.0` is planned for April 2024 and will be supported until June 2029.

LTS releases are recommended for production environments, because they benefit from regular bugfix and security updates. However, there are no new features added to an LTS release, nor any kind of behavioral change.


### About LXD and LXC

LXD and LXC are two distinct implementations of Linux containers.
- **LXC** is a low-level user space interface for the Linux kernel containment features. It consists of tools (lxc-* commands), templates, and library and language bindings.
- **LXD** is a more intuitive and user-friendly tool aimed at making it easy to work with Linux containers. It is an alternative to LXC’s tools and distribution template system, with the added features that come from being controllable over the network. Under the hood, LXD uses LXC to create and manage the containers. LXD provides a superset of the features that LXC supports, and it is easier to use. Therefore, if you are unsure which of the tools to use, you should go for LXD. LXC should be seen as an alternative for experienced users that want to run Linux containers on distributions that don’t support LXD.


### LXD Daemon and LXD Client

The central part of LXD is its daemon. It runs persistently in the background, manages the instances, and handles all requests. The daemon provides a REST API that you can access directly or through a client (for example, the default command-line client that comes with LXD).

LXD is frequently confused with LXC, and the fact that LXD provides both a `lxd` command and a `lxc` command doesn’t make things easier.

> **Somewhat confusingly, LXD also provides an lxc command. This is different from the lxc command in the LXC package.**
> Note: all LXC command line tools are named `lxc-*`, while LXD tools are called `lxd` (daemon) and `lxc` (client). Note that there is no dash in the latter.

To control LXD, you typically use two different commands: lxd and lxc.
- **LXD daemon**
    - The `lxd` command controls the LXD daemon. Since the daemon is typically started automatically, *you hardly ever need to use the lxd command*. An exception is the `lxd init` subcommand that you run to initialize LXD.
    - There are also some subcommands for debugging and administrating the daemon, but they are intended for advanced users only.
- **LXD client**
    - The `lxc` command is a command-line client for LXD, which you can use to interact with the LXD daemon. You use the lxc command to manage your instances, the server settings, and overall the entities you create in LXD.
    - The lxc tool is not the only client you can use to interact with the LXD daemon. You can also use the API, the UI, or a custom LXD client.


### LXD Containers and Virtual Machines

LXD provides support for two different types of instances: system containers and virtual machines.

- When running a **system container**, LXD simulates a virtual version of a full operating system. To do this, it uses the functionality provided by the kernel running on the host system. You should **use a system container** to leverage the smaller size and **increased performance** if all functionality you require is compatible with the kernel of your host operating system.

- When running a **virtual machine**, LXD uses the hardware of the host system, but the kernel is provided by the virtual machine. Therefore, virtual machines can be used to run, for example, a different operating system. If you need functionality that is not supported by the OS kernel of your host system or you want to run a completely different OS, use a virtual machine.
    - LXD uses QEMU with Q35 UEFI layout and SecureBoot by default under the hood.
    - All devices are virtio-based (no complex device emulation at the host level). 
    - Main difference from other VM tools is in pre-installed image offerings and uniform management interface (same as with containers).

![Virtual machines vs. system containers](https://documentation.ubuntu.com/lxd/en/latest/_images/virtual-machines-vs-system-containers.svg)

> We are only going to work with containers in this course.


## LXD Installation and Initialization

Sources:

- ✅ [How to install LXD](https://documentation.ubuntu.com/lxd/en/latest/installing/)

### LXD Installation

The easiest way to install LXD is to install the snap package.
- Run `snap version` to find out if snap is installed on your system:
    - If you see a table of version numbers, snap is installed and you can continue with the next step of installing LXD. Otherwise install snap using the online documentation for your distribution.
        ```bash
        # example: snap installation on ubuntu
        sudo apt update
        sudo apt install snapd
        ```
- Enter the following command to install LXD: `sudo snap install lxd`
    - If you get an error message that the snap is already installed, run the following command to refresh it and ensure that you are running an up-to-date version: `sudo snap refresh lxd`
    - If snap is already installed and you want to install the latest stable version of LXD, run the following commands:
        - `sudo snap remove lxd`
        - `sudo snap install lxd`
- Check the installed snaps: `snap list`. You should see an output like:
    ```bash
    Name      Version         Rev    Tracking         Publisher   Notes
    lxd       5.19-8635f82    26200  latest/stable    canonical✓  -
    snapd     2.60.4          20290  latest/stable    canonical✓  snapd
    ...
    ```
- Check the version of LXD that you have installed: `lxd --version`
- Note the `Tracking` channel in `snap list` output. By default snap will automatically track the latest/stable channel and **will enable automatic snap updates**. In the case of LXD, this can be problematic because **all machines of a cluster must use the same version of the LXD snap**. Therefore, you should schedule your updates and make sure that all cluster members are in sync regarding the snap version that they use.
    - To prevent this behavior, you can manually hold the package updates using `sudo snap refresh --hold lxd` command.
    - When you choose to update your installation, use the following commands to remove the hold, update the snap, and hold the updates again:
        ```bash
        sudo snap refresh --unhold lxd
        sudo snap refresh lxd --cohort="+" # this flag ensures that all machines in a cluster see the same snap revision and are therefore not affected by a progressive rollout (lxd snap is a progressive release deployed to smaller number of users at first)
        sudo snap refresh --hold lxd
        ```
        > You can check snap refresh (update) timer using `sudo snap refresh --time` and alter its settings using `sudo snap set system refresh.timer=4:00-7:00,19:00-22:10`

For additional details on managing the LXD snap package, see [Manage the LXD Snap](./manage_lxd_snap.md).

### LXD Initialization

Sources:
- ✅ [How to initialize LXD](https://documentation.ubuntu.com/lxd/en/latest/howto/initialize/)

Before you can create a LXD instance, you must configure and initialize LXD. The following command is used to initialize LXD: `lxd init`. It allows for the configuration of:

- Directory or ZFS container backend. If you choose ZFS, you can choose which block devices to use, or the size of a file to use as backing store.
- Availability over the network.
- A ‘trust password’ used by remote clients to vouch for their client certificate.

> For simple configurations, you can run this command as a normal user. However, some more advanced operations during the initialization process (for example, joining an existing cluster) require root privileges. **In this case, run the command with sudo or as root.**

> Further LXD client commands `lxc` can be run as any user who is a member of group lxd. You can add users to the lxd group using the following command: `adduser <user> lxd`. Because group membership is normally only applied at login, you might need to either re-open your user session or use the `newgrp lxd` command in the shell you’re using to talk to LXD.
> Additional resources:
> - https://documentation.ubuntu.com/lxd/en/latest/installing/#manage-access-to-lxd
> - https://documentation.ubuntu.com/lxd/en/latest/explanation/security/#security-daemon-access

Run the following command to start the **interactive configuration process**:
```bash
sudo lxd init
```

The tool asks a series of questions to determine the required configuration. The questions are dynamically adapted to the answers that you give. They cover the following areas:
- **Clustering**: A cluster combines several LXD servers.The default answer is `no`, which means clustering is not enabled.
- **MAAS support**: MAAS is an open-source tool that lets you build a data center from bare-metal servers. The default answer is `no`, which means MAAS support is not enabled.
- **Networking**: Provides network access for the instances. You can let LXD create a new bridge (recommended) or use an existing network bridge or interface.
- **Storage pools**: Instances (and other data) are stored in storage pools. For testing purposes, you can create a loop-backed storage pool.
- **Remote access**: Allows remote access to the server over the network. The default answer is `no`, which means remote access is not allowed. 
- **Automatic image update**: You can download images from image servers. In this case, images can be updated automatically. The default answer is `yes`, which means that LXD will update the downloaded images regularly.

Check if the default bridge and storage pool have been created: `lxc network list` and `lxc storage list`.

You can now use `lxd init --dump` command to dump the LXD daemon preseed configuration YAML and `lxc info` to view further client and daemon configuration details.

## LXD Basic Usage

The primary LXD interface is offered by the LXD client - the `lxc` command. The `lxc` command can be run by any user that is a member of `lxd` group. The command line client offers several subcommadns. List them using `lxc --help`

```
Description:
  Command line client for LXD

  All of LXD's features can be driven through the various commands below.
  For help with any of those, simply call them with --help.

Usage:
  lxc [command]

Available Commands:
  alias       Manage command aliases
  cluster     Manage cluster members
  config      Manage instance and server configuration options
  console     Attach to instance consoles
  copy        Copy instances within or in between LXD servers
  delete      Delete instances and snapshots
  exec        Execute commands in instances
  export      Export instance backups
  file        Manage files in instances
  help        Help about any command
  image       Manage images
  import      Import instance backups
  info        Show instance or server information
  init        Create instances from images
  launch      Create and start instances from images
  list        List instances
  monitor     Monitor a local or remote LXD server
  move        Move instances within or in between LXD servers
  network     Manage and attach instances to networks
  operation   List, show and delete background operations
  pause       Pause instances
  profile     Manage profiles
  project     Manage projects
  publish     Publish instances as images
  query       Send a raw query to LXD
  rebuild     Rebuild instances
  remote      Manage the list of remote servers
  rename      Rename instances and snapshots
  restart     Restart instances
  restore     Restore instances from snapshots
  snapshot    Create instance snapshots
  start       Start instances
  stop        Stop instances
  storage     Manage storage pools and volumes
  version     Show local and remote versions
  warning     Manage warnings
```

If you need help for any specific subcommands you can also run those with the `--help` parameter.

```
lxc image --help
```

A complete LXD documentation with an included quick start guide is available at the following link: [https://documentation.ubuntu.com/lxd/en/latest/](https://documentation.ubuntu.com/lxd/en/latest/)


### LXD Images and Image Servers

Images are **available from remote image stores** but you can also **create your own images**, either based on an existing instances or a rootfs image.

Each image is identified by a fingerprint (SHA256). To make it easier to manage images, LXD allows defining one or more aliases for each image.

When you create an instance using a remote image, **LXD downloads the image and caches it locally**. It is stored in the local image store with the cached flag set. 

> LXD can automatically keep images that come from a remote server up to date.

Sources:

- ✅ [Remote image servers](https://documentation.ubuntu.com/lxd/en/latest/reference/remote_image_servers/)
- ✅ [About images](https://documentation.ubuntu.com/lxd/en/latest/image-handling/)
- ✅ [How to use remote images](https://documentation.ubuntu.com/lxd/en/latest/howto/images_remote/)

Unlike LXC, which uses an operating system template script to create its container, **LXD uses an image as the basis for its container**. It will download base images from a remote image store or make use of available images from a local image store. The image stores are simplestream or LXD servers exposed over a network.

The image store that will be used by LXD can be populated using three methods:

- **Using the built-in image remotes**
- Using a remote LXD as an image server
- Manually importing an image

The lxc CLI command comes pre-configured with the following **default remote image servers**:

- `lxc remote list`:
    - `ubuntu:`: This server provides official stable Ubuntu images. (https://cloud-images.ubuntu.com/releases/)
    - `ubuntu-daily:`: This server provides official daily Ubuntu images.
    - `ubuntu-minimal`: This server provides official Ubuntu Minimal images. (https://cloud-images.ubuntu.com/minimal/releases/)
    - `ubuntu-minimal-daily`: This server provides official daily Ubuntu Minimal images.
    - `images:`: This server provides unofficial images for a variety of Linux distributions. The images are maintained by the Linux Containers team and are built to be compact and minimal. (https://images.linuxcontainers.org/)
    - `local`: Local LXD instance and its image store

Remote servers that use the simple streams format are **pure image servers**. LXD supports the [following types](https://documentation.ubuntu.com/lxd/en/latest/reference/remote_image_servers/#remote-server-types) of remote image servers:

- Simple streams servers
- Public LXD servers (no auth)
- LXD servers

**Images contain a root file system and a metadata file that describes the image.** They can also contain templates for creating files inside an instance that uses the image. Images can be packaged as either a unified image (single file) or a split image (two files).

LXD container images have the following structure:

```
metadata.yaml
rootfs/ (directory, squashfs or .img file in qcow2 for VMs)
templates/ (optional directory)
```

The images are **packaged as tarballs** (unified .tar.xz or split). The image identifier for unified images is the SHA-256 of the tarball.

The `metadata.yaml` file contains information that is relevant to running the image in LXD. It includes the following information:

```
architecture: x86_64
creation_date: 1424284563
properties:
  description: Ubuntu 22.04 LTS Intel 64bit
  os: Ubuntu
  release: jammy 22.04
templates:
  ...
```

The optional `templates/metadata.yaml` are used to dynamically create files inside an instance in Pongo2 template engine format:

```
templates:
  /etc/hosts:
    when:
      - create
      - rename
    template: hosts.tpl
    properties:
      foo: bar
  /etc/hostname:
    when:
      - start
    template: hostname.tpl
  /etc/network/interfaces:
    when:
      - create
    template: interfaces.tpl
    create_only: true
```

The when key parameter can be:
- create - run at the time a new instance is created from the image
- copy - run when an instance is created from an existing one
- start - run every time the instance is started

> Some remotes also include the image manifest files, listing the installed packages and their versions.

- List current local images with: `lxc image list`
- List remotes with: `lxc remote list`
- List remote images with: `lxc image list <remote:>`

> To add a remote image server follow the instructions in the [Add a remote image server](https://documentation.ubuntu.com/lxd/en/latest/howto/images_remote/#add-a-remote-server) section.


### Running Your First System Container with LXD

Sources:

- ✅ [How to create instances](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_create/#instances-create)

For creating and managing instances, we use the LXD command line client `lxc`.

To create an instance, you can use either the `lxc init` or the `lxc launch` command. The `lxc init` command only creates the instance, while the `lxc launch` command creates and starts it.

Use the following syntax to create a container: `lxc launch|init <image_server>:<image_name> <instance_name> [flags]`

- You can list all images that are available from a remote using the following syntax: `lxc image list [<remote>:]`

- List local images by running the following command: `lxc image list local:`
- List images from ubuntu remote by version and type filter: `lxc image list ubuntu:22.04 type=container`
- List image info: `lxc image info ubuntu:22.04`
- List image properties: `lxc image show ubuntu:22.04`
- Launch a container called `first` using the `Ubuntu 22.04` image:
    - `lxc launch ubuntu:22.04 first`

The preceding command will **pull an image, create and start** a new Ubuntu container named `first`, which can be confirmed with the following command:

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


### Interacting with Containers

Sources:

- ✅ [How to run commands in an instance](https://documentation.ubuntu.com/lxd/en/latest/instance-exec/#run-commands)
- ✅ [How to access files in an instance](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_access_files/#instances-access-files)

LXD allows to run commands inside an instance using the LXD client, without needing to access the instance through the network.

You can interact with your instances by running commands in them (including an interactive shell) or accessing the files in the instance. To run commands inside your instance, use the `lxc exec` command.

Start by **launching an interactive shell** in your instance:

- Create and start `lxc launch ubuntu:22.04 first` or just start `lxc start first` your container.
- Exec bash `lxc exec first -- bash`
- Shorthand for the previous command is `lxc shell first`
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

To pull/push a directory with all contents, enter the following command:
- `lxc file [pull|push] -r <instance_name>/<path_to_directory> <local_location>`

To **edit a file in an instance** from your local machine, enter the following command:
- `lxc file edit first/etc/hosts` (The file must already exist on the instance. You cannot use the edit command to create a file on the instance.)

To **delete a file** from your instance, enter the following command: 
- `lxc file delete <instance_name>/<path_to_file>`


### LXD Profiles and Container Configuration

Sources:

- ✅ [Configure instances](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/#configure-instances)
- ✅ [Instance options](https://documentation.ubuntu.com/lxd/en/latest/reference/instance_options/#instance-options)

Containers are configured according to a set of **profiles** and a set of **container-specific configuration**. Profiles are applied first, so that container specific configuration can override profile configuration.

**Container Configuration**

Container configuration includes properties like the architecture, limits on resources such as CPU and RAM, security details including apparmor restriction overrides, and devices to apply to the container.

Show basic details of an existing container
- `lxc info <container_name>`

Show configuration of an existing container
- `lxc config show <container_name>`

**To set instance options and properties (--property flag), the `lxc config set` command can be used.** A list of all [available configuration options is accessible here](https://documentation.ubuntu.com/lxd/en/latest/reference/instance_options/#instance-options).

Available configuration options include **limits** - flexible constraints on the resources which containers can consume. The limits come in the following categories:

- CPU: limit cpu available to the container in several ways.
- Disk: configure the priority of I/O requests under load
- RAM: configure memory and swap availability
- Network: configure the network priority under load
- Processes: limit the number of concurrent processes in the container.

To set container configuration for an existing container use the following syntax:
- `lxc config set <instance_name> <option_key>=<option_value> <option_key>=<option_value> ...`

For our first continer:
- `lxc config set first limits.memory=1GiB`

To set configuration during container creation (launch):
- `lxc launch ubuntu:22.04 limited --config limits.cpu=1 --config limits.memory=192MiB`

Now check the differences between the host and the containers:

```bash
# memory
free -h
lxc exec first -- free -h
lxc exec limited -- free -h
# cpus
nproc
lxc exec first -- nproc
lxc exec limited -- nproc
```

Besides limits, configuration options may also add devices to containers, set autostart options, and load kernel modules or alter sysctl config.

For instance, to mount /opt in container at /opt, you could add a disk device:
- `lxc config device add <container_name> <device_name> disk source=/opt path=opt`
- to reconfigure use `lxc config device set <container_name> <device_name> ...`

To enable container autostart, you can use:
- `lxc config set <container_name> boot.autostart=true`

To edit the whole configuration, you can use:
- `lxc config edit <container_name>`

**Profiles**

Profiles are named collections of configurations which may be applied to more than one container. For instance, all containers created with lxc launch, by default, include the default profile, which provides a network interface eth0.

> To mask a device which would be inherited from a profile but which should not be in the final container, define a device by the same name but of type ‘none’:

Profiles store a set of configuration options. They can contain instance options, devices and device options.

You can apply any number of profiles to an instance. They are applied in the order they are specified, so the last profile to specify a specific key takes precedence.

Enter the following command to display a list of all available profiles:
- `lxc profile list`

Enter the following command to display the contents of a profile:
- `lxc profile show <profile_name>`

Create an empty profile or delete an existing:
- `lxc profile create <profile_name>`
- `lxc profile delete <profile_name>`

To set an instance option for a profile, use the lxc profile set command. Specify the profile name and the key and value of the instance option:
- `lxc profile set <profile_name> <option_key>=<option_value> <option_key>=<option_value> ...`

Lastly, to apply or remove profiles from an instance:
- `lxc profile add <instance_name> <profile_name>`
- `lxc profile remove <instance_name> <profile_name>`

Or configure profiles during container creation time:
- `lxc launch <image> <instance_name> --profile <profile> --profile <profile> ...

> Example: create an autoboot profile
> ```bash
> lxc profile create autoboot
> lxc profile set autoboot boot.autostart=true
> for ct in {"first", "limited"}; do lxc profile add $ct autoboot; done;
> lxc profile show autoboot
> ```


### Logs and Troubleshooting

To view debug information about LXD itself, on a systemd based host use:
- `journalctl -u lxd`

Container logfiles for a container may be seen using:
- `lxc info <container_name> --show-log`

The configuration file which was used may be found under `/var/log/lxd/<container_name>/lxc.conf` while apparmor profiles can be found in `/var/lib/lxd/security/apparmor/profiles/<container_name>` and seccomp profiles in `/var/lib/lxd/security/seccomp/<contianer_name>`.

