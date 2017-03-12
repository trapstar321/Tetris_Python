from kivy.uix.widget import Widget
from point import Point
from kivy.core.window import Window
from kivy.properties import ObjectProperty,NumericProperty

class CellBorder(Widget):
    red=NumericProperty(0.1)
    green=NumericProperty(0.2)
    blue=NumericProperty(0.3)    

class CellBackground(Widget):
    red=NumericProperty(0.3)
    green=NumericProperty(0.2)
    blue=NumericProperty(0.1)
    
    def size(self):
        return self.parent.size[0]/1.1
    
    def margin(self):
        return (self.parent.size[0]-self.size())/2

class Cell(Widget):   
    background=ObjectProperty(None)
    border=ObjectProperty(None) 
    def __init__(self,point,**kwargs):
        size=(Window.size[0]/10, Window.size[1]/20)                
        kwargs['size']=size 
        self.point=point
        
        super(Cell, self).__init__(**kwargs)
        