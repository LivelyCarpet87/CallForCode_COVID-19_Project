import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

#Changes the window size
from kivy.core.window import Window
Window.size = (kivy.metrics.mm(72.3), kivy.metrics.mm(157.8)) #Height, Width





class HomePage(Screen, Widget):
    
    options = ObjectProperty(None)
    
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