from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock                              

class ScrollGame(Widget):
    jumper = ObjectProperty(None)
    regularenemy = ObjectProperty(None)
    flyingenemy = ObjectProperty(None)
    moveVal = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(ScrollGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.moveVal = 1
        elif keycode[1] == 's':
            self.moveVal = 2
        return True

    def update(self, dt):
        if (not self.jumper.check_death(self.regularenemy) == 1 and not self.jumper.check_death(self.flyingenemy)):
            if (self.moveVal == 1):
                if (self.jumper.jump() == 1):
                    self.moveVal = 0
            elif (self.moveVal == 2):
                if (self.jumper.crouch() == 1):
                    self.moveVal = 0
            self.regularenemy.move()
            self.flyingenemy.move()
            self.jumper.check_death(self.regularenemy)
            self.jumper.check_death(self.flyingenemy)

class RegularEnemy(Widget):
    movePosition = NumericProperty(800)
    moveSpeed = NumericProperty(2)

    def move(self):
        self.movePosition -= self.moveSpeed
        if (self.movePosition < -50):
            self.respawn()
            return 1

    def respawn(self):
        self.movePosition = 1600

class FlyingEnemy(Widget):
    movePosition = NumericProperty(1600)
    moveSpeed = NumericProperty(2)

    def move(self):
        self.movePosition -= self.moveSpeed
        if (self.movePosition < -50):
            self.respawn()
            return 1

    def respawn(self):
        self.movePosition = 1600



class Jumper(Widget):
    jumpvalue = NumericProperty(150)
    jumpBool = NumericProperty(1)
    crouchBool = NumericProperty(1)
    jumpHeight = NumericProperty(350)
    crouchHeight = NumericProperty(20)
    floorHeight = NumericProperty(150)

    jumpSpeed = NumericProperty(2.5)
    crouchSpeed = NumericProperty(2)

    label = 'SCROLLER'

    def jump(self):
        if (self.jumpBool == 1):
            if self.jumpvalue < self.jumpHeight:
                self.jumpvalue += self.jumpSpeed
            else:
                self.jumpBool = 0;
        else:
            if (self.land() == 1):
                return 1

    def land(self):
        if self.jumpvalue > self.floorHeight:
            self.jumpvalue -= self.jumpSpeed
        else: 
            self.jumpBool = 1
            return 1

    def crouch(self):
        if (self.crouchBool == 1):
            if self.jumpvalue > self.crouchHeight:
                self.jumpvalue -= self.crouchSpeed
            else:
                self.crouchBool = 0;
        else:
            if (self.crouchback() == 1):
                return 1

    def crouchback(self):
        if self.jumpvalue < self.floorHeight:
            self.jumpvalue += self.crouchSpeed
        else: 
            self.crouchBool = 1
            return 1

    def check_death(self, enemy):
        if self.collide_widget(enemy):
            return 1

class ScrollApp(App):
    def build(self):
        game = ScrollGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    ScrollApp().run()