
## LXC - Running foreign architectures
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
