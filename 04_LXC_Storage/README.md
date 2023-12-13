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

