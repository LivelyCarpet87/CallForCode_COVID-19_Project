import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout



class MyApp(App):
    def build(self):
        return FloatLayout()
    

if __name__ == "__main__":
    MyApp().run()
    exit()