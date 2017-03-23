from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from shapes import *
from random import random, randint
from dice import roll_die
from tetris_w import Tetris
from kivy.graphics import Color

class TetrisApp(App):
    t = None
    
    def __init__(self):
        super(TetrisApp, self).__init__()
        self.colors = []    
        
        #dark blue
        self.colors.append(self.color(10,47,220))
        #light blue
        self.colors.append(self.color(18,170,214))
        #dark green
        self.colors.append(self.color(0,81,40))
        #light green
        self.colors.append(self.color(0,255,128))
        #orange
        self.colors.append(self.color(234,69,21))
        #red
        self.colors.append(self.color(255,0,0))
        #yellow
        self.colors.append(self.color(230,230,0))
        
        for color in self.colors:
            color.a=0.5
        
    
    def color(self,r, g, b):
        return Color(r/float(255), g/float(255), b/float(255))
    
    def random_shape(self):
        shapes = {}
        
        #shapes[0]=ZShapeRight
        #shapes[1]=ZShapeLeft
        
        shapes[0]=TShape
        shapes[1]=LShapeRight
        shapes[2]=LShapeLeft
        shapes[3]=ZShapeRight
        shapes[4]=ZShapeLeft   
        shapes[5]=SquareShape     
        
        #return shapes[roll_die(len(shapes), 20)](self.random_background(), Shape.MAX_Y-2)
        return shapes[roll_die(len(shapes), 20)](self.random_background(), Shape.MAX_Y-2)        
    
    def random_background(self):
        return self.colors[roll_die(len(self.colors), 20)]        
    
    
    def build(self):
        Window.size=(400,820)
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
            self.t.remove_full();
            shape=self.random_shape()
            print(shape)
            self.t.add_shape(shape)
            self.t.current_shape(shape)
    
if __name__=="__main__":
    TetrisApp().run()    