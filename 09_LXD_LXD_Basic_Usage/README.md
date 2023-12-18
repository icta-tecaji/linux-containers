# LXD Basic Usage

The primary LXD interface is offered by the LXD client - the `lxc` command. The `lxc` command can be run by any user that is a member of `lxd` group. The command line client offers several subcommands. List them using `lxc --help`

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


## LXD Images and Image Servers

Sources:

- ✅ [Remote image servers](https://documentation.ubuntu.com/lxd/en/latest/reference/remote_image_servers/)
- ✅ [About images](https://documentation.ubuntu.com/lxd/en/latest/image-handling/)
- ✅ [How to use remote images](https://documentation.ubuntu.com/lxd/en/latest/howto/images_remote/)

Unlike LXC, which uses an operating system template script to create its container, **LXD uses an image as the basis for its container**. It will download base images from a remote image store or make use of available images from a local image store. The image stores are simplestream or LXD servers exposed over a network.

The image store that will be used by LXD can be populated using three methods:

- **Using the built-in image remotes**
- Using a remote LXD as an image server
- Manually importing an image

Images are **available from remote image stores** but you can also **create your own images**, either based on an existing instances or a rootfs image.

Each image is identified by a fingerprint (SHA256). To make it easier to manage images, LXD allows defining one or more aliases for each image.

When you create an instance using a remote image, **LXD downloads the image and caches it locally**. It is stored in the local image store with the cached flag set. 

> LXD can automatically keep images that come from a remote server up to date.

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


## Running Your First System Container with LXD

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


## Interacting with Containers

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


## LXD Profiles and Container Configuration

Sources:

- ✅ [Configure instances](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/#configure-instances)
- ✅ [Instance options](https://documentation.ubuntu.com/lxd/en/latest/reference/instance_options/#instance-options)

Containers are configured according to a set of **profiles** and a set of **container-specific configuration**. Profiles are applied first, so that container specific configuration can override profile configuration.

### Container Configuration

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


### Profiles

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


## Managing Container Instances

Sources:

- [Backing up instances](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_backup/)

### Back up

There are different ways of backing up your instances:

- Use snapshots for instance backup
- Use export files for instance backup
- Copy an instance to a backup server

Which method to choose depends both on your use case and on the storage driver you use. In general, **snapshots are quick and space efficient** (depending on the storage driver, except for dir driver), but they are stored in the same storage pool as the instance and therefore not too reliable.

**Export files** can be stored on different disks and are therefore more reliable. They can also be used to restore the instance into a different storage pool. If you have a separate, network-connected LXD server available, **regularly copying instances to this other server** gives high reliability as well, and this method can also be used to back up snapshots of the instance.

### Snapshots

Sources:

- [Manage snapshots](https://documentation.ubuntu.com/lxd/en/latest/tutorial/first_steps/#manage-snapshots)
- [Migration](https://documentation.ubuntu.com/lxd/en/latest/migration/)

You can save your instance at a point in time by creating an instance snapshot, which makes it easy to restore the instance to a previous state. Most storage drivers support optimized snapshot creation (e.g., COW, fast and efficient operation).

**Create snapshot**

Use the following command to create a snapshot of an instance:
- `lxc snapshot <instance_name> [<snapshot name>]`

> Add the `--reuse` flag in combination with a snapshot name to replace an existing snapshot.

> By default, snapshots are kept forever, unless the `snapshots.expiry` configuration option is set. (`lxc profile set default snapshots.expiry 1d`)

> For virtual machines, you can add the `--stateful` flag to capture not only the data included in the instance volume but also the running state of the instance. Note that this feature is not fully supported for containers because of CRIU (Checkpoint/Restore In Userspace) limitations.

> To use CRIU you have to enable it using snap:
>   ```
>   sudo snap set lxd criu.enable=true
>   sudo snap restart lxd
>   sudo snap get lxd criu
>   ```

**Restore from snapshot**

To do so, use the following command:
- `lxc restore <instance_name> <snapshot_name>`

> If the snapshot is stateful (which means that it contains information about the running state of the instance), you can add the `--stateful` flag to restore the state.

New containers can also be created by copying a container or snapshot:
- `lxc copy <instance_name>/<snapshot_name> testcontainer`

**Manage snapshots**

Use the following command to display the snapshots for an instance:
- `lxc info <instance_name>`

You can view or modify snapshots in a similar way to instances, by referring to the snapshot with `<instance_name>/<snapshot_name>`.

To show configuration information about a snapshot, use the following command:
- `lxc config show <instance_name>/<snapshot_name>`

To change the expiry date of a snapshot, use the following command:
- `lxc config edit <instance_name>/<snapshot_name>`

To delete a snapshot, use the following command:
- `lxc delete <instance_name>/<snapshot_name>`

**Schedule snapshots**

Use cron-like syntax. For example, to configure daily snapshots, use the following command:
- `lxc config set <instance_name> snapshots.schedule @daily`

> When scheduling regular snapshots, consider setting an automatic expiry (`snapshots.expiry`) and a naming pattern for snapshots (`snapshots.pattern`). You should also configure whether you want to take snapshots of instances that are not running (`snapshots.schedule.stopped`).


### Backup/Restore to/from File (Export/Import)

Use the following command to export an instance to a compressed file (for example, /path/to/my-instance.tgz):
- `lxc export <instance_name> [<file_path>]`

If you were to list file contents, you'd discover that the exported tar file includes container configuration details (not just disk data):

```
tar -ztf ./f.tar.xz | head
```

```
backup/index.yaml
backup/snapshots/first_snap
backup/snapshots/first_snap/backup.yaml
backup/snapshots/first_snap/metadata.yaml
backup/snapshots/first_snap/rootfs
backup/snapshots/first_snap/rootfs/bin
backup/snapshots/first_snap/rootfs/boot
backup/snapshots/first_snap/rootfs/burek
backup/snapshots/first_snap/rootfs/dev
backup/snapshots/first_snap/rootfs/dev/console
```

You can import an export file (for example, /path/to/my-backup.tgz) as a new instance. To do so, use the following command:
- `lxc import <file_path> [<instance_name>]`


### Copying or Moving Containers

**Copying**

Copy the first container into a container called third:
- `lxc copy first third`

You will see that all but the third container are running. This is because you created the third container by copying the first, but you didn’t start it.

You can start the third container with:
- `lxc start third`

You can also copy the instance between servers:
- `lxc copy [<source_remote>:]<source_instance_name> <target_remote>:[<target_instance_name>]`

**Moving, renaming and live migration**

Containers can be renamed and live-migrated using the lxc move command:
- `lxc move c1 final-beta`

> Live migration means migrating an instance while it is running. This method is supported for virtual machines.

For containers, there is limited support for live migration using CRIU. However, because of extensive kernel dependencies, only very basic containers (non-systemd containers without a network device) can be migrated reliably. In most real-world scenarios, you should stop the container, move it over and then start it again.

If you want to use live migration for containers, you must enable CRIU on both the source and the target server. If you are using the snap, use the following commands to enable CRIU:

```
snap set lxd criu.enable=true
sudo systemctl reload snap.lxd.daemon
```

### Create, Manage and Publish Images

When working with images, you can inspect various information about the available images, view and edit their properties and [configure aliases to refer to specific images](https://documentation.ubuntu.com/lxd/en/latest/howto/images_manage/#configure-image-aliases). You can also export an image to a file, which can be useful to copy or import it on another machine.

**Publishing images**

When a container or container snapshot is ready for consumption by others, it can be published as a new image using;
- lxc publish <container_name>/<snapshot_name> --alias <published_image_alias>

The published image will be private by default, meaning that LXD will not allow clients without a trusted certificate to see them. If the image is safe for public viewing (i.e. contains no private information), then the ‘public’ flag can be set, either at publish time using:

- `lxc publish <container_name>/<snapshot_name> --alias <published_image_alias> public=true`

or after the fact using:

- `lxc image edit <published_image_alias>`

and changing the value of the public field.

**Export/import image**

Image can be exported as, and imported from, tarballs:
- `lxc image export <published_image_alias>0 <published_image_alias>.tar.gz`
- `lxc image import <published_image_alias>.tar.gz --alias <published_image_alias> --public`

> To import a split image, enter the following command:
> - `lxc image import <metadata_tarball_path> <rootfs_tarball_path> [<target_remote>:]`


## Logs and Troubleshooting

To view debug information about LXD itself, on a systemd based host use:
- `journalctl -u lxd`

Container logfiles for a container may be seen using:
- `lxc info <container_name> --show-log`

The LXD snap includes a tool that collects the relevant server information for debugging. Enter the following command to run it:
- `sudo lxd.buginfo`

The configuration file which was used may be found under `/var/log/lxd/<container_name>/lxc.conf` while apparmor profiles can be found in `/var/lib/lxd/security/apparmor/profiles/<container_name>` and seccomp profiles in `/var/lib/lxd/security/seccomp/<contianer_name>`.

