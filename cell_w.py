from kivy.uix.widget import Widget
from point import Point
from kivy.core.window import Window
from kivy.properties import ObjectProperty,NumericProperty

class CellBorder(Widget):
    red=NumericProperty(1)
    green=NumericProperty(1)
    blue=NumericProperty(1)    

class CellBackground(Widget):
    def __init__(self,**kwargs):
        super(CellBackground,self).__init__(**kwargs)        
    
    def size(self):
        return self.parent.size[0]/1.1
    
    def margin(self):
        return (self.parent.size[0]-self.size())/2

class Cell(Widget):   
    background=ObjectProperty(None)
    border=ObjectProperty(None) 
    score=ObjectProperty(None)
    def __init__(self,point,background,**kwargs):
        size=(400/10, 800/20)                
        kwargs['size']=size 
        self.point=point
        self.added=False
        
        self.red = background.r
        self.green = background.g
        self.blue = background.b
        
        super(Cell, self).__init__(**kwargs)
        