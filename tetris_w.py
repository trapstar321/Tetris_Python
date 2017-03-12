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
    
    def __init__(self, **kwargs):
        super(Tetris, self).__init__(**kwargs)
        self.shapes=[]       
        self.current=None
        
        self.keys = {}
        self.keys[Tetris.LEFT]=False
        self.keys[Tetris.DOWN]=False
        self.keys[Tetris.RIGHT]=False
        self.keys[Tetris.A]=False
        self.keys[Tetris.S]=False
        self.keys[Tetris.D]=False
        self.keys[Tetris.SPACE]=False
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
    
        Clock.schedule_interval(self.movement, 0.05)
        Clock.schedule_interval(self.rotation, 0.1) 
    
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
        self.keys[keycode[0]]=False
       
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keys[keycode[0]]=True     
        #if keycode[0]==Tetris.SPACE:
        #    self.current.rotate()
        #elif keycode[0]==Tetris.S or keycode[0]==Tetris.DOWN:
        #    self.current.move(Movement.DOWN)
        #elif keycode[0]==Tetris.A or keycode[0]==Tetris.LEFT:
        #    self.current.move(Movement.LEFT)
        #elif keycode[0]==Tetris.D or keycode[0]==Tetris.RIGHT:
        #    self.current.move(Movement.RIGHT)
        
    def movement(self,dt):
        #border constraints
        if self.keys[Tetris.LEFT] or self.keys[Tetris.A]:
            if self.current.can_move(Movement.LEFT, self.shapes):
                self.current.move(Movement.LEFT)
        elif self.keys[Tetris.RIGHT] or self.keys[Tetris.D]:
            if self.current.can_move(Movement.RIGHT, self.shapes):
                self.current.move(Movement.RIGHT)
        if self.keys[Tetris.DOWN] or self.keys[Tetris.S]:
            if self.current.can_move(Movement.DOWN, self.shapes):            
                self.current.move(Movement.DOWN)
                
        #TODO: left right collision and movement    
                
        
    def rotation(self, dt):
        if self.keys[Tetris.SPACE]:            
            self.current.rotate()