# LXC Storage

## Attaching directories from the host OS
- [LXC manpages: MOUNT POINTS](https://linuxcontainers.org/lxc/manpages//man5/lxc.container.conf.5.html#:~:text=value%20is%20used.-,MOUNT%20POINTS,-The%20mount%20points)


The root filesystem of LXC containers is visible from the host OS as a regular directory tree. We can directly manipulate files in a running container by just making changes in that directory. LXC also allows for **attaching directories from the host OS inside the container using bind mount**.

A bind mount is a different view of the directory tree. It achieves this by replicating the existing directory tree under a different mount point.

Let's create a new container, directory, and a file on the host:
```bash
mkdir /tmp/export_to_container

hostname -f > /tmp/export_to_container/file

sudo lxc-create -t download \
  -n mount_container -- \
  --dist ubuntu \
  --release jammy \
  --arch amd64
```

Use the `lxc.mount.entry` option in the configuration file of the container, telling LXC what directory to bind mount from the host, and the mount point inside the container to bind to:
- `echo "lxc.mount.entry = /tmp/export_to_container/ /var/lib/lxc/mount_container/rootfs/mnt none ro,bind 0 0" | sudo tee -a /var/lib/lxc/mount_container/config`
- `sudo cat /var/lib/lxc/mount_container/config`

Once the container is started, we can see that the `/mnt` inside it now contains the file that we created in the `/tmp/export_to_container` directory on the host OS earlier:
- `sudo lxc-start -n mount_container`
- `sudo lxc-ls -f`
- `sudo lxc-attach -n mount_container`
- `cat /mnt/file`
- `ls -l /mnt`
- `exit`

> When an LXC container is in a running state, some files are only visible from `/proc` on the host OS. In order to make persistent changes in the root filesystem of a container, modify the files in `/var/lib/lxc/mount_container/rootfs/` instead.

## Backing Stores
- [Backing Stores](https://ubuntu.com/server/docs/containers-lxc#:~:text=autostart%20a%20container.-,Backing%20Stores,-LXC%20supports%20several)
- [Storage backingstores](https://stgraber.org/2013/12/27/lxc-1-0-container-storage/)

LXC supports several backing stores (default dir type, LVM, Btrfs, and ZFS) for container root filesystems. The default is a **simple directory backing store**, because it requires no prior host customization, so long as the underlying filesystem is large enough. It also requires **no root privilege to create** the backing store, so that it is seamless for unprivileged use. 
- The rootfs for a privileged directory backed container is located (by default) under `/var/lib/lxc/C1/rootfs`, while the rootfs for an unprivileged container is under `~/.local/share/lxc/C1/rootfs` (C1 is the name of the container).

Using the default store might be sufficient in some cases, however, to take advantage of more advanced features, such as container snapshots and backups, other types are available.

Clones are either snapshots or copies of another container. 
- A **copy** is a new container copied from the original, and takes as much space on the host as the original. 
- A **snapshot** exploits the underlying backing store’s snapshotting ability to make a copy-on-write container referencing the first. Snapshots can be created from btrfs, LVM, zfs, and directory backed containers. 


## Creating container backup using lxc-copy
- [Manpages: lxc-copy](https://linuxcontainers.org/lxc/manpages//man1/lxc-copy.1.html)

Regardless of the backend store of the container, we can use the `lxc-copy` utility to create a full copy of the LXC instance.

> `lxc-clone` has been deprecated, and replaced by `lxc-copy`.

Before we copy a container make sure to stop it.

Specify the name of the container on the original host we want to back up, and a name for the copy:
- `sudo lxc-stop -n mount_container`
- `sudo lxc-ls -f`
- `sudo lxc-copy --name mount_container --newname mount_container_backup`
- `sudo ls /var/lib/lxc`

Creating a full copy will update the configuration file of the new container with the newly specified name and location of the rootfs:
- `sudo cat /var/lib/lxc/mount_container_backup/config`


## Snapshots
To more easily support the use of snapshot clones for iterative container development, LXC supports snapshots. When working on a container C1, before making a potentially dangerous or hard-to-revert change, you can create a snapshot.
```bash
# Start the container
sudo lxc-start -n mount_container

sudo lxc-ls -f

# Associate the comment in comment_file with the newly created snapshot.
echo "before installing NGINX" > snap-comment
# Create a snapshot of the container.
sudo lxc-snapshot -n mount_container -c snap-comment
# Snapshot fails because the container is running.
sudo lxc-snapshot -n mount_container -L -C
sudo lxc-stop -n mount_container

# Create a snapshot of the container.
sudo lxc-snapshot -n mount_container -c snap-comment
# Check the snapshot.
sudo lxc-snapshot -n mount_container -L -C

# Start the container and install NGINX.
sudo lxc-start -n mount_container
sudo lxc-attach -n mount_container
apt update
apt install nginx
apt list --installed | grep nginx
exit

# Revert the container:
sudo lxc-stop -n mount_container
sudo lxc-snapshot -n mount_container -r snap0

# Start the container and check that NGINX is not installed.
sudo lxc-start -n mount_container
sudo lxc-attach -n mount_container
apt update
apt list --installed | grep nginx
exit

# Or if you want to restore a snapshot as its own container, you can use:
sudo lxc-stop -n mount_container
sudo lxc-ls -f
sudo lxc-snapshot -n mount_container -r snap0 -N mount_container_no_nginx
sudo lxc-ls -f

# Delete the snapshot.
sudo lxc-snapshot -n mount_container -d snap0

# Stop and remove all containers.
sudo lxc-destroy -n mount_container
sudo lxc-destroy -n mount_container_no_nginx
sudo lxc-destroy -n mount_container_backup
sudo lxc-ls -f
```

## Passing devices to a running container
- [Manpages: lxc-device](https://linuxcontainers.org/lxc/manpages//man1/lxc-device.1.html)

By default LXC will prevent any access using the devices cgroup as a filtering mechanism. You could edit the container configuration to allow the right additional devices and then restart the container.

But for one-off things, there’s also a very convenient tool called `lxc-device`. With it, you can simply do:
- `sudo lxc-device add -n p1 /dev/ttyUSB0 /dev/ttyS0`

The same tool also allows moving network devices from the host to within the container.


## Using the LVM backing store

## Using the Btrfs backing store

## Using the ZFS backing store

## Ephemeral Containers
