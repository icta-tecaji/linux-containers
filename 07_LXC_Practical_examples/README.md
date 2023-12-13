# LXC Practical examples

- OpenWRT
- Running Docker in LXD


## Update multiple containers
- https://www.cyberciti.biz/faq/how-to-update-debian-or-ubuntu-linux-containers-lxc/

sudo lxc-create -t download \
  -n container-test-2 -- \
  --dist debian \
  --release bookworm \
  --arch amd64

sudo lxc-start -n container-test-2
sudo lxc-ls --fancy
