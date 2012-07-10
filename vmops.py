#!/usr/bin/python
"""A script which demonstrates how to clone a VM.
Usage:
    clone_vm.py <source_vm_name> <dest_vm_name>
e.g.
    clone_vm test test_clone

"""

import sys
import time

from psphere.errors import ObjectNotFoundError
from psphere.client import Client
from psphere.soap import VimFault
from psphere.managedobjects import VirtualMachine
from pysphere import VIServer


class Vmops:
 client=None
 def connect(self,server_name,userid, password):
    self.client=Client(server_name,userid,password)


 def cloneMachine(self,source_vm_name, dest_vm_name):

    try:
        vm = VirtualMachine.get(self.client, name=source_vm_name)
        #f vm.name == dest_vm_name:
         #   print("ERROR: Destination VM \"%s\" already exists." % dest_vm_name)
          #  client.logout()
          #  sys.exit(1)
        #vm.parent # Datacenter folder

        vm_clone_spec = self.client.create("VirtualMachineCloneSpec")
        vm_reloc_spec = self.client.create("VirtualMachineRelocateSpec")
        vm_reloc_spec.datastore = vm.datastore
        vm_reloc_spec.host = None
        vm_reloc_spec.transform = None


        vm_reloc_spec.pool = vm.resourcePool

        vm_clone_spec.powerOn = True
        vm_clone_spec.template = False
        vm_clone_spec.location = vm_reloc_spec
        vm_clone_spec.snapshot = None


        task = vm.CloneVM_Task(folder=vm.parent, name=dest_vm_name, spec=vm_clone_spec)

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
    except ObjectNotFoundError:
        print("ERROR: No VM with name \"%s\" to clone" % source_vm_name)
    except VimFault, e:
        print("Failed to clone %s: " % e)
        sys.exit()



 def changevmConfig(self,vm_name,cpuCount):
    try:
     new_config = self.client.create("VirtualMachineConfigSpec")
     new_config.numCPUs = cpuCount
     new_config.cpuHotAddEnabled=True
     vm = VirtualMachine.get(self.client, name=vm_name)
     print("Reconfiguring %s" % vm_name)
     if vm.config.hardware.numCPU == cpuCount:
        print("Not reconfiguring %s as it already has 2 CPUs" % vm_name)
        sys.exit()
     task = vm.ReconfigVM_Task(spec=new_config)
     while task.info.state in ["queued", "running"]:
      print("Waiting 5 more seconds for VM creation")
      time.sleep(5)
      task.update()

     if task.info.state == "success":
      elapsed_time = task.info.completeTime - task.info.startTime
      print("Successfully reconfigured VM %s. Server took %s seconds." %
          (vm_name, elapsed_time.seconds))
     elif task.info.state == "error":
      print("ERROR: The task for reconfiguring the VM has finished with"
          " an error. If an error was reported it will follow.")
      print("ERROR: %s" % task.info.error.localizedMessage)
    except VimFault, e:
     print("Failed to reconfigure %s: " % e)
     sys.exit()
    except ObjectNotFoundError:
     print("ERROR: No VM found with name %s" % vm_name)


 def changevmMemory(self,vm_name,memory):
     try:
         new_config = self.client.create("VirtualMachineConfigSpec")
         new_config.memoryMB = memory
         vm = VirtualMachine.get(self.client, name=vm_name)
         print("Reconfiguring %s" % vm_name)
         if vm.config.hardware.numCPU == cpuCount:
             print("Not reconfiguring %s as it already has %s memory" % (vm_name,memory))
             sys.exit()
         task = vm.ReconfigVM_Task(spec=new_config)
         while task.info.state in ["queued", "running"]:
             print("Waiting 5 more seconds for VM creation")
             time.sleep(5)
             task.update()

         if task.info.state == "success":
             elapsed_time = task.info.completeTime - task.info.startTime
             print("Successfully reconfigured VM %s. Server took %s seconds." %
                   (vm_name, elapsed_time.seconds))
         elif task.info.state == "error":
             print("ERROR: The task for reconfiguring the VM has finished with"
                   " an error. If an error was reported it will follow.")
             print("ERROR: %s" % task.info.error.localizedMessage)
     except VimFault, e:
         print("Failed to reconfigure %s: " % e)
         sys.exit()
     except ObjectNotFoundError:
         print("ERROR: No VM found with name %s" % vm_name)



source_vm_name = "Chef Node"
dest_vm_name = "Chef Node Clone"

x=Vmops()
x.connectVIServer("69.33.0.216","vpxuser","Tubuai123!")
x.connect("69.33.0.216","vpxuser","Tubuai123!")
x.stopVm(source_vm_name)
x.changevmMemory(source_vm_name,2096)
x.cloneMachine(source_vm_name,dest_vm_name)
#x.startVm(source_vm_name)

#x.stopGuest(source_vm_name)
#x.rebootGuest(source_vm_name)


#x.closeconnection()