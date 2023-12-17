# LXD Storage Operations and Imaging

Snapshots, mounts, add device lxc config device add c1 opt disk source=/opt path=opt


- https://documentation.ubuntu.com/lxd/en/latest/explanation/storage/

- https://stgraber.org/2016/03/15/lxd-2-0-installing-and-configuring-lxd-212/ - Storage backends

distrobuilder
copy
export
publish
restore

For instance, to mount /opt in container at /opt, you could add a disk device:
- `lxc config device add <container_name> opt disk source=/opt path=opt`


Or with a bigger disk:

lxc launch ubuntu:22.04 ubuntu-vm-big --vm --device root,size=30GiB

## Mounting storage volumes
- [Mount a file system from the instance](https://documentation.ubuntu.com/lxd/en/latest/howto/instances_access_files/#mount-a-file-system-from-the-instance)


## ZFS
If you opted for ZFS backing store (even on loop device) you may install zfs utilities and then investigate the created zpool and volumes.
```bash
sudo apt install zfsutils-linux
sudo zpool list
sudo zfs list
```

file-backed zpool will be created automatically. With ZFS, launching a new container is fast because the filesystem starts as a copy on write clone of the images’ filesystem. Note that unless the container is privileged (see below) LXD will need to change ownership of all files before the container can start, however this is fast and change very little of the actual filesystem data.

The other supported backing stores are described in detail in the Storage configuration section of the LXD documentation.

https://documentation.ubuntu.com/lxd/en/latest/explanation/storage/

## Create, manage and export images

When working with images, you can inspect various information about the available images, view and edit their properties and [configure aliases to refer to specific images](https://documentation.ubuntu.com/lxd/en/latest/howto/images_manage/#configure-image-aliases). You can also export an image to a file, which can be useful to copy or import it on another machine.

# backup, copy

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


## Snapshots

Containers can be renamed and live-migrated using the lxc move command:

lxc move c1 final-beta
They can also be snapshotted:

lxc snapshot c1 YYYY-MM-DD
Later changes to c1 can then be reverted by restoring the snapshot:

lxc restore u1 YYYY-MM-DD
New containers can also be created by copying a container or snapshot:

lxc copy u1/YYYY-MM-DD testcontainer

## Publishing images

When a container or container snapshot is ready for consumption by others, it can be published as a new image using;

lxc publish u1/YYYY-MM-DD --alias foo-2.0
The published image will be private by default, meaning that LXD will not allow clients without a trusted certificate to see them. If the image is safe for public viewing (i.e. contains no private information), then the ‘public’ flag can be set, either at publish time using

lxc publish u1/YYYY-MM-DD --alias foo-2.0 public=true
or after the fact using

lxc image edit foo-2.0
and changing the value of the public field.

## Image export and import

Image can be exported as, and imported from, tarballs:

lxc image export foo-2.0 foo-2.0.tar.gz
lxc image import foo-2.0.tar.gz --alias foo-2.0 --public
