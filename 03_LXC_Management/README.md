# LXC Management

## Autostart LXC containers
- [lxc-autostart](https://linuxcontainers.org/lxc/manpages//man1/lxc-autostart.1.html)
- [Auto-start](https://stgraber.org/2013/12/21/lxc-1-0-your-second-container/)

LXC does not have a long-running daemon. 

**By default, LXC containers do not start after a server reboot.** LXC supports marking containers to be started at system boot. Prior to Ubuntu 14.04, this was done using symbolic links under the directory /etc/lxc/auto. Starting with Ubuntu 14.04, it is done through the container configuration files. 

To change that, we can use the `lxc-autostart` tool and the containers configuration file. Each container has a configuration file typically under `/var/lib/lxc/<container name>/config` for privileged containers and `$HOME/.local/share/lxc/<container name>/config` for unprivileged containers.

The startup related values that are available are:
- `lxc.start.auto` = 0 (disabled) or 1 (enabled)
- `lxc.start.delay` = 0 (delay in second to wait after starting the container)
- `lxc.start.order` = 0 (priority of the container, higher value means starts earlier)
- `lxc.group` = group1,group2,group3,… (groups the container is a member of)

`lxc-autostart` processes containers with lxc.start.auto set. It **lets the user start, shutdown, kill, restart containers in the right order, waiting the right time.** Supports filtering by lxc.group or just run against all defined containers. It can also be used by external tools in list mode where no action will be performed and the list of affected containers (and if relevant, delays) will be shown. The [-r], [-s] and [-k] options specify the action to perform. If none is specified, then the containers will be started.

When your machine starts, an init script will ask `lxc-autostart` to start all containers of a given group (by default, all containers which aren’t in any) in the right order and waiting the specified time between them.
1. Create the containers:
```bash
# Create the first container (no autostart):
sudo lxc-create -t download \
  -n 01-no-autostart -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Create the second container (autostart):
sudo lxc-create -t download \
  -n 02-autostart-privileged -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Check (autostart is 0):
sudo lxc-ls --fancy

# Add the autostart option to the containers configuration files:
sudo su
echo "lxc.start.auto = 1" >> /var/lib/lxc/02-autostart-privileged/config
exit

# Check (autostart is 1 in the configuration files for the selected containers):
sudo lxc-ls --fancy

# List all containers that are configured to start automatically:
sudo lxc-autostart --list

# Now we can use the lxc-autostart command again to start all containers
#configured to autostart
sudo lxc-autostart -a
sudo lxc-start -n 01-no-autostart

# Check (autostart is 0):
sudo lxc-ls --fancy
```
> Unprivileged containers can’t be started at boot time as they require additional setup to be done by the user. [Guide](https://bobcares.com/blog/lxc-autostart-unprivileged-containers/)

2. Reboot the server: `sudo reboot`
3. Check the containers status: `sudo lxc-ls --fancy` (the autostart container is running)
4. Stop and destroy the containers:
```bash
sudo lxc-stop -n 02-autostart-privileged
sudo lxc-destroy -n 01-no-autostart
```

Two other useful autostart configuration parameters are adding a delay to the
start, and defining a group in which multiple containers can start as a single unit.
```bash
sudo su
echo "lxc.start.delay = 5" >> /var/lib/lxc/02-autostart-privileged/config
echo "lxc.group = high_priority" >> /var/lib/lxc/02-autostart-privileged/config
cat /var/lib/lxc/02-autostart-privileged/config
exit

sudo lxc-autostart --list # Notice that no containers showed

# This is because our container now belongs to an autostart group. Let's specify it:
sudo lxc-autostart --list --group high_priority

# Start all containers belonging to a given autostart group
sudo lxc-autostart --group high_priority
sudo lxc-ls --fancy

# Stop all containers belonging to a given autostart group
sudo lxc-autostart --group high_priority -s
sudo lxc-destroy -n 02-autostart-privileged
```

For lxc-autostart **to automatically start containers after a server reboot, it first
needs to be started.**


## LXC Lifecycle management hooks
Beginning with Ubuntu 12.10, it is possible to define hooks to be executed at specific points in a container’s lifetime:

Pre-start hooks are run in the host’s namespace before the container ttys, consoles, or mounts are up. If any mounts are done in this hook, they should be cleaned up in the post-stop hook.
Pre-mount hooks are run in the container’s namespaces, but before the root filesystem has been mounted. Mounts done in this hook will be automatically cleaned up when the container shuts down.
Mount hooks are run after the container filesystems have been mounted, but before the container has called pivot_root to change its root filesystem.
Start hooks are run immediately before executing the container’s init. Since these are executed after pivoting into the container’s filesystem, the command to be executed must be copied into the container’s filesystem.
Post-stop hooks are executed after the container has been shut down.
If any hook returns an error, the container’s run will be aborted. Any post-stop hook will still be executed. Any output generated by the script will be logged at the debug priority.

Please see the lxc.container.conf(5) manual page for the configuration file format with which to specify hooks. Some sample hooks are shipped with the lxc package to serve as an example of how to write and use such hooks.

## Freezing a running container

## Limiting container resource usage

## Cloning
For rapid provisioning, you may wish to customize a canonical container according to your needs and then make multiple copies of it. This can be done with the lxc-clone program.

Clones are either snapshots or copies of another container. A copy is a new container copied from the original, and takes as much space on the host as the original. A snapshot exploits the underlying backing store’s snapshotting ability to make a copy-on-write container referencing the first. Snapshots can be created from btrfs, LVM, zfs, and directory backed containers. Each backing store has its own peculiarities - for instance, LVM containers which are not thinpool-provisioned cannot support snapshots of snapshots; zfs containers with snapshots cannot be removed until all snapshots are released; LVM containers must be more carefully planned as the underlying filesystem may not support growing; btrfs does not suffer any of these shortcomings, but suffers from reduced fsync performance causing dpkg and apt to be slower.

Snapshots of directory-packed containers are created using the overlay filesystem. For instance, a privileged directory-backed container C1 will have its root filesystem under /var/lib/lxc/C1/rootfs. A snapshot clone of C1 called C2 will be started with C1’s rootfs mounted readonly under /var/lib/lxc/C2/delta0. Importantly, in this case C1 should not be allowed to run or be removed while C2 is running. It is advised instead to consider C1 a canonical base container, and to only use its snapshots.

Given an existing container called C1, a copy can be created using:

sudo lxc-clone -o C1 -n C2
A snapshot can be created using:

sudo lxc-clone -s -o C1 -n C2
See the lxc-clone manpage for more information.

## Copy

Cloning the container and its power off

Before we clone a container make sure to stop it using the command discussed above, then type the below command to make a clone of it. The name of our cloned container will be sample2.

Note: Earlier the command had lxc-clone instead of lxc-copy, lxc-clone is now deprecated.

sudo lxc-copy -n <old container> -N <new container>


## Snapshots
To more easily support the use of snapshot clones for iterative container development, LXC supports snapshots. When working on a container C1, before making a potentially dangerous or hard-to-revert change, you can create a snapshot

sudo lxc-snapshot -n C1
which is a snapshot-clone called ‘snap0’ under /var/lib/lxcsnaps or $HOME/.local/share/lxcsnaps. The next snapshot will be called ‘snap1’, etc. Existing snapshots can be listed using lxc-snapshot -L -n C1, and a snapshot can be restored - erasing the current C1 container - using lxc-snapshot -r snap1 -n C1. After the restore command, the snap1 snapshot continues to exist, and the previous C1 is erased and replaced with the snap1 snapshot.

Snapshots are supported for btrfs, lvm, zfs, and overlayfs containers. If lxc-snapshot is called on a directory-backed container, an error will be logged and the snapshot will be created as a copy-clone. The reason for this is that if the user creates an overlayfs snapshot of a directory-backed container and then makes changes to the directory-backed container, then the original container changes will be partially reflected in the snapshot. If snapshots of a directory backed container C1 are desired, then an overlayfs clone of C1 should be created, C1 should not be touched again, and the overlayfs clone can be edited and snapshotted at will, as such

lxc-clone -s -o C1 -n C2
lxc-start -n C2 -d # make some changes
lxc-stop -n C2
lxc-snapshot -n C2
lxc-start -n C2 # etc

## Ephemeral Containers
While snapshots are useful for longer-term incremental development of images, ephemeral containers utilize snapshots for quick, single-use throwaway containers. Given a base container C1, you can start an ephemeral container using

lxc-start-ephemeral -o C1
The container begins as a snapshot of C1. Instructions for logging into the container will be printed to the console. After shutdown, the ephemeral container will be destroyed. See the lxc-start-ephemeral manual page for more options.

## Update multiple containers
- https://www.cyberciti.biz/faq/how-to-update-debian-or-ubuntu-linux-containers-lxc/

## Consoles
-lxc-console

Containers have a configurable number of consoles. One always exists on the container’s /dev/console. This is shown on the terminal from which you ran lxc-start, unless the -d option is specified. The output on /dev/console can be redirected to a file using the -c console-file option to lxc-start. The number of extra consoles is specified by the lxc.tty variable, and is usually set to 4. Those consoles are shown on /dev/ttyN (for 1 <= N <= 4). To log into console 3 from the host, use:

sudo lxc-console -n container -t 3
or if the -t N option is not specified, an unused console will be automatically chosen. To exit the console, use the escape sequence Ctrl-a q. Note that the escape sequence does not work in the console resulting from lxc-start without the -d option.

Each container console is actually a Unix98 pty in the host’s (not the guest’s) pty mount, bind-mounted over the guest’s /dev/ttyN and /dev/console. Therefore, if the guest unmounts those or otherwise tries to access the actual character device 4:N, it will not be serving getty to the LXC consoles. (With the default settings, the container will not be able to access that character device and getty will therefore fail.) This can easily happen when a boot script blindly mounts a new /dev.

## Troubleshooting

Logging
If something goes wrong when starting a container, the first step should be to get full logging from LXC:

sudo lxc-start -n C1 -l trace -o debug.out
This will cause lxc to log at the most verbose level, trace, and to output log information to a file called ‘debug.out’. If the file debug.out already exists, the new log information will be appended.

Monitoring container status
Two commands are available to monitor container state changes. lxc-monitor monitors one or more containers for any state changes. It takes a container name as usual with the -n option, but in this case the container name can be a posix regular expression to allow monitoring desirable sets of containers. lxc-monitor continues running as it prints container changes. lxc-wait waits for a specific state change and then exits. For instance,

sudo lxc-monitor -n cont[0-5]*
would print all state changes to any containers matching the listed regular expression, whereas

sudo lxc-wait -n cont1 -s 'STOPPED|FROZEN'
will wait until container cont1 enters state STOPPED or state FROZEN and then exit.

Attach
As of Ubuntu 14.04, it is possible to attach to a container’s namespaces. The simplest case is to simply do

sudo lxc-attach -n C1
which will start a shell attached to C1’s namespaces, or, effectively inside the container. The attach functionality is very flexible, allowing attaching to a subset of the container’s namespaces and security context. See the manual page for more information.

Container init verbosity
If LXC completes the container startup, but the container init fails to complete (for instance, no login prompt is shown), it can be useful to request additional verbosity from the init process. For an upstart container, this might be:

sudo lxc-start -n C1 /sbin/init loglevel=debug
You can also start an entirely different program in place of init, for instance

sudo lxc-start -n C1 /bin/bash
sudo lxc-start -n C1 /bin/sleep 100
sudo lxc-start -n C1 /bin/cat /proc/1/status


# Security
- [Introduction to security](https://linuxcontainers.org/lxc/security/)
- https://linuxcontainers.org/lxc/security/#cgroup-limits
- https://documentation.ubuntu.com/lxd/en/latest/explanation/projects/
- https://documentation.ubuntu.com/lxd/en/latest/explanation/security/

Apparmor
LXC ships with a default Apparmor profile intended to protect the host from accidental misuses of privilege inside the container. For instance, the container will not be able to write to /proc/sysrq-trigger or to most /sys files.

The usr.bin.lxc-start profile is entered by running lxc-start. This profile mainly prevents lxc-start from mounting new filesystems outside of the container’s root filesystem. Before executing the container’s init, LXC requests a switch to the container’s profile. By default, this profile is the lxc-container-default policy which is defined in /etc/apparmor.d/lxc/lxc-default. This profile prevents the container from accessing many dangerous paths, and from mounting most filesystems.

Programs in a container cannot be further confined - for instance, MySQL runs under the container profile (protecting the host) but will not be able to enter the MySQL profile (to protect the container).

lxc-execute does not enter an Apparmor profile, but the container it spawns will be confined.

Customizing container policies
If you find that lxc-start is failing due to a legitimate access which is being denied by its Apparmor policy, you can disable the lxc-start profile by doing:

sudo apparmor_parser -R /etc/apparmor.d/usr.bin.lxc-start
sudo ln -s /etc/apparmor.d/usr.bin.lxc-start /etc/apparmor.d/disabled/
This will make lxc-start run unconfined, but continue to confine the container itself. If you also wish to disable confinement of the container, then in addition to disabling the usr.bin.lxc-start profile, you must add:

lxc.aa_profile = unconfined
to the container’s configuration file.

LXC ships with a few alternate policies for containers. If you wish to run containers inside containers (nesting), then you can use the lxc-container-default-with-nesting profile by adding the following line to the container configuration file

lxc.aa_profile = lxc-container-default-with-nesting
If you wish to use libvirt inside containers, then you will need to edit that policy (which is defined in /etc/apparmor.d/lxc/lxc-default-with-nesting) by uncommenting the following line:

mount fstype=cgroup -> /sys/fs/cgroup/**,
and re-load the policy.

Note that the nesting policy with privileged containers is far less safe than the default policy, as it allows containers to re-mount /sys and /proc in nonstandard locations, bypassing apparmor protections. Unprivileged containers do not have this drawback since the container root cannot write to root-owned proc and sys files.

Another profile shipped with lxc allows containers to mount block filesystem types like ext4. This can be useful in some cases like maas provisioning, but is deemed generally unsafe since the superblock handlers in the kernel have not been audited for safe handling of untrusted input.

If you need to run a container in a custom profile, you can create a new profile under /etc/apparmor.d/lxc/. Its name must start with lxc- in order for lxc-start to be allowed to transition to that profile. The lxc-default profile includes the re-usable abstractions file /etc/apparmor.d/abstractions/lxc/container-base. An easy way to start a new profile therefore is to do the same, then add extra permissions at the bottom of your policy.

After creating the policy, load it using:

sudo apparmor_parser -r /etc/apparmor.d/lxc-containers
The profile will automatically be loaded after a reboot, because it is sourced by the file /etc/apparmor.d/lxc-containers. Finally, to make container CN use this new lxc-CN-profile, add the following line to its configuration file:

lxc.aa_profile = lxc-CN-profile
Control Groups
Control groups (cgroups) are a kernel feature providing hierarchical task grouping and per-cgroup resource accounting and limits. They are used in containers to limit block and character device access and to freeze (suspend) containers. They can be further used to limit memory use and block i/o, guarantee minimum cpu shares, and to lock containers to specific cpus.

By default, a privileged container CN will be assigned to a cgroup called /lxc/CN. In the case of name conflicts (which can occur when using custom lxcpaths) a suffix “-n”, where n is an integer starting at 0, will be appended to the cgroup name.

By default, a privileged container CN will be assigned to a cgroup called CN under the cgroup of the task which started the container, for instance /usr/1000.user/1.session/CN. The container root will be given group ownership of the directory (but not all files) so that it is allowed to create new child cgroups.

As of Ubuntu 14.04, LXC uses the cgroup manager (cgmanager) to administer cgroups. The cgroup manager receives D-Bus requests over the Unix socket /sys/fs/cgroup/cgmanager/sock. To facilitate safe nested containers, the line

lxc.mount.auto = cgroup
can be added to the container configuration causing the /sys/fs/cgroup/cgmanager directory to be bind-mounted into the container. The container in turn should start the cgroup management proxy (done by default if the cgmanager package is installed in the container) which will move the /sys/fs/cgroup/cgmanager directory to /sys/fs/cgroup/cgmanager.lower, then start listening for requests to proxy on its own socket /sys/fs/cgroup/cgmanager/sock. The host cgmanager will ensure that nested containers cannot escape their assigned cgroups or make requests for which they are not authorized.

### Security
A namespace maps ids to resources. By not providing a container any id with which to reference a resource, the resource can be protected. This is the basis of some of the security afforded to container users. For instance, IPC namespaces are completely isolated. Other namespaces, however, have various leaks which allow privilege to be inappropriately exerted from a container into another container or to the host.

By default, LXC containers are started under a Apparmor policy to restrict some actions. The details of AppArmor integration with lxc are in section Apparmor. Unprivileged containers go further by mapping root in the container to an unprivileged host UID. This prevents access to /proc and /sys files representing host resources, as well as any other files owned by root on the host.

Exploitable system calls
It is a core container feature that containers share a kernel with the host. Therefore if the kernel contains any exploitable system calls the container can exploit these as well. Once the container controls the kernel it can fully control any resource known to the host.

In general to run a full distribution container a large number of system calls will be needed. However for application containers it may be possible to reduce the number of available system calls to only a few. Even for system containers running a full distribution security gains may be had, for instance by removing the 32-bit compatibility system calls in a 64-bit container. See the lxc.container.conf manual page for details of how to configure a container to use seccomp. By default, no seccomp policy is loaded.


## LXC web panel
- [LXC Web Panel](https://lxc-webpanel.github.io/install.html)
- [LXC-Web-Panel](https://github.com/lxc-webpanel/LXC-Web-Panel)

> The project is no longer maintained and is deprecated. Supported for LXC 0.7 to 0.9. You can use LXD UI instead.

Some people find working with the command line a bit tedious, this method is just for them. By installing the web panel of LXC one can manage the containers with the help of GUI. Note: For installing the web panel you must be a root user.

```bash
sudo su
wget http://lxc-webpanel.github.io/tools/install.sh -O - | bash
```

The user interface can be accessed at the  Url: `http:/your_ip_address:5000/` by using the user id and password which by default are admin and admin.