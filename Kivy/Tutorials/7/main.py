import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class HomePage(Screen):
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
        return kv
    

if __name__ == "__main__":
    MyMainApp().run()
    exit()