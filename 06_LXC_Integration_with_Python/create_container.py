import sys
import time

import lxc


def create_container(
    name: str,
    template_data: dict = {"dist": "ubuntu", "release": "jammy", "arch": "amd64"},
) -> None:
    """Create a container."""
    # Setup the container object
    c = lxc.Container(name)
    if c.defined:
        print("Container already exists", file=sys.stderr)
        sys.exit(1)

    # Create the container rootfs
    if not c.create(
        "download",
        lxc.LXC_CREATE_QUIET,
        template_data,
    ):
        print("Failed to create the container rootfs", file=sys.stderr)
        sys.exit(1)

    # Start the container
    if not c.start():
        print("Failed to start the container", file=sys.stderr)
        sys.exit(1)

    # Wait for the container to start
    time.sleep(5)

    if c.running:
        print("Container is started and running successfully.")


if __name__ == "__main__":
    container_name = input("Enter the container name: ")
    create_container(container_name)
