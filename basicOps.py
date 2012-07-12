__author__ = 'icsadmin'




import sys
import time

from psphere.errors import ObjectNotFoundError
from psphere.client import Client
from psphere.soap import VimFault
from psphere.managedobjects import VirtualMachine
from pysphere import VIServer
from config import Config
import re




class basicOps:

    server=None

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
        self.server=VIServer()
        self.server.connect(server,username,password)

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

    def clone(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        resource_pools=self.server.get_resource_pools()
        arp=resource_pools.keys()[0]
        new_vm=vm.clone("Chef node Clone",resourcepool=arp)

    def getResourceList(self, cluster=None, datacenter=None, resourcePool=None):
         if datacenter==None and cluster==None:
            resource_pools=self.server.get_resource_pools()
         elif (datacenter==None and cluster !=None):
            clusters=self.server.get_clusters()
            print clusters
            keycluster=self.find_key(clusters,cluster)
            print(keycluster)
            resource_pools=self.server.get_resource_pools(keycluster)
            print(resource_pools)
            resourcePool=self.find_key(resource_pools,resourcePool,True)
            print(resourcePool)



 #               resource_pools=self.server.get_resource_pools()
    def find_key(self,dic, val, partial=False):
      retval=None
      if partial==False:
       retval=[k for k, v in dic.iteritems() if v == val][0]
      else:
        retval =[k for k, v in dic.iteritems() if (v.find(val)>0)][0]
      return retval

    def find_value(self,dic, key):
     return dic[key]

         #resource_pools=self.server.get_resource_pools()er,
         #print(resource_pools.values())

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


