__author__ = 'icsadmin'

import os
from basicOps import basicOps
import pprint
from vmops import Vmops




class Utility:

 def showmain(self):
    self.MainMenu()
    while  1:
     ok=raw_input()
     if (len(ok)>1):
         continue
     if ok in (''):
         continue
     if ok =='x':
        self.MainMenu()
     elif ok.isdigit() and int(ok) == 6:
        break;
     elif  ok.isdigit() and int(ok) == 1:
        x=basicOps()
        x.connect()
        print("Printing ")
        self.ask_for_Machine("Chef Node Template")
     elif  ok.isdigit() and int(ok) == 2:
         x=basicOps()
         x.connect()
         self.ask_for_Machine("Windows Template name")
     elif  ok.isdigit() and int(ok) == 3:
         x=basicOps()
         x.connect()
         self.ask_for_Machine("Ubuntu 12.04 64bit med")
     elif  ok.isdigit() and int(ok) == 4:
         x=basicOps()
         x.connect()
         self.ask_for_Machine("Windows Template name")
     elif  ok.isdigit() and int(ok) == 5:
         x=basicOps()
         x.connect()
         self.ask_for_Machine("Windows Template name",receipe=True)




 def MainMenu(self):

         os.system("clear")
         print("******************************VCENTER Admin Utility******************************")
         print("1. Launch Centos Machine")
         print("2. Launch Windows Machine")
         print("3. Launch Ubuntu Machine")
         print("4. Show Machine Summary")
         print("5. Install Recipe")
         print("6. Exit")





 def showRecipes(self):

    os.system("clear")
    print("******************************Select Packages to Install on the VM******************************")
    print("1. MySQL Install")
    print("2. .net Install. Only Applicable to Windows")
    print("x. Main")


 def ask_for_Machine(self, templateName,showSummary=False,receipe=False):
     os.system("clear")

     print("Enter Machine Name")
     while True:
      name=raw_input()
      if name in (''):
        continue
      if name=='x':
          self.MainMenu()
      elif (len(name)>2):
         machineName=name
         if(receipe==True):
            self.showRecipes()
            while True:
               name=raw_input()
               if name=='x':
                 break;
               if((receipe==True)and(name.isdigit())and(int(name)==1)):
                 #search machine or show message if m1achine is not there
                 print("Generating Recipe 1")
               elif((receipe==True)and(name.isdigit())and(int(name)==2)):
                 #search machine or show message if machine is not there
                 print("Generating Recipe 2")
               elif(receipe==True)and name.isdigit():
                 #search machine or show message if machine is not there
                 continue
            self.showmain()
         elif (receipe==False):
            print("Creating Machine:"+machineName+":")
            x=basicOps()
            y=Vmops()
            x.connect()
            y.connect()
            print(templateName)
            print(machineName)
            x.clone(templateName,machineName)
            bootstrapChef(machineName)
            self.showFooter()

 def showFooter(self):
        print("\n")
        print ("x. Back to Main Menu")

 def bootstrapChef(self,vm):
     y=Vmops()
     y.connect()
     chefnode=y.findVM(vm)
     chefnode.login_in_guest("root","Tubuai123!")
     chefserver=y.findVM("Chef Server")
     chefserver.login_in_guest("root","Tubuai123!")

     createhostnamecentosfile(vm)
     # remove the chef client properties from the server
     pid=chefnode.start_process("/bin/rm",args=["-f","-r","/etc/chef"])
     if pid >0: print("Chef Node with name "+ vm + " Initialized")
     pid=chefserver.start_process("knife bootstrap "+ ip + "-x root -P Tubuai123! -y" )
     if pid >0: print("Chef Server bootstraped Chef Node"+vm)

 def createhostnamecentosfile(self,vmname):

     print ("create file and upload to the server")
     #create file and upload to the /etc/sysconfig folder using vmname as the servername
     #reboot guest
     # get task check status
     # Check vm status also
     # once vm status is up then
     # get IP
     #return IP address



y=Utility()
y.showmain()



