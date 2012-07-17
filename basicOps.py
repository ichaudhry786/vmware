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
            task=vm.power_on(run_sync=False)
            return task

    def stopVm(self, vmname):
        vm=self.server.get_vm_by_name(vmname)
        status=vm.get_status()
        if status=="POWERED ON":
            task=vm.power_off(run_sync=False)
            return task


    def stopGuest(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        task=vm.shutdown_guest(run_sync=False)
        return task

    def rebootGuest(self,vmname):
        vm=self.server.get_vm_by_name(vmname)
        task=vm.reboot_guest(run_sync=False)
        return task

    def getDataCenters(self):
        return self.server.get_datacenters()

    def clone(self,templateName,cloneName="Template Clone"):
        vm=self.server.get_vm_by_name(templateName)
        resourcePool=self.getResourcePool()
        print resourcePool
        task=vm.clone(cloneName,resourcepool=resourcePool,sync_run=False)
        try:
            status=task.get_state()
            print(status)
            print "Creating machine from template:Job Status:" + status
            if  status!="error":
              while (status!="success" or status !="error"):
                  status=task.get_state()
                  if  status=="success":
                   break;
            print "Creating machine from template: Job Status:" + status
            #vm_new=self.server.get_vm_by_name(cloneName)
            #return vm_new
        except:
            print("Error Occured:")


    def getResourcePool(self):

        configuration=Config()
        datacenter = configuration._config_value("vmware", "datacenter")
        if datacenter is None:
            raise ValueError("server must be supplied"+"in configuration file.")
        cluster = configuration._config_value("vmware", "cluster")
        if cluster is None:
            raise ValueError("cluster name must be supplied in configuration file.")
        resourcePool = configuration._config_value("vmware", "resourcePool")
        if resourcePool is None:
            raise ValueError("Resource Pool name must be supplied in configuration file")
        clusters=self.server.get_clusters()
            #print clusters
        keycluster=self.find_key(clusters,cluster)
           # print(keycluster)
        resource_pools=self.server.get_resource_pools(keycluster)
       # print(resource_pools)
        resourcePool=self.find_key(resource_pools,resourcePool,True)
       # print (resourcePool)
        return resourcePool


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


