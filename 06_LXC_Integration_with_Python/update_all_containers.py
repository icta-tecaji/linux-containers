import lxc

for container in lxc.list_containers(as_object=True):
    print("Updating container %s" % container.name)
    # Start the container (if not started)
    started = False
    if not container.running:
        if not container.start():
            continue
        print("> Started container %s for update" % container.name)
        started = True

    if container.state != "RUNNING":
        continue

    # Wait for connectivity
    if not container.get_ips(timeout=30):
        continue

    # Run the updates
    container.attach_wait(lxc.attach_run_command, ["apt", "update"])
    container.attach_wait(lxc.attach_run_command, ["apt", "upgrade", "-y"])

    # Shutdown the container
    if started and not container.shutdown(30):
        container.stop()

    print("Done updating container %s" % container.name)
    print("-------------------------------------")
