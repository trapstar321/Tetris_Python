from point import Point
from cell_w import Cell, CellBackground
from rotation import rotate_around_origin_clockwise, rotate_around_origin_counter_clockwise, Rotation
from movement import Movement
from enum import Enum
from dice import roll_die

class Shape(object):
    MAX_X=10
    MAX_Y=20   
    MIN_X=0
    MIN_Y=0 
    
    def __init__(self, background):
        self.cells = []
        self.origin=None
        self.locked=False
        self.background=background        
        
    def add_cell(self, point, cell_size):
        assert point.x<Shape.MAX_X #and point.y<Shape.MAX_Y
        assert point.x>=Shape.MIN_Y and point.y>=Shape.MIN_Y    
                
        c = Cell(point=point, background=self.background, size=cell_size)
        
        self.cells.append(c)        
        c.pos = (point.x*c.size[0], point.y*c.size[1])
    
    def get_cell(self, point):
        return filter(lambda x: x.point.x==point.x and x.point.y==point.y, self.cells)
    
    def max_y(self):
        ys = [cell.point.y for cell in self.cells]
        if len(ys)==0:
            return None
        return max(ys)
    
    def max_y_pos(self):
        ys = [cell.pos[1] for cell in self.cells]
        if len(ys)==0:
            return None
        return max(ys)
    
    def min_y(self):
        ys = [cell.point.y for cell in self.cells]
        return min(ys)
    
    def max_y_on_x(self, x):
        cells = []
        for cell in self.cells:
            if cell.point.x==x:
                cells.append(cell)
        
        ys = [cell.point.y for cell in cells]
        if len(ys)==0:
            return None
        return max(ys)        
    
    def min_y_on_x(self, x):
        cells = []
        for cell in self.cells:
            if cell.point.x==x:
                cells.append(cell)
        
        ys = [cell.point.y for cell in cells]
        if len(ys)==0:
            return None
        return min(ys)      
    
    def move_cell(self, cell, new_position):
        assert new_position.x<Shape.MAX_X #and new_position.y<Shape.MAX_Y
        assert new_position.x>=Shape.MIN_X and new_position.y>=Shape.MIN_Y        
        
        pos = (int(new_position.x*cell.size[0]), int(new_position.y*cell.size[1]))                
        cell.pos = pos
        cell.point=new_position    

    def collision(self, new_positions, shapes):
        if self.locked:
            return True
        
        for pos in new_positions.values():           
            if pos.x<Shape.MIN_X: 
                return True
            if pos.x>Shape.MAX_X-1:                                    
                return True
            if pos.y<Shape.MIN_Y:
                return True
            
            for shape in shapes: 
                if shape is self:
                    continue               
                for cell in shape.cells:
                    if cell.point.x==pos.x and cell.point.y==pos.y:                        
                        return True                             
                
        return None

    def remove_cell(self, cell):
        self.cells.remove(cell)
    
    def random_rotation(self):
        rotations=[Rotation.CLOCKWISE, Rotation.COUNTER_CLOCKWISE]
        return rotations[roll_die(len(rotations), 20)]
    
    def random_degrees(self):
        degrees = [90,180,270,360]        
        return degrees[roll_die(len(degrees), 20)]        
    
    #rotate with collision check
    #if rotation is successfull without collision, changes are applied to cells of shape
    def try_rotate(self, positions, rotation, degrees, shapes):        
        x = int(degrees/90)
        if rotation==Rotation.CLOCKWISE: 
            for _ in range(0,x):           
                for key, value in positions.items():                
                    positions[key] = rotate_around_origin_clockwise(positions[self.cells[0]].as_tuple(), value.as_tuple())
                if not self.collision(positions, shapes):                               
                    continue
                else:
                    print('Collision')     
                    return True
            self.apply_changes(positions)
        elif rotation==Rotation.COUNTER_CLOCKWISE:
            for _ in range(0,x):
                for key, value in positions.items():                
                    positions[key] = rotate_around_origin_counter_clockwise(positions[self.cells[0]].as_tuple(), value.as_tuple())
                if not self.collision(positions, shapes):
                    continue
                else:
                    print('Collision')     
                    return True
            self.apply_changes(positions) 
        return False               
    
    def try_move_with_rotate(self, movement, rotation, degrees, shapes): 
        new_positions = self.move(movement)
        collision = self.collision(new_positions, shapes)
        if not collision:
            if not self.try_rotate(new_positions, rotation, degrees, shapes):
                return False
        else:
            return False
        return True
    
    def rotate(self, shapes):
        new_positions={}
        
        collision=None
        #move shape if its close to edge and can rotate after that                   
        if self.origin.x==Shape.MAX_X-1:    
            if not self.try_move_with_rotate(Movement.LEFT, Rotation.CLOCKWISE, 90, shapes):
                return 
        elif self.origin.x==Shape.MIN_X:
            if not self.try_move_with_rotate(Movement.RIGHT, Rotation.CLOCKWISE, 90, shapes):
                return
        elif self.origin.y==Shape.MIN_Y:
            if not self.try_move_with_rotate(Movement.UP, Rotation.CLOCKWISE, 90, shapes):
                return        
        
        for cell in self.cells[1:]:
            new_positions[cell] = rotate_around_origin_clockwise(self.origin.as_tuple(), cell.point.as_tuple())
        
        if not self.collision(new_positions, shapes):
            self.apply_changes(new_positions) 
        else:
            new_positions = self.move(Movement.LEFT)
            collision=self.collision(new_positions, shapes)
            if not collision:          
                if not self.try_rotate(new_positions, Rotation.CLOCKWISE, 90, shapes):
                    return 
                else:
                    collision=True 
            if collision:         
                new_positions = self.move(Movement.RIGHT)
                collision = self.collision(new_positions, shapes)
                if not collision:
                    if not self.try_rotate(new_positions, Rotation.CLOCKWISE, 90, shapes):
                        return
                    else:  
                        collision=True
            if collision:
                new_positions = self.move(Movement.UP)
                if not self.collision(new_positions, shapes):                
                    if not self.try_rotate(new_positions, Rotation.CLOCKWISE, 90, shapes):
                        return  
                    else:
                        collision=True
                
    def move(self, movement): 
        new_positions={}             
        if movement==Movement.LEFT or movement==Movement.RIGHT:
            x=None
            if movement==Movement.RIGHT:
                x=1
            else:
                x=-1
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x+x, cell.point.y)
        if movement==Movement.UP: 
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x, cell.point.y+1)     
        elif movement==Movement.DOWN:
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x, cell.point.y-1)
            
        return new_positions
    
    def apply_changes(self, new_positions):        
        for cell in self.cells:
            try:
                cell.point = new_positions[cell]
                cell.pos = (int(cell.point.x*cell.size[0]), int(cell.point.y*cell.size[1]))
            except KeyError:
                pass
        self.origin=self.cells[0].point        
    
    def lock_shape(self):
        self.locked=True            
    
    def enter(self, max_y_on_x):
        on_screen = self.max_y()-Shape.MAX_Y+1
        if on_screen>0:            
            for _ in range(0, on_screen):
                new_positions = self.move(Movement.DOWN)
                self.apply_changes(new_positions) 
        
        for x in max_y_on_x:
            if max_y_on_x[x] is None:
                continue
            min_y = self.min_y_on_x(x)
            if min_y is None:
                continue
            diff = (max_y_on_x[x]-min_y)+1
                        
            if diff>0:                
                for _ in range(0, diff):                    
                    new_positions = self.move(Movement.UP)
                    self.apply_changes(new_positions)
        
class TShape(Shape):
    def __init__(self, background, size, rotation):        
        super(TShape, self).__init__(background)        
    
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
        self.rotation=rotation
        
        self.add_cell(origin, size)
        self.add_cell(Point(origin.x+1, origin.y), size)
        self.add_cell(Point(origin.x-1, origin.y), size)        
        self.add_cell(Point(origin.x, origin.y+1), size)
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)        
        
        if rotation is None:            
            self.rotation = {'rotation':self.random_rotation(), 'degrees':self.random_degrees()}
            
        self.try_rotate(positions, self.rotation['rotation'], self.rotation['degrees'], [])
        

class LShapeRight(Shape):
    def __init__(self, background, size, rotation):
        super(LShapeRight, self).__init__(background)
        
        self.rotation=rotation
        
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
        self.add_cell(origin, size)
        self.add_cell(Point(origin.x, origin.y-1), size)
        self.add_cell(Point(origin.x, origin.y+1), size)
        self.add_cell(Point(origin.x+1, origin.y-1), size)
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        if not self.rotation:            
            self.rotation={'rotation':self.random_rotation(), 'degrees':self.random_degrees()}
        
        self.try_rotate(positions, self.rotation['rotation'], self.rotation['degrees'], [])
        
class LShapeLeft(Shape):
    def __init__(self, background, size, rotation):
        super(LShapeLeft, self).__init__(background)
                
        self.rotation=rotation
                
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
                
        self.add_cell(origin, size)        
        self.add_cell(Point(origin.x, origin.y-1), size)
        self.add_cell(Point(origin.x, origin.y+1), size)
        self.add_cell(Point(origin.x-1, origin.y-1), size)   
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        if not self.rotation:
            self.rotation={'rotation':self.random_rotation(), 'degrees':self.random_degrees()}
        
        self.try_rotate(positions, self.rotation['rotation'], self.rotation['degrees'], [])      

class ZShape(Shape):
    def __init__(self, background):
        self.rotation_counter=0
        super(ZShape, self).__init__(background)
    
    def random_rotation(self):
        rotations=[
            {'rotation':Rotation.CLOCKWISE, 'degrees':90, 'rotations':0},            
            {'rotation':Rotation.CLOCKWISE, 'degrees':270, 'rotations':1},
            {'rotation':Rotation.COUNTER_CLOCKWISE, 'degrees':90, 'rotations':2},
            {'rotation':Rotation.COUNTER_CLOCKWISE, 'degrees':270, 'rotations':3},
        ]
        
        rotation=rotations[roll_die(len(rotations), 20)]
        return rotation
    
    def rotate(self, shapes):
        new_positions={}
        
        tmp_counter = self.rotation_counter
        
        tmp_counter+=1
        degrees=270
        rotation=Rotation.CLOCKWISE
        
        if tmp_counter==2:            
            degrees=90
            rotation=Rotation.COUNTER_CLOCKWISE
        elif tmp_counter==3:            
            degrees=270
            rotation=Rotation.COUNTER_CLOCKWISE
        elif tmp_counter==4:            
            degrees=90
            rotation=Rotation.CLOCKWISE
        
        if tmp_counter==4:
            tmp_counter=0
        
        collision=None
        #move shape if its close to edge and can rotate after that                   
        if self.origin.x==Shape.MAX_X-1:
            new_positions = self.move(Movement.LEFT)                            
        elif self.origin.x==Shape.MIN_X:
            new_positions = self.move(Movement.RIGHT)            
        elif self.origin.y==Shape.MIN_Y:
            new_positions = self.move(Movement.UP)
        else:            
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x, cell.point.y)          
        
        
        if not self.try_rotate(new_positions, rotation, degrees, shapes):
            self.rotation_counter=tmp_counter            
            return 
        else:
            new_positions = self.move(Movement.LEFT)
            collision=self.collision(new_positions, shapes)
            if not collision:          
                if not self.try_rotate(new_positions, rotation, degrees, shapes):
                    self.rotation_counter=tmp_counter
                    return 
                else:
                    collision=True
            if collision:         
                new_positions = self.move(Movement.RIGHT)
                collision = self.collision(new_positions, shapes)
                if not collision:
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        return
                    else:
                        collision=True
            if collision:
                new_positions = self.move(Movement.UP)
                if not self.collision(new_positions, shapes):                
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        return  
                    else:
                        collision=True 
        
class ZShapeLeft(ZShape):
    def __init__(self, background, size, rotation):
        super(ZShapeLeft, self).__init__(background)        
        
        self.rotation=rotation
        
        origin = Point(4,Shape.MAX_Y)
        self.origin=origin
        
        self.add_cell(origin, size)        
        self.add_cell(Point(origin.x-1, origin.y), size)
        self.add_cell(Point(origin.x-1, origin.y-1), size)        
        self.add_cell(Point(origin.x, origin.y+1), size) 
        
        if not self.rotation:
            self.rotation=self.random_rotation()
          
        for _ in range(0,self.rotation['rotations']):
            self.rotate([])
        
class ZShapeRight(ZShape):
    def __init__(self, background, size, rotation):
        super(ZShapeRight, self).__init__(background)
        
        self.rotation=rotation
        
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
                
        self.add_cell(origin, size)
        self.add_cell(Point(origin.x-1, origin.y), size)
        self.add_cell(Point(origin.x-1, origin.y+1), size)        
        self.add_cell(Point(origin.x, origin.y-1), size)
        
        if not self.rotation:
            self.rotation = self.random_rotation()
            
        for _ in range(0,self.rotation['rotations']):
            self.rotate([])
        
class SquareShape(Shape):
    def __init__(self, background, size, rotation):
        super(SquareShape, self).__init__(background)
        
        self.rotation=rotation
        
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
        
        self.add_cell(origin, size)
        self.add_cell(Point(origin.x+1, origin.y), size)
        self.add_cell(Point(origin.x+1, origin.y-1), size)        
        self.add_cell(Point(origin.x, origin.y-1), size)
        
    def rotate(self, shapes):
        pass
    
class IShape(Shape):
    def __init__(self, background, size, rotation):
        self.rotation_counter=0
        super(IShape, self).__init__(background)    
        
        self.rotation=rotation
        
        origin = Point(4, Shape.MAX_Y)
        self.origin=origin
        
        self.add_cell(origin, size)
        self.add_cell(Point(origin.x, origin.y-1), size)
        self.add_cell(Point(origin.x, origin.y+1), size)        
        self.add_cell(Point(origin.x, origin.y+2), size)
        
        if not self.rotation:
            self.rotation = self.random_rotation()
                    
        for _ in range(0,self.rotation['rotations']):
            self.rotate([])
        
    def random_rotation(self):
        rotations=[
            {'rotation':Rotation.CLOCKWISE, 'degrees':90, 'rotations':0},            
            {'rotation':Rotation.CLOCKWISE, 'degrees':90, 'rotations':1},
            {'rotation':Rotation.COUNTER_CLOCKWISE, 'degrees':90, 'rotations':2},
            {'rotation':Rotation.COUNTER_CLOCKWISE, 'degrees':90, 'rotations':3},
        ]
        
        rotation=rotations[roll_die(len(rotations), 20)]
        return rotation
    
    def move_origin(self, movement):
        new_origin=None
        if movement==Movement.LEFT:
            new_origin = Point(self.cells[0].point.x-1, self.cells[0].point.y)
            
        elif movement==Movement.RIGHT:
            new_origin=Point(self.cells[0].point.x+1, self.cells[0].point.y)
        
        if not new_origin is None:
            cells = self.get_cell(new_origin)
            
            if not cells is None:
                cell = list(cells)[0]
                ind=None
                for idx, c in enumerate(self.cells):
                    if c is cell:
                        ind=idx
                         
                
                tmp_cell = self.cells[0]
                self.cells[0]=cell
                self.cells[ind]=tmp_cell
                
                self.origin=self.cells[0].point
    
    def rotate(self, shapes):
        new_positions={}
        
        tmp_counter = self.rotation_counter
        
        tmp_counter+=1
        degrees=90
        
        switch_origin=Movement.RIGHT        
        rotation=Rotation.CLOCKWISE
        
        if tmp_counter==2:            
            degrees=90
            rotation=Rotation.CLOCKWISE
            switch_origin=None
        elif tmp_counter==3:            
            degrees=90
            rotation=Rotation.COUNTER_CLOCKWISE
            switch_origin=Movement.LEFT
        elif tmp_counter==4:            
            degrees=90
            switch_origin=None
            rotation=Rotation.COUNTER_CLOCKWISE
                
        if tmp_counter==4:
            tmp_counter=0
        
        collision=None
        #move shape if its close to edge and can rotate after that                   
        if self.origin.x==Shape.MAX_X-1:
            new_positions = self.move(Movement.LEFT)                            
        elif self.origin.x==Shape.MIN_X:
            new_positions = self.move(Movement.RIGHT)            
        elif self.origin.y==Shape.MIN_Y:
            new_positions = self.move(Movement.UP)
        else:            
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x, cell.point.y)
        
        if not self.try_rotate(new_positions, rotation, degrees, shapes):
            self.rotation_counter=tmp_counter 
            self.move_origin(switch_origin)           
            return 
        else:
            new_positions = self.move(Movement.LEFT)
            collision=self.collision(new_positions, shapes)
            if not collision:          
                if not self.try_rotate(new_positions, rotation, degrees, shapes):
                    self.rotation_counter=tmp_counter
                    self.move_origin(switch_origin)
                    return 
                else:
                    collision=True
            if collision:           
                new_positions = self.move(Movement.RIGHT)
                collision = self.collision(new_positions, shapes)
                if not collision:
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        self.move_origin(switch_origin)
                        return
                    else:
                        collision=True
            if collision:
                new_positions = self.move(Movement.UP)
                if not self.collision(new_positions, shapes):                
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        self.move_origin(switch_origin)
                        return  
                    else:
                        collision=True 
                        
        
        
if __name__=="__main__":
    sh1 = TShape(Point(3,3))
    
    for point in sh1.points:
        print(point)
                