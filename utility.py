__author__ = 'icsadmin'

import os
from basicOps import basicOps
import pprint


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
     elif ok.isdigit() and int(ok) == 3:
        break;
     elif  ok.isdigit() and int(ok) == 1:
        x=basicOps()
        x.connect()
        self.showManagedList(x)


 def MainMenu(self):
         os.system("clear")
         print("******************************VCENTER Admin Utility******************************")
         print("1. Browse Server")
         print("2. Launch Machine")
         print("3. Exit")


 def showManagedList(self,x,datacenter=True, cluster=False):
         print("Current Data Center List on the Server.Select data Center Option")
         val=x.getDataCenters()
         i=1
         while 1
         for y in val.values():
            print(str(i) + ".)" + y)
            i=i+11


         self.showFooter()





 def showFooter(self):
        print("\n")
        print("\n")
        print("\n")
        print ("x. Back to Main Menu")

 def savecontext(self):