from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from shapes import *
from random import random, randint
from dice import roll_die
from tetris_w import Tetris
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class TetrisApp(App):
    t = None
    
    def __init__(self):
        super(TetrisApp, self).__init__()
        self.colors = []    
        self.next_shape=None
        self.display_shape=None
        self.game_over=False
        self.popup=None
        self.score_label=None
        
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
        
        shapes[0]=IShape
        shapes[1]=TShape
        shapes[2]=LShapeRight
        shapes[3]=LShapeLeft
        shapes[4]=ZShapeRight
        shapes[5]=ZShapeLeft   
        shapes[6]=SquareShape
        
        return shapes[roll_die(len(shapes), 20)](self.random_background(), (40,40), None)        
    
    def random_background(self):
        return self.colors[roll_die(len(self.colors), 20)]        
    
    
    def build(self):
        Window.size=(400,870)
        self.t = Tetris()        
        
        #self.ts = TShape(Point(4,4))        
        shape=self.random_shape()
        shape.enter(self.max_y_on_x())  
        self.t.add_shape(shape)
        self.t.current_shape(shape)
        
        self.next_shape=self.random_shape()
        self.display_next_shape(self.next_shape)
        
        Clock.schedule_interval(self.update, 0.05)
        
        return self.t
     
    def max_y_on_x(self):
        #for each position on X find max Y
        #used in shape when entering scene to determine min Y position it should be on
        max_y_on_x={}
        for x in range(0, Shape.MAX_X):
            max_y_on_x[x]=[]            
            for shape in self.t.shapes:
                myox = shape.max_y_on_x(x)
                if myox is not None:
                    max_y_on_x[x].append(myox)
            if len(max_y_on_x[x])==0:
                max_y_on_x[x]=None
            else:
                max_y_on_x[x]=max(max_y_on_x[x])
        return max_y_on_x
    
    def is_game_over(self):
        max_y=self.t.current.max_y()
        if max_y is not None and max_y>Shape.MAX_Y-1:
            return True
        return False
    
    def quit(self, instance):        
        App.stop(self)
    
    def restart(self, instance):
        self.game_over=False
        self.popup.dismiss()        
        self.t.reset()
        
        shape=self.random_shape()
        shape.enter(self.max_y_on_x())  
        self.t.add_shape(shape)
        self.t.current_shape(shape)
        
        self.next_shape=self.random_shape()
        self.display_next_shape(self.next_shape)
        
        return
    
    def show_gameover_popup(self):
        if self.popup is None:
            layout = BoxLayout(orientation='vertical')
            self.score_label = Label(text='', font_size='20sp')
            
            button_layout = BoxLayout(orientation='horizontal')
            restart=Button(text='Restart',font_size='20sp')
            restart.bind(on_press=self.restart)
            quit=Button(text='Quit', font_size='20sp')
            quit.bind(on_press=self.quit)
            button_layout.add_widget(restart)
            button_layout.add_widget(quit)
            
            layout.add_widget(self.score_label)
            layout.add_widget(button_layout)
            
            popup = Popup(title='Game over', content=layout, auto_dismiss=False, size_hint=(None, None), size=(350, 200), title_size='25sp')
            self.popup=popup
        self.score_label.text = 'Your score is: {0}'.format(self.t.current_score)
        self.popup.open()
    
    def update(self, dt):
        if self.game_over:
            return
        if self.t.current.locked:            
            self.t.remove_full();
            if self.is_game_over():
                self.game_over=True
                self.show_gameover_popup()
                return                        
            self.next_shape.enter(self.max_y_on_x())                        
            self.t.add_shape(self.next_shape)
            self.t.current_shape(self.next_shape)
            self.next_shape=self.random_shape()
            self.display_next_shape(self.next_shape)
            
    def display_next_shape(self, shape):
        if self.display_shape is not None:     
            for cell in self.display_shape.cells:
                self.t.remove_widget(cell)        
        
        self.display_shape = shape.__class__(shape.background, (20,20), shape.rotation)
        max_y_pos = self.display_shape.max_y_pos()
        diff = 870-max_y_pos-20
            
        for cell in self.display_shape.cells:
            cell.pos[1]+=diff
            cell.pos[0]+=130 
            self.t.add_widget(cell)
    
if __name__=="__main__":
    TetrisApp().run()    