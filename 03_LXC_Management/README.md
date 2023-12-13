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

Two other useful autostart configuration parameters are adding a delay to the start, and defining a group in which multiple containers can start as a single unit.
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


## Freezing a running container
LXC takes advantage of the freezer cgroup to freeze all the processes running inside a container. The processes will be in a blocked state until thawed. Freezing a container can be useful in cases where the system load is high and you want to free some resources without actually stopping the container and preserving its running state.

That very simply freezes all the processes in the container so they won’t get any time allocated by the scheduler. However **the processes will still exist and will still use whatever memory they used to**.
```bash
# Create a container:
sudo lxc-create -t download \
  -n container-test -- \
  --dist debian \
  --release bookworm \
  --arch amd64

# Start the container:
sudo lxc-start -n container-test
sudo lxc-ls --fancy

# Run in second terminal:
sudo lxc-monitor --name container-test

# Freeze the container:
sudo lxc-freeze -n container-test
sudo lxc-ls --fancy

# Unfreeze the container:
sudo lxc-unfreeze --name container-test
sudo lxc-ls --fancy
```

## LXC Lifecycle management hooks
- [Man pages: CONTAINER HOOKS](https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=ids%20to%20map.-,CONTAINER%20HOOKS,-Container%20hooks%20are)

LXC provides a convenient way to execute programs during the life cycle of containers. The following table summarizes the various configuration options available to allow this feature:

| Option      | Description |
| ----------- | ----------- |
| `lxc.hook.pre-start`     | A hook to be run in the host namespace before the container ttys, consoles, or mounts are loaded. If any mounts are done in this hook, they should be cleaned up in the post-stop hook.       |
| `lxc.hook.pre-mount`   | A hook to be run in the container's filesystem namespace, but before the rootfs has been set up. Mounts done in this hook will be automatically cleaned up when the container shuts down.       |
| `lxc.hook.mount`   | A hook to be run in the container after mounting has been done, but before the pivot_root.      |
| `lxc.hook.autodev`   | A hook to be run in the container after mounting has been done and after any mount hooks have run, but before the pivot_root       |
| `lxc.hook.start`   | A hook to be run in the container right before executing the container's init      |
| `lxc.hook.stop`   | A hook to be run in the host's namespace after the container has been shut down      |
| `lxc.hook.post-stop`   | A hook to be run in the host's namespace after the container has been shut down      |
| `lxc.hook.clone`   | A hook to be run when the container is cloned       |
| `lxc.hook.destroy`   | A hook to be run when the container is destroyed       |


If any hook returns an error, the container’s run will be aborted. Any post-stop hook will still be executed. Any output generated by the script will be logged at the debug priority.

Let's create a new container and write a simple script that will output
the values of four LXC variables to a file, when the container starts:
```bash
# Check if the container exists:
sudo lxc-ls --fancy
# Stop the container:
sudo lxc-stop -n container-test

# add the lxc.hook.pre-start option to its configuration file:
sudo su
echo "lxc.hook.pre-start = /var/lib/lxc/container-test/pre_start.sh" >> /var/lib/lxc/container-test/config
cat /var/lib/lxc/container-test/config
# create a simple bash script and make it executable:
nano /var/lib/lxc/container-test/pre_start.sh

# add
#!/bin/bash
LOG_FILE=/tmp/container.log
echo "Container name: $LXC_NAME" | tee -a $LOG_FILE
echo "Container mounted rootfs: $LXC_ROOTFS_MOUNT" | tee -a $LOG_FILE
echo "Container config file $LXC_CONFIG_FILE" | tee -a $LOG_FILE
echo "Container rootfs: $LXC_ROOTFS_PATH" | tee -a $LOG_FILE

chmod u+x /var/lib/lxc/container-test/pre_start.sh
exit

# Start the container:
sudo lxc-start -n container-test
sudo lxc-ls --fancy

# check the contents of the file that the bash script should have written to
cat /tmp/container.log

# Stop and destroy the container:
sudo lxc-stop -n container-test
sudo lxc-destroy -n container-test
```


## Limiting container resource usage

LXC comes with tools to limit container resources. The container must be started with the `lxc-start` command for the limits to be applied.

```bash
# Create a container:
sudo lxc-create -t download \
  -n container-test -- \
  --dist debian \
  --release bookworm \
  --arch amd64

sudo lxc-start -n container-test
sudo lxc-ls --fancy

# set up the available memory for a container to 512 MB
sudo lxc-cgroup -n container-test memory.limit_in_bytes 536870912

# check the memory limit:
sudo lxc-attach --name container-test -- free -h

# Changing the value only requires running the same command again. 
# Let's change the available memory to 256 MB
sudo lxc-cgroup -n container-test memory.limit_in_bytes 268435456

# check the memory limit:
sudo lxc-attach --name container-test -- free -h

# We can also pin a CPU core to a container
sudo lxc-attach --name container-test -- cat /proc/cpuinfo | grep processor

# Check the number of cores available on the host:
cat /proc/cpuinfo | grep processor

# Pin the container to the second core:
sudo lxc-cgroup -n container-test cpuset.cpus 1
sudo lxc-attach --name container-test -- cat /proc/cpuinfo | grep processor
```

To make changes to persist server reboots, we need to add them to the configuration file of the container:
- `echo "lxc.cgroup.memory.limit_in_bytes = 536870912" | sudo tee -a  /var/lib/lxc/container-test/config`

Setting various other cgroup parameters is done in a similar way.

Stop and destroy the container:
```bash
sudo lxc-stop -n container-test
sudo lxc-destroy -n container-test
```

## Troubleshooting
If something goes wrong when starting a container, the first step should be to get full logging from LXC:

```bash
sudo lxc-create -t download \
  -n container-test-3 -- \
  --dist debian \
  --release bookworm \
  --arch amd64

sudo lxc-start -n container-test-3 -l debug -o debug.out
sudo lxc-ls --fancy

sudo cat debug.out

sudo lxc-stop -n container-test-3
sudo lxc-destroy -n container-test-3
sudo rm debug.out
```

This will cause lxc to log at the debug verbose level and to output log information to a file called `debug.out`. If the file debug.out already exists, the new log information will be appended.


# Security
- https://stgraber.org/2014/01/01/lxc-1-0-security-features/
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

## Running foreign architectures
By default LXC will only let you run containers of one of the architectures supported by the host. That makes sense since after all, your CPU doesn’t know what to do with anything else.

Except that we have this convenient package called “qemu-user-static” which contains a whole bunch of emulators for quite a few interesting architectures. The most common and useful of those is qemu-arm-static which will let you run most armv7 binaries directly on x86.

The “ubuntu” template knows how to make use of qemu-user-static, so you can simply check that you have the “qemu-user-static” package installed, then run:

sudo lxc-create -t ubuntu -n p3 -- -a armhf
After a rather long bootstrap, you’ll get a new p3 container which will be mostly running Ubuntu armhf. I’m saying mostly because the qemu emulation comes with a few limitations, the biggest of which is that any piece of software using the ptrace() syscall will fail and so will anything using netlink. As a result, LXC will install the host architecture version of upstart and a few of the networking tools so that the containers can boot properly.

stgraber@castiana:~$ file /bin/ls
/bin/ls: ELF 64-bit LSB  executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, """BuildID[sha1]""" =e50e0a5dadb8a7f4eaa2fd715cacb9842e157dc7, stripped
stgraber@castiana:~$ sudo lxc-start -n p3 -d
stgraber@castiana:~$ sudo lxc-attach -n p3
root@p3:/# file /bin/ls
/bin/ls: ELF 32-bit LSB  executable, ARM, EABI5 version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, """BuildID[sha1]""" =88ff013a8fd9389747fb1fea1c898547fb0f650a, stripped
root@p3:/# exit
stgraber@castiana:~$ sudo lxc-stop -n p3
stgraber@castiana:~$


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