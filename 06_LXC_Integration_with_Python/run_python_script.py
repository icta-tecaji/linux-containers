import sys

import lxc

conainer_name = input("Enter the name of the container to run the function on: ")


c = lxc.Container(conainer_name)
if not c.running:
    c.start()


def print_hostname():
    with open("/etc/hostname") as fd:
        print("Hostname: %s" % fd.read().strip())


# First run on the host
print_hostname()

# Then on the container
c.attach_wait(print_hostname)

if not c.shutdown(30):
    c.stop()

# Destroy the container
if not c.destroy():
    print(f"Failed to destroy the container: {c.name}", file=sys.stderr)
    sys.exit(1)
