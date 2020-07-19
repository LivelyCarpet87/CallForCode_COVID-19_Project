import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.storage.jsonstore import JsonStore


#Changes the window size
from kivy.core.window import Window
Window.size = (kivy.metrics.mm(72.3), kivy.metrics.mm(157.8)) #Height, Width


#MAC
from scapy.all import ARP, Ether, srp
import sys
import subprocess
import os

#TIME
import datetime

#Regular Expressions
import re

#Manages all permanent storage and adding into the JSON file
class storageUnit():

    def __init__(self):
        print("Before trying to find json file")
        self.store = JsonStore('local.json')
        print("Before test of jsonstore file")
#        if (not self.store.exists("numEntries")):
#            self.store.put("numEntries", value = 0)
 #           self.store.put("macDict", value = dict())
#            self.store.put("recentTen", value = list())
#            self.store.put("prevNetwork", value = dict())
        print("BEFORE PRINT ________")
        print(self.store.get("prevNetwork")["value"])
        print("AFTER PRINT _________")
        
#Adds a unknown / new mac address that was not on the previous network into the json file
    def addEntry(self, macAddress, time):
        if macAddress in self.store.get("macDict")["value"]:
            self.store.get("macDict")["value"][macAddress] += [time]#HEREEE
            self.store.get("recentTen")["value"] = [[time, macAddress]] + self.store.get("recentTen")["value"][:9]
            #self.store.get("prevNetwork")["value"][macAddress] = 0
        else:
            self.store.get("numEntries")["value"] += 1
            self.store.get("macDict")["value"][macAddress] = [time]
            self.store.get("recentTen")["value"] = [[time, macAddress]] + self.store.get("recentTen")["value"][:9]
            #self.store.get("prevNetwork")["value"][macAddress] = 0
#Checks if the previous prevNetwork is the same as foreignSet, which is a set
    def isSamePrevNetwork(self, foreignSet):
        returnArr = []
        for i in foreignSet:
            if i not in self.store.get("prevNetwork")["value"]:
                returnArr += [i]
        return returnArr

#This entire class is meant for macAddress collection
class GetMacAdd():
    def __init__(self, **kwargs):
        #super(HomePage, self).__init__(**kwargs)
        print("enter GetMacAdd")
        self.storage = storageUnit()

        self.supported = False  #  Documents whether our mac address collection method is supported


    def pressed(self, instance):
        print("button pressed")
        macList = self.getMac()
        self.label3.text = "SelfMac : " + macList

    def getString(self, recentTen):
        returnStr = ""
        for i in recentTen:
            returnStr += repr(i)+ "\n"
        return returnStr

    def tryGetMac(self):

        fails = 0
        if os.path.isfile(os.sep+"proc"+os.sep+"net"+os.sep+"arp"):
            if os.access(os.sep+"proc"+os.sep+"net"+os.sep+"arp", os.R_OK):
                f=open(os.sep+"proc"+os.sep+"net"+os.sep+"arp", "r")
                result = f.read()
                self.supported = True  #  Documents whether our mac address collection method is supported
                return result
            else:
                fails = fails + 1
        else:
            fails = fails + 1
        try:
            result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
            self.supported = True #  Documents whether our mac address collection method is supported
            return result
        except subprocess.CalledProcessError:
            fails = fails + 1
            pass
        self.supported = False #  Documents whether our mac address collection method is supported
        return ""

    def getMac(self):
        result = self.tryGetMac()

        macInitStr = result.stdout

        macInitStr = repr(macInitStr)
        isMacAddr = re.compile(r"([\da-fA-F]{1,2}:[\da-fA-F]{1,2}:[\da-fA-F]{1,2}:[\da-fA-F]{1,2}:[\da-fA-F]{1,2}:[\da-fA-F]{1,2})")
        shortMacList = re.findall(isMacAddr,macInitStr)
        isContractionStart = re.compile(r'^([\da-fA-F]):')
        isContractionMid = re.compile(r':([\da-fA-F]):')
        isContractionEnd = re.compile(r':([\da-fA-F])$')
        macList = []
        for mac in shortMacList:
            if re.search(isContractionStart,mac) is not None:
                digit = re.search(isContractionStart,mac).group(1)
                mac = re.sub(isContractionStart,digit + "0:",mac)
            if re.search(isContractionEnd,mac) is not None:
                digit = re.search(isContractionEnd,mac).group(1)
                mac = re.sub(isContractionEnd,":" + digit + "0",mac)
            while re.search(isContractionMid,mac) is not None:
                digit = re.search(isContractionMid,mac).group(1)
                mac = re.sub(isContractionMid,":" + digit + "0:",mac)
            macList.append(mac)

        """
        splitArr = macInitStr.split(" ")
        macList = []
        for part in splitArr:
            if part.count(":") == 5:
                macList += [part]
        """
        compareSet = set(macList)
        print("compareSet = " + repr(compareSet))
        print("prevNetwork = " + repr(self.storage.store.get("prevNetwork")["value"]))
        diffArr = self.storage.isSamePrevNetwork(compareSet)
        if len(diffArr) == 0:
            return self.getString(self.storage.store.get("recentTen")["value"])
        else:
            for macAdd in diffArr:
                self.storage.addEntry(macAdd, str(datetime.datetime.now()))
            
            self.storage.store.put("prevNetwork", value = dict.fromkeys(compareSet, 0))
            return self.getString(self.storage.store.get("recentTen")["value"])

#Class for the homepage screen
class HomePage(Screen, Widget):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
#References the json file called local.json
        self.store = JsonStore('local.json')
        print("whether previous exist = " + repr(self.store.exists('numEntries')))
#Checks if there is a file. If there is not, initiate all 4 necessary parts
        if (not self.store.exists('numEntries')):
            print("enter")
            self.store.put("numEntries", value = 0)
            self.store.put("macDict", value = dict())
            self.store.put("recentTen", value = list())
            self.store.put("prevNetwork", value = dict())
        self.options = ObjectProperty(None)
#macClass variable is just used as a reference to be able to call the getMac class
        self.macClass = GetMacAdd()
        self.actualMac = self.macClass.getMac()
        
    
    
#This method is used when we click the button to check our current network mac
    def calculateMac(self):
        self.actualMac = self.macClass.getMac()
        return self.actualMac
    
    #This calculates the offset accordingly (topLeftH and topLeftW are both in terms of proportions)
    def findCoordinates(self, percentage, topLeftWidth, topLeftHeight):
        smallDim = min(Window.size)
        offSet = smallDim * percentage
        xCoor = topLeftWidth * Window.size[1] + offSet#Windows: (Height, Width)
        yCoor = topLeftHeight * Window.size[0] - self.options.size[0] - offSet
        print(xCoor / Window.size[1])
        print(yCoor / Window.size[0])
        return (xCoor / Window.size[1], yCoor / Window.size[0])
    
    pass

#SideBar class page (reference my.kv file)
class SideBarPage(Screen):
    pass

#AboutUs class page (reference my.kv file)
class AboutUsPage(Screen):      
    pass

#QuitApp class page (reference my.kv file)
class QuitAppPage(Screen):
    def deleteDataButtonClicked(self):
        print("DeleteData button Clicked")
    def quitButtonClicked(self):
        print("Quit button clicked")
    pass

#SendData class page (reference my.kv file)
class SendDataPage(Screen):
    def sendDataButtonClicked(self):
        print("sendData button clicked")
    pass

#SeeDataPage class page (reference my.kv file)
class SeeDataPage(Screen):
    def __init__(self, **kwargs):
        super(SeeDataPage, self).__init__(**kwargs)
        print("ENTER SEEDATAPAGE INIT")
        self.store = JsonStore('local.json')
#Used for future reference and changing the data in the table
        self.data = [0] * 20
#Stores the recentTen aspect of the json file
        self.recentTen = self.store.get("recentTen")["value"]
#Creates the grid used to display the information
        self.table = GridLayout()
        self.table.cols = 2
        
        
        print("BEFORE ASSIGN VALUES")
#Initiates the table by first creating a label into the self.data array, and 
#then adding them to the grid
        for i in range(len(self.recentTen)):
            self.data[2 * i] = Label(text = self.recentTen[i][1])
            self.data[2 * i + 1] = Label(text = self.recentTen[i][0])
            self.table.add_widget(self.data[2 * i])
            self.table.add_widget(self.data[2 * i + 1])
        self.add_widget(self.table)

#This method changes the self.data so that it reflects the new recentTen
    def renewRecentTen(self):
        print("renew clicked")
        self.recentTen = self.store.get("recentTen")["value"]
        for i in range(len(self.recentTen)):
            self.data[2 * i].text = self.recentTen[i][1]
            self.data[2 * i + 1].text = self.recentTen[i][0]

    pass

#Represent the transitions between the windows above
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")
    
class MyMainApp(App):
    def build(self):
        print(Window.size)
        print(type(Window.size))
#        store = JsonStore('local.json')
#        print(store.exists('numEntries'))
#        if (not store.exists('numEntries')):
#            print("enter")
#            store.put("numEntries", value = 0)
#            store.put("macDict", value = dict())
#            store.put("recentTen", value = list())
 #           store.put("prevNetwork", value = dict())
        return kv
    

if __name__ == "__main__":
    print("ENTER MOST OUTSIDE")
    MyMainApp().run()
    exit()