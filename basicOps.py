__author__ = 'icsadmin'




import sys
import time

from psphere.errors import ObjectNotFoundError
from psphere.client import Client
from psphere.soap import VimFault
from psphere.managedobjects import VirtualMachine
from pysphere import VIServer
from psphere import config, template
import createvmfromtemplate


class basicOps:

    server=None

    def connectVIServer(self,server_name,userid, password):
        self.server=VIServer()
        self.server.connect(server_name,userid,password)

    def startVm(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        status=vm.get_status()
        if status=="POWERED OFF":
            vm.power_on()

    def stopVm(self, vmname):
        vm=self.server.get_vm_by_name(vmname)
        status=vm.get_status()
        if status=="POWERED ON":
            vm.power_off()

    def stopGuest(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        vm.shutdown_guest()

    def rebootGuest(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        vm.reboot_guest()




#source_vm_name = "Chef Server"
#dest_vm_name = "Chef Server Clone"

#x=Vmops()
#x.connectVIServer("69.33.0.216","vpxuser","Tubuai123!")
#x.connect("69.33.0.216","vpxuser","Tubuai123!")
#x.getTemplate(source_vm_name)
#x.stopVm(source_vm_name)
#x.changevmMemory(source_vm_name,2096)
#x.cloneMachine(source_vm_name,dest_vm_name)
#x.startVm(source_vm_name)

#x.stopGuest(source_vm_name)
#x.rebootGuest(source_vm_name)


#x.closeconnection()


