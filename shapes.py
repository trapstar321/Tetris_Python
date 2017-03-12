from point import Point
from cell_w import Cell
from rotation import rotate_around_origin
from movement import Movement

class Shape(object):
    MAX_X=10
    MAX_Y=20   
    MIN_X=0
    MIN_Y=0 
    
    def __init__(self, origin):
        self.cells = []
        self.origin=origin
        self.locked=False
        
    def add_cell(self, point):
        assert point.x<Shape.MAX_X #and point.y<Shape.MAX_Y
        assert point.x>=Shape.MIN_Y and point.y>=Shape.MIN_Y
        
        c = Cell(point=point)
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

    def collision_check(self, movement, shapes):
        changed_prop = None
        unchanged_prop= None
        direction = None
        if movement==Movement.DOWN:
            changed_prop='y'
            unchanged_prop='x'
            direction=-1
        elif movement==Movement.LEFT:
            changed_prop='x'
            unchanged_prop='y'
            direction=-1
        elif movement==Movement.RIGHT:
            changed_prop='x'
            unchanged_prop='y'
            direction=1
        
        cells = self.cells        
        for shape in shapes:
            if shape is self:
                continue
            for cell in cells:                                
                for c in shape.cells:                                                 
                    if getattr(c.point,changed_prop)==getattr(cell.point, changed_prop)+direction and getattr(c.point,unchanged_prop)==getattr(cell.point, unchanged_prop):
                        return True
        return False

    def can_move(self, movement, shapes):
        if self.locked:
            return False
        if movement==Movement.LEFT:
            for cell in self.cells:
                if cell.point.x<=Shape.MIN_X:                    
                    return False
        elif movement==Movement.RIGHT:
            for cell in self.cells:
                if cell.point.x>=Shape.MAX_X-1:                    
                    return False
        if movement==Movement.DOWN:
            for cell in self.cells:                
                if cell.point.y<=Shape.MIN_Y:
                    self.lock_shape()
                    return False
            
        if self.collision_check(movement, shapes):
            print("Collision")
            if movement==Movement.DOWN:
                self.lock_shape()
            return False   
                
        return True

    def remove_cell(self, point):
        pass
    
    def rotate(self):
        if self.origin.x==Shape.MAX_X-1:
            self.move(Movement.LEFT)
        elif self.origin.x==Shape.MIN_X:
            self.move(Movement.RIGHT)
        elif self.origin.y==Shape.MIN_Y:
            self.move(Movement.UP)
        
        for cell in self.cells[1:]:
            new_position = rotate_around_origin(self.origin.as_tuple(), cell.point.as_tuple())
            
            self.move_cell(cell, new_position) 
            
    def move(self, movement):                
        if movement==Movement.LEFT or movement==Movement.RIGHT:
            x=None
            if movement==Movement.RIGHT:
                x=1
            else:
                x=-1
            for cell in self.cells:
                new_position=Point(cell.point.x+x, cell.point.y)                
                self.move_cell(cell, new_position)
            self.origin=self.cells[0].point
        if movement==Movement.UP: 
            for cell in self.cells:
                new_position=Point(cell.point.x, cell.point.y+1)                
                self.move_cell(cell, new_position)
            self.origin=self.cells[0].point           
        elif movement==Movement.DOWN:
            for cell in self.cells:
                new_position=Point(cell.point.x, cell.point.y-1)                
                self.move_cell(cell, new_position)
            self.origin=self.cells[0].point
    
    def lock_shape(self):
        self.locked=True            
        
class TShape(Shape):
    def __init__(self, origin):
        super(TShape, self).__init__(origin)
        
        self.add_cell(origin)
        self.add_cell(Point(origin.x+1, origin.y))
        self.add_cell(Point(origin.x-1, origin.y))        
        self.add_cell(Point(origin.x, origin.y+1))               
        #self.add_cell(Point(4,6))
        #self.add_cell(Point(3,7))
        #self.add_cell(Point(5,7))
        

class LShapeRight(Shape):
    def __init__(self, origin):
        super(LShapeRight, self).__init__(origin)
        
        self.add_cell(origin)
        self.add_cell(Point(origin.x, origin.y-1))
        self.add_cell(Point(origin.x, origin.y+1))
        self.add_cell(Point(origin.x+1, origin.y-1))
        
class LShapeLeft(Shape):
    def __init__(self, origin):
        super(LShapeLeft, self).__init__(origin)
        
        self.add_cell(origin)
        self.add_cell(Point(origin.x, origin.y-1))
        self.add_cell(Point(origin.x, origin.y+1))
        self.add_cell(Point(origin.x-1, origin.y-1))        
        
if __name__=="__main__":
    sh1 = TShape(Point(3,3))
    
    for point in sh1.points:
        print(point)
                