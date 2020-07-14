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



class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.storage = storageUnit()

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
    def getMac(self):
        result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)

        macInitStr = result.stdout

        macInitStr = repr(macInitStr)
        isMacAddr = re.compile(r"([\da-f|A-F]{1,2}:[\da-f|A-F]{1,2}:[\da-f|A-F]{1,2}:[\da-f|A-F]{1,2}:[\da-f|A-F]{1,2}:[\da-f|A-F]{1,2})")
        macList = re.findall(isMacAddr,macInitStr)
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
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()
    exit()
