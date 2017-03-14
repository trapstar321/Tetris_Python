from kivy.uix.widget import Widget
from kivy.core.window import Window
from movement import Movement
from kivy.clock import Clock
from point import Point

class Tetris(Widget):
    LEFT=276
    RIGHT=275
    DOWN=274
    A=97
    S=115
    D=100
    SPACE=32
    W=119
    UP=273    
    
    def __init__(self, **kwargs):
        super(Tetris, self).__init__(**kwargs)
        self.shapes=[]       
        self.current=None
        
        self.keys = {}
        self.keys[Tetris.LEFT]={'handled':True, 'keydown':False}
        self.keys[Tetris.DOWN]={'handled':True, 'keydown':False}
        self.keys[Tetris.RIGHT]={'handled':True, 'keydown':False}
        self.keys[Tetris.A]={'handled':True, 'keydown':False}
        self.keys[Tetris.S]={'handled':True, 'keydown':False}
        self.keys[Tetris.D]={'handled':True, 'keydown':False}
        self.keys[Tetris.SPACE]={'handled':True, 'keydown':False}
        self.keys[Tetris.W]={'handled':True, 'keydown':False}
        self.keys[Tetris.UP]={'handled':True, 'keydown':False}        
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
    
        Clock.schedule_interval(self.movement, 0.07)
        Clock.schedule_interval(self.rotation, 0.2) 
    
    def add_shape(self, shape):
        self.shapes.append(shape)
        cells = shape.cells
        
        for cell in cells:            
            self.add_widget(cell)
    
    def current_shape(self, shape):
        self.current=shape
    
    def remove_shape(self, shape):
        shapes = filter(lambda x:x==shape, self.shapes)
        
        for shape in shapes:
            for cell in shape.cells:
                self.remove_widget(cell)
                
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard=None

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[0] in self.keys:                
            self.keys[keycode[0]]['keydown']=False
       
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):        
        if keycode[0] in self.keys:        
            self.keys[keycode[0]]['keydown']=True
            self.keys[keycode[0]]['handled']=False
        
    def key_pressed(self, key):
        if key in self.keys:
            ret = self.keys[key]['keydown'] or not self.keys[key]['handled']
            self.keys[key]['handled']=True
        else:
            ret = False
        return ret
        
    def movement(self,dt):        
        if self.key_pressed(Tetris.LEFT) or self.key_pressed(Tetris.A):
            if self.current.can_move(Movement.LEFT, self.shapes):
                self.current.move(Movement.LEFT)
        elif self.key_pressed(Tetris.RIGHT) or self.key_pressed(Tetris.D):
            if self.current.can_move(Movement.RIGHT, self.shapes):
                self.current.move(Movement.RIGHT)
        if self.key_pressed(Tetris.DOWN) or self.key_pressed(Tetris.S):
            if self.current.can_move(Movement.DOWN, self.shapes):            
                self.current.move(Movement.DOWN)  
                
        
    def rotation(self, dt):
        if self.key_pressed(Tetris.SPACE) or self.key_pressed(Tetris.UP) or self.key_pressed(Tetris.W):            
            self.current.rotate()