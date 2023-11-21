- https://documentation.ubuntu.com/lxd/en/latest/explanation/storage/

- https://stgraber.org/2016/03/15/lxd-2-0-installing-and-configuring-lxd-212/ - Storage backends



Or with a bigger disk:

lxc launch ubuntu:22.04 ubuntu-vm-big --vm --device root,size=30GiB