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


## Security
- [Introduction to security](https://linuxcontainers.org/lxc/security/)
- [Security features](https://stgraber.org/2014/01/01/lxc-1-0-security-features/)
- [Potential DoS attacks](https://linuxcontainers.org/lxc/security/#potential-dos-attacks)

### Potential DoS attacks
LXC doesn't pretend to prevent DoS attacks by default. When running multiple untrusted containers or when allowing untrusted users to run containers, one should keep a few things in mind and update their configuration accordingly:
- **Cgroup limits**:
  - LXC inherits cgroup limits from its parent. As a result, a user in a container can reasonably easily DoS the host by running a fork bomb, by using all the system's memory or creating network interfaces until the kernel runs out of memory.
  - This can be mitigated by either setting the relevant lxc.cgroup configuration entries (memory, cpu and pids) or by making sure that the parent user is placed in appropriately configured cgroups at login time.
  - As with cgroups, the parent's limit is inherited so unprivileged containers cannot have ulimits set to values higher than their parent.
- **Shared network bridges**:
  - LXC sets up basic level 2 connectivity for its containers. As a convenience it also provides one default bridge on the system.
  - As a container connected to a bridge can transmit any level 2 traffic that it wishes, it can effectively do MAC or IP spoofing on the bridge.
  - When running untrusted containers or when allowing untrusted users to run containers, one should ideally create one bridge per user or per group of untrusted containers and configure `/etc/lxc/lxc-usernet` such that users may only use the bridges that they have been allocated.
- **Kernel**:
  - It is a core container feature that containers share a kernel with the host. Therefore if the kernel contains any exploitable system calls the container can exploit these as well. 
  - Once the container controls the kernel it can fully control any resource known to the host.

### Security features

By default, LXC containers are started under a Apparmor policy to restrict some actions. The details of AppArmor integration with lxc are in section Apparmor. Unprivileged containers go further by mapping root in the container to an unprivileged host UID. This prevents access to `/proc` and `/sys` files representing host resources, as well as any other files owned by root on the host.


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
