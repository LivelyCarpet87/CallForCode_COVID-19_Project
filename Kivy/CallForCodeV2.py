#KIVY
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

#MAC
from scapy.all import ARP, Ether, srp
import sys
import subprocess

#TIME
import datetime

#Regular Expressions
import re



class storageUnit():

    def __init__(self):
        self.numEntries = 0
        self.macDict = dict() #Key corresponding to list
        self.recentTen = []
        self.prevNetwork = set()

    def addEntry(self, macAddress, time):
        if macAddress in self.macDict:
            self.macDict[macAddress] += [time]
            self.recentTen = [[time, macAddress]] + self.recentTen[:9]
            self.prevNetwork.add(macAddress)
        else:
            self.numEntries += 1
            self.macDict[macAddress] = [time]
            self.recentTen = [[time, macAddress]] + self.recentTen[:9]
            self.prevNetwork.add(macAddress)



class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.storage = storageUnit()

        self.supported  #  Documents whether our mac address collection method is supported

        self.cols = 1

        self.smallGrid = GridLayout()
        self.smallGrid.cols = 1

        self.label1 = Label(text = "Name : Ryan")
        self.smallGrid.add_widget(self.label1)

        self.label2 = Label(text = "SelfMac : placeHolder")
        self.smallGrid.add_widget(self.label2)


        self.submit = Button(text = "Submit", font_size = 40)
        self.submit.bind(on_press = self.pressed)
        self.smallGrid.add_widget(self.submit)

        self.add_widget(self.smallGrid)

        self.label3 = Label(text = "foundMac : placeHolder")
        self.add_widget(self.label3)

    def pressed(self, instance):
        print("button pressed")
        macList = self.getMac()
        self.label3.text = "SelfMac : " + macList

    def getString(self, recentTen):
        returnStr = ""
        for i in recentTen:
            returnStr += repr(i)+ "\n"
        return returnStr

    def tryGetMac():

        fails = 0
        if os.path.isfile(os.sep+"proc"+os.sep+"net"+os.sep+"arp") \
        and os.access(os.sep+"proc"+os.sep+"net"+os.sep+"arp", os.R_OK)
            f=open(os.sep+"proc"+os.sep+"net"+os.sep+"arp", "r")
            result = f.read()
            self.supported = True  #  Documents whether our mac address collection method is supported
            return result
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
        result = tryGetMac()

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
        print("prevNetwork = " + repr(self.storage.prevNetwork))
        if compareSet.issubset(self.storage.prevNetwork):
            return self.getString(self.storage.recentTen)
        else:
            diff = compareSet.difference(self.storage.prevNetwork)
            for macAdd in diff:
                self.storage.addEntry(macAdd, datetime.datetime.now())
            return self.getString(self.storage.recentTen)


class MyApp(App):
    def build(self):
        print("hello its me this is the start of the program")
        return HomePage()



if __name__ == "__main__":
    MyApp().run()
    exit()
