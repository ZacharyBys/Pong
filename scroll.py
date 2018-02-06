from pynput.keyboard import Key, Listener
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False                                     

class ScrollGame(Widget):
    jumper = ObjectProperty(None)
    
    def update(self, dt):
        self.jumper.jump()

class Jumper(Widget):
    jumpvalue = NumericProperty(35)
    jumpBool = NumericProperty(1)
    jumpHeight = NumericProperty(135)
    floorHeight = NumericProperty(35)
    jumpSpeed = NumericProperty(2)

    def jump(self):
        if (self.jumpBool == 1):
            if self.jumpvalue < self.jumpHeight:
                self.jumpvalue += self.jumpSpeed
            else:
                self.jumpBool = 0;
        else:
            self.land()

    def land(self):
        if self.jumpvalue > self.floorHeight:
            self.jumpvalue -= self.jumpSpeed
        else: 
            self.jumpBool = 1


class ScrollApp(App):
    def build(self):
        game = ScrollGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    ScrollApp().run()