import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics import Color

class Touch(Widget):
    
    btn = ObjectProperty(None)
    
    def on_touch_down(self, touch):
        print("mouse down", touch)
        self.btn.opacity = 0.5
    def on_touch_move(self, touch):
        print("mouse move", touch)
        self.btn.pos = touch.pos
    def on_touch_up(self, touch):
        print("mouse up", touch)
        self.btn.opacity = 1
    
    
    
class MyApp(App):
    def build(self):
        return Touch()
    

if __name__ == "__main__":
    MyApp().run()
    exit()