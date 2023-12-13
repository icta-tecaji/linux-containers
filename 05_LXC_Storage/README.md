# LXC Storage

- https://ubuntu.com/server/docs/containers-lxc -> Backing Stores

- https://stgraber.org/2013/12/27/lxc-1-0-container-storage/

## Passing devices to a running container
It’s great being able to enter and leave the container at will, but what about accessing some random devices on your host?

By default LXC will prevent any such access using the devices cgroup as a filtering mechanism. You could edit the container configuration to allow the right additional devices and then restart the container.

But for one-off things, there’s also a very convenient tool called “lxc-device”.
With it, you can simply do:

`sudo lxc-device add -n p1 /dev/ttyUSB0 /dev/ttyS0`

Which will add (mknod) /dev/ttyS0 in the container with the same type/major/minor as /dev/ttyUSB0 and then add the matching cgroup entry allowing access from the container.

The same tool also allows moving network devices from the host to within the container.


## Attaching directories from the host OS and exploring the running filesystem of a container
- LXC knjiga stran 97

## Attaching directories from the host OS

Exchanging data with a container
Because containers directly share their filesystem with the host, there’s a lot of things that can be done to pass data into a container or to get stuff out.

The first obvious one is that you can access the container’s root at:
/var/lib/lxc/<container name>/rootfs/

That’s great, but sometimes you need to access data that’s in the container and on a filesystem which was mounted by the container itself (such as a tmpfs). In those cases, you can use this trick:

sudo ls -lh /proc/$(sudo lxc-info -n p1 -p -H)/root/run/
Which will show you what’s in /run of the running container “p1”.

Now, that’s great to have access from the host to the container, but what about having the container access and write data to the host?
Well, let’s say we want to have our host’s /var/cache/lxc shared with “p1”, we can edit /var/lib/lxc/p1/fstab and append:

/var/cache/lxc var/cache/lxc none bind,create=dir
This line means, mount “/var/cache/lxc” from the host as “/var/cache/lxc” (the lack of initial / makes it relative to the container’s root), mount it as a bind-mount (“none” fstype and “bind” option) and create any directory that’s missing in the container (“create=dir”).

Now restart “p1” and you’ll see /var/cache/lxc in there, showing the same thing as you have on the host. Note that if you want the container to only be able to read the data, you can simply add “ro” as a mount flag in the fstab.

## Using the LVM backing store

## Using the Btrfs backing store

## Using the ZFS backing store


## Cloning
For rapid provisioning, you may wish to customize a canonical container according to your needs and then make multiple copies of it. This can be done with the `lxc-clone` program.

Clones are either snapshots or copies of another container. 
- A **copy** is a new container copied from the original, and takes as much space on the host as the original. 
- A **snapshot** exploits the underlying backing store’s snapshotting ability to make a copy-on-write container referencing the first. Snapshots can be created from btrfs, LVM, zfs, and directory backed containers. 


Each backing store has its own peculiarities - for instance, LVM containers which are not thinpool-provisioned cannot support snapshots of snapshots; zfs containers with snapshots cannot be removed until all snapshots are released; LVM containers must be more carefully planned as the underlying filesystem may not support growing; btrfs does not suffer any of these shortcomings, but suffers from reduced fsync performance causing dpkg and apt to be slower.

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