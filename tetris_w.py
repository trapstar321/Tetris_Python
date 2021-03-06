from kivy.uix.widget import Widget
from kivy.core.window import Window
from movement import Movement
from kivy.clock import Clock
from point import Point
from shapes import Shape
from kivy.graphics import Color
from kivy.properties import ObjectProperty
from score import Score

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
    
    MAX_ROTATIONS=8
    
    score = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Tetris, self).__init__(**kwargs)
        self.shapes=[]       
        self.current=None
        self.current_score=0
        
        self.n_current_rotations=0
        self.rotated=False      
        
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
    
        self.update_score(0)
    
        Clock.schedule_interval(self.movement, 0.07)
        Clock.schedule_interval(self.rotation, 0.2) 
        Clock.schedule_interval(self.move_down, 0.8)
    
    def update_score(self, x):
        self.current_score+=x        
        self.score.text = 'Score: {0}'.format(self.current_score)
    
    def reset(self):        
        for shape in self.shapes:
            for cell in shape.cells:
                self.remove_widget(cell)
        
        self.shapes=[]
        self.current=None
        self.n_current_rotations=0
        self.rotated=False
        self.current_score=0
        self.update_score(0) 
        
        return
    
    def add_shape(self, shape):
        self.shapes.append(shape)
        #for cell in cells:            
            #self.add_widget(cell)            
    
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
    
    def lock_current_shape(self):
        self.current.lock_shape()
        self.n_current_rotations=0
        
    def movement(self,dt):        
        collision=None        
        if self.key_pressed(Tetris.LEFT) or self.key_pressed(Tetris.A):
            new_positions = self.current.move(Movement.LEFT)
            collision=self.current.collision(new_positions, self.shapes)
            if not collision:
                self.current.apply_changes(new_positions)                     
        elif self.key_pressed(Tetris.RIGHT) or self.key_pressed(Tetris.D):
            new_positions = self.current.move(Movement.RIGHT)
            collision=self.current.collision(new_positions, self.shapes)
            if not collision:
                self.current.apply_changes(new_positions)            
        if self.key_pressed(Tetris.DOWN) or self.key_pressed(Tetris.S):
            new_positions = self.current.move(Movement.DOWN)
            collision=self.current.collision(new_positions, self.shapes)
            if not collision:
                self.current.apply_changes(new_positions) 
                self.update_score(Score.MOVEMENT.value)
            else:
                self.lock_current_shape()
                         
        self.hide_out_of_bound_cells()
    
    def move_down(self, dt):
        new_positions = self.current.move(Movement.DOWN)
        collision=self.current.collision(new_positions, self.shapes)
        if not collision:
            self.current.apply_changes(new_positions)
        else:
            if not self.rotated:
                self.lock_current_shape()
            if self.rotated and self.n_current_rotations==Tetris.MAX_ROTATIONS:
                self.lock_current_shape()
                
        self.rotated=False
        self.hide_out_of_bound_cells() 
        
    def rotation(self, dt):
        if self.key_pressed(Tetris.SPACE) or self.key_pressed(Tetris.UP) or self.key_pressed(Tetris.W):
            self.rotated=True
            self.current.rotate(self.shapes)
            self.hide_out_of_bound_cells()
            
            if self.n_current_rotations<Tetris.MAX_ROTATIONS:                
                self.n_current_rotations+=1
            
    def hide_out_of_bound_cells(self):        
        for cell in self.current.cells:
            if cell.point.y>=Shape.MAX_Y-1 and cell.added:
                cell.added=False
                self.remove_widget(cell)
            if cell.point.y<=Shape.MAX_Y-1 and not cell.added:
                cell.added=True                
                self.add_widget(cell)
     
    
    def remove_row(self, y):
        for x in range(0, Shape.MAX_X):
            for shape in self.shapes:
                for cell in shape.get_cell(Point(x,y)):
                    shape.remove_cell(cell)
                    self.remove_widget(cell)        
               
    def remove_full(self):
        rows_removed = []
        for y in range(0,Shape.MAX_Y):
            found_cnt = 0
            for x in range(0,Shape.MAX_X):
                found=False
                for shape in self.shapes:
                    if len(list(shape.get_cell(Point(x,y))))>0:
                        found=True
                        break;
                if found:
                    found_cnt+=1
                    #print('Found {0}:{1}'.format(x,y))
                    if x==Shape.MAX_X-1:
                        #print('Remove row {0}'.format(y))
                        self.remove_row(y)
                        rows_removed.append(y)
                        
                else:
                    #print("Row {0} not full".format(y))
                    break            
        
        #move all cells after last removed row one row down
        if(len(rows_removed))>0:
            print(max(rows_removed))
            
            self.update_score(Score.FULL_ROW.value*len(rows_removed))
            
            for y in range(max(rows_removed)+1,Shape.MAX_Y) :
                for x in range(0, Shape.MAX_X):
                    for shape in self.shapes:
                        cells = shape.get_cell(Point(x,y))
                        for cell in cells:
                            shape.move_cell(cell, Point(cell.point.x, cell.point.y-len(rows_removed)))                 