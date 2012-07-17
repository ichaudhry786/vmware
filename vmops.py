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
from basicOps import basicOps
from config import Config


class Vmops:
 client=None
 def connect(self):
     configuration=Config()
     server = configuration._config_value("general", "server")
     if server is None:
         raise ValueError("server must be supplied on command line"+"or in configuration file.")
     username = configuration._config_value("general", "username")
     if username is None:
         raise ValueError("username must be supplied on command line"
                      " or in configuration file.")
     password = configuration._config_value("general", "password")
     if password is None:
         raise ValueError("password must be supplied on command line"
                      " or in configuration file.")

     self.client=Client(server,username,password)


 def findVM(self,vmName):
     vm = self.client.find_entity_view("VirtualMachine",filter={"name": vmName})
     return vm


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
         if vm.config.hardware.memoryMB== vm_name:
             print("Not reconfiguring %s as it already has %s memory" % (vm_name,memory))
             sys.exit()
         task = vm.ReconfigVM_Task(spec=new_config)
         while task.info.state in ["queued", "running"]:
             print("Waiting 5 more seconds for VM starting")
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

# def getResourcePool(self):
     #pools=self.client.find_entity_view("ResourcePool",filter={"name": "Customs-Dev-vDC"})
     #print(pools)


source_vm_name = "Chef Node Template"
dest_vm_name = "Chef Node Clone"

#x=Vmops()
y=basicOps()


#y.connectVIServer("69.33.0.216","vpxuser","Tubuai123!")
#x.connect()
#y.stopVm(source_vm_name)
#x.changevmMemory(source_vm_name,2096)
#x.cloneMachine(source_vm_name,dest_vm_name)
#y.connect()
#y.clone(source_vm_name,"Development Cluster","Customs-Prod-vDC",cloneName="Chef Node Clone 2")
#y.stopVm(source_vm_name)
#x.getResourcePoole
#x.stopGuest(source_vm_name)
#x.rebootGuest(source_vm_name)
#y.getResourceList(cluster="Development Cluster",resourcePool="Customs-Prod-vDC")
#x=Utility()
#x.showmain()
#x.closeconnection()