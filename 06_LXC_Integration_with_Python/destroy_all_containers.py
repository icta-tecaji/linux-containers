import sys

import lxc

for container in lxc.list_containers(as_object=True):
    if container.running:
        # Stop the container
        if not container.stop():
            print(f"Failed to stop the container: {container.name}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Stopped the container: {container.name}")

    # Destroy the container
    if not container.destroy():
        print(f"Failed to destroy the container: {container.name}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Destroyed the container: {container.name}")

    print("-------------------------------------")
