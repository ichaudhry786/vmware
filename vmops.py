#!/usr/bin/python
"""A script which demonstrates how to clone a VM.
Usage:
    clone_vm.py <source_vm_name> <dest_vm_name>
e.g.
    clone_vm test test_clone

"""

import sys
import time

from psphere.client import Client
from psphere.soap import VimFault
from psphere.managedobjects import VirtualMachine
from psphere.errors import ObjectNotFoundError

source_vm_name = "Chef Node"
dest_vm_name = "Chef Node Clone"

client = Client("69.33.0.216","vpxuser","Tubuai123!")

try:
    vm = VirtualMachine.get(client, name=dest_vm_name)
    if vm.name == dest_vm_name:
        print("ERROR: Destination VM \"%s\" already exists." % dest_vm_name)
        client.logout()
        sys.exit(1)
except ObjectNotFoundError:
    pass

try:
    vm = VirtualMachine.get(client, name=source_vm_name)
except ObjectNotFoundError:
    print("ERROR: No VM with name \"%s\" to clone" % source_vm_name)

name = dest_vm_name
folder = vm.parent # Datacenter folder
vm_clone_spec = client.create("VirtualMachineCloneSpec")
vm_reloc_spec = client.create("VirtualMachineRelocateSpec")
vm_reloc_spec.datastore = vm.datastore
vm_reloc_spec.host = None
vm_reloc_spec.transform = None
vm_reloc_spec.pool = vm.resourcePool
vm_clone_spec.powerOn = True
vm_clone_spec.template = False
vm_clone_spec.location = vm_reloc_spec
vm_clone_spec.snapshot = None

try:
    task = vm.CloneVM_Task(folder=folder, name=name, spec=vm_clone_spec)
except VimFault, e:
    print("Failed to clone %s: " % e)
    sys.exit()

while task.info.state in ["queued", "running"]:
    print("Waiting 5 more seconds for VM creation")
    time.sleep(5)
    task.update()

if task.info.state == "success":
    elapsed_time = task.info.completeTime - task.info.startTime
    print("Successfully cloned VM %s from %s. Server took %s seconds." %
          (dest_vm_name, source_vm_name, elapsed_time.seconds))
elif task.info.state == "error":
    print("ERROR: The task for cloning the VM has finished with"
          " an error. If an error was reported it will follow.")
    try:
        print("ERROR: %s" % task.info.error.localizedMessage)
    except AttributeError:
        print("ERROR: There is no error message available.")
else:
    print("UNKNOWN: The task reports an unknown state %s" %
          task.info.state)

# All done
client.logout()