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
        
    def add_cell(self, point):
        assert point.x<Shape.MAX_X #and point.y<Shape.MAX_Y
        assert point.x>=Shape.MIN_Y and point.y>=Shape.MIN_Y    
                
        c = Cell(point=point, background=self.background)
        
        self.cells.append(c)        
        c.pos = (point.x*c.size[0], point.y*c.size[1])
    
    def get_cell(self, point):
        return filter(lambda x: x.point.x==point.x and x.point.y==point.y, self.cells)
    
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
                print('Collide with left edge')                  
                return True
            if pos.x>Shape.MAX_X-1:
                print('Collide with right edge')                    
                return True
            if pos.y<Shape.MIN_Y:        
                print('Collide with bottom')        
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
            print('Move left and rotate')
            if not self.try_rotate(new_positions, rotation, degrees, shapes):
                return False
        else:
            print('Collision')
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
        
        print('Did not move before rotating')
        
        for cell in self.cells[1:]:
            new_positions[cell] = rotate_around_origin_clockwise(self.origin.as_tuple(), cell.point.as_tuple())
        
        if not self.collision(new_positions, shapes):
            self.apply_changes(new_positions) 
        else:
            print('Try move left')
            new_positions = self.move(Movement.LEFT)
            collision=self.collision(new_positions, shapes)
            if not collision:          
                if not self.try_rotate(new_positions, Rotation.CLOCKWISE, 90, shapes):
                    return 
                else:
                    collision=True 
            if collision:     
                print('Try move right')           
                new_positions = self.move(Movement.RIGHT)
                collision = self.collision(new_positions, shapes)
                if not collision:
                    if not self.try_rotate(new_positions, Rotation.CLOCKWISE, 90, shapes):
                        return
                    else:  
                        collision=True
            if collision:    
                print('Try move up')
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
        
class TShape(Shape):
    def __init__(self, background, y):
        super(TShape, self).__init__(background)
        
        origin = Point(4, y)
        self.origin=origin
        
        self.add_cell(origin)
        self.add_cell(Point(origin.x+1, origin.y))
        self.add_cell(Point(origin.x-1, origin.y))        
        self.add_cell(Point(origin.x, origin.y+1))
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        self.try_rotate(positions, self.random_rotation(), self.random_degrees(), [])
        

class LShapeRight(Shape):
    def __init__(self, background, y):
        super(LShapeRight, self).__init__(background)
        
        origin = Point(4, y)
        self.origin=origin
        self.add_cell(origin)
        self.add_cell(Point(origin.x, origin.y-1))
        self.add_cell(Point(origin.x, origin.y+1))
        self.add_cell(Point(origin.x+1, origin.y-1))
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        self.try_rotate(positions, self.random_rotation(), self.random_degrees(), [])
        
class LShapeLeft(Shape):
    def __init__(self, background, y):
        super(LShapeLeft, self).__init__(background)
                
        origin = Point(4, y)
        self.origin=origin
                
        self.add_cell(origin)        
        self.add_cell(Point(origin.x, origin.y-1))
        self.add_cell(Point(origin.x, origin.y+1))
        self.add_cell(Point(origin.x-1, origin.y-1))   
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        self.try_rotate(positions, self.random_rotation(), self.random_degrees(), [])
                  

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
        print("Rotate")
        new_positions={}
        
        tmp_counter = self.rotation_counter
        
        tmp_counter+=1
        degrees=270
        rotation=Rotation.CLOCKWISE
        
        if tmp_counter==2:            
            degrees=90
            rotation=Rotation.COUNTER_CLOCKWISE
            print('2 90 COUNTER CLOCKWISE')
        elif tmp_counter==3:            
            degrees=270
            rotation=Rotation.COUNTER_CLOCKWISE
            print('3 270 COUNTER CLOCKWISE')
        elif tmp_counter==4:            
            degrees=90
            rotation=Rotation.CLOCKWISE
            print('4 90 CLOCKWISE')
        else:
            print('1 270 CLOCKWISE')
        
        if tmp_counter==4:
            tmp_counter=0
        
        collision=None
        #move shape if its close to edge and can rotate after that                   
        if self.origin.x==Shape.MAX_X-1:    
            print('Move left')
            new_positions = self.move(Movement.LEFT)                            
        elif self.origin.x==Shape.MIN_X:
            print('Move right')
            new_positions = self.move(Movement.RIGHT)            
        elif self.origin.y==Shape.MIN_Y:
            print('Move up')
            new_positions = self.move(Movement.UP)
        else:            
            for cell in self.cells:
                new_positions[cell]=Point(cell.point.x, cell.point.y)          
        
        
        if not self.try_rotate(new_positions, rotation, degrees, shapes):
            self.rotation_counter=tmp_counter            
            return 
        else:
            print(degrees)
            print(rotation)
            print('Try move left')
            new_positions = self.move(Movement.LEFT)
            collision=self.collision(new_positions, shapes)
            if not collision:          
                if not self.try_rotate(new_positions, rotation, degrees, shapes):
                    self.rotation_counter=tmp_counter
                    return 
                else:
                    print('Collision')
                    collision=True
            if collision:     
                print('Try move right')           
                new_positions = self.move(Movement.RIGHT)
                collision = self.collision(new_positions, shapes)
                if not collision:
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        return
                    else:  
                        print('Collision')
                        collision=True
            if collision:    
                print('Try move up')
                new_positions = self.move(Movement.UP)
                if not self.collision(new_positions, shapes):                
                    if not self.try_rotate(new_positions, rotation, degrees, shapes):
                        self.rotation_counter=tmp_counter
                        return  
                    else:
                        print('Collision')
                        collision=True 
        
class ZShapeLeft(ZShape):
    def __init__(self, background, y):
        super(ZShapeLeft, self).__init__(background)        
        
        origin = Point(4,y)
        self.origin=origin
        
        self.add_cell(origin)        
        self.add_cell(Point(origin.x-1, origin.y))
        self.add_cell(Point(origin.x-1, origin.y-1))        
        self.add_cell(Point(origin.x, origin.y+1)) 
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        rotation = self.random_rotation()        
        for _ in range(0,rotation['rotations']):
            self.rotate([]) 
        
class ZShapeRight(ZShape):
    def __init__(self, background, y):
        super(ZShapeRight, self).__init__(background)
        
        origin = Point(4, y)
        self.origin=origin
                
        self.add_cell(origin)
        self.add_cell(Point(origin.x-1, origin.y))
        self.add_cell(Point(origin.x-1, origin.y+1))        
        self.add_cell(Point(origin.x, origin.y-1)) 
        
        positions={}
        for cell in self.cells:
            positions[cell]=Point(cell.point.x, cell.point.y)
        
        rotation = self.random_rotation()
        for _ in range(0,rotation['rotations']):
            self.rotate([]) 
        
class SquareShape(Shape):
    def __init__(self, background, y):
        super(SquareShape, self).__init__(background)
        
        origin = Point(4, y)
        self.origin=origin
        
        self.add_cell(origin)
        self.add_cell(Point(origin.x+1, origin.y))
        self.add_cell(Point(origin.x+1, origin.y-1))        
        self.add_cell(Point(origin.x, origin.y-1))
        
    def rotate(self, shapes):
        pass
        
if __name__=="__main__":
    sh1 = TShape(Point(3,3))
    
    for point in sh1.points:
        print(point)
                