from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.core.window import Window
from shapes import *
from cell_w import CellBackground
from movement import Movement
from random import randint

from point import Point
from tetris_w import Tetris

class TetrisApp(App):
    t = None
    
    def random_shape(self):
        starting_pos = Point(4,21)
        shapes = {}
        #shapes[0]=TShape
        #shapes[1]=LShapeRight
        #hapes[2]=LShapeLeft
        #shapes[3]=ZShapeRight
        #shapes[4]=ZShapeLeft
        shapes[0]=ZShapeRight
        
        #return shapes[randint(0,4)](starting_pos)
        return shapes[0](starting_pos)
    
    def random_background(self):
        CellBackground.red=randint(0,1)
        CellBackground.green=randint(0,1)
        CellBackground.blue=randint(0,1)
    
    def build(self):
        Window.size=(400,800)
        self.t = Tetris()        
        
        #self.ts = TShape(Point(4,4))
        shape=self.random_shape()
        
        #self.t.add_shape(self.ts)
        self.t.add_shape(shape)        
        
        self.t.current_shape(shape)
        
        Clock.schedule_interval(self.update, 0.05)
        
        return self.t
    
    def update(self, dt):
        if self.t.current.locked:
            self.random_background()
            shape=self.random_shape()
            self.t.add_shape(shape)
            self.t.current_shape(shape)
    
if __name__=="__main__":
    TetrisApp().run()    