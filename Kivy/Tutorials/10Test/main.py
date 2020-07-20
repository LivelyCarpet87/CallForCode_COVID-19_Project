import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
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


class storageUnit():

    def __init__(self):
        print("Before trying to find json file")
        self.store = JsonStore('local.json')
        print("Before test of jsonstore file")
        if (not self.store.exists("numEntries")):
            self.store.put("numEntries", value = 0)
            self.store.put("macDict", value = dict())
            self.store.put("recentTen", value = list())
            self.store.put("prevNetwork", value = dict())
        print("BEFORE PRINT ________")
        print(self.store.get("prevNetwork")["value"])
        print("AFTER PRINT _________")
        

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
    def isSamePrevNetwork(self, foreignSet):
        returnArr = []
        for i in foreignSet:
            if i not in self.store.get("prevNetwork")["value"]:
                returnArr += [i]
        return returnArr

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
                self.storage.addEntry(macAdd, datetime.datetime.now())
            
            self.storage.store.put("prevNetwork", value = dict.fromkeys(compareSet, 0))
            return self.getString(self.storage.store.get("recentTen")["value"])

class HomePage(Screen, Widget):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.options = ObjectProperty(None)
        self.macAdd = GetMacAdd().getMac()
        
    
    
    
    def calculateMac(self):
        return self.macAdd
    
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

class SideBarPage(Screen):
    pass

class AboutUsPage(Screen):
    
            
    pass

class QuitAppPage(Screen):
    pass

class SendDataPage(Screen):
    pass

class SeeDataPage(Screen):
    pass

#Represent the transitions between the windows above
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")
    
class MyMainApp(App):
    def build(self):
        print(Window.size)
        print(type(Window.size))
        
        return kv
    

if __name__ == "__main__":
    
    MyMainApp().run()
    exit()