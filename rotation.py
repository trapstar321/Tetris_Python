from kivy.vector import Vector
import numpy
import math
from point import Point
from enum import Enum

class Rotation(Enum):
    CLOCKWISE=1
    COUNTER_CLOCKWISE=2


rotation_matrix_clockwise=numpy.array(
    [
         [0,-1],
         [1, 0]
    ]
)

rotation_matrix_counter_clockwise=numpy.array(
    [
         [0,1],
         [-1, 0]
    ]
)

def rotate_around_origin_clockwise(origin, point):
    v1 = Vector(point)-Vector(origin)
    
    v2 = rotation_matrix_clockwise.dot(v1)
    
    new_position = Vector(origin)-Vector(v2)    
    
    return Point(new_position[0], new_position[1])

def rotate_around_origin_counter_clockwise(origin, point):
    v1 = Vector(point)-Vector(origin)
    
    v2 = rotation_matrix_counter_clockwise.dot(v1)
    
    new_position = Vector(origin)-Vector(v2)    
    
    return Point(new_position[0], new_position[1])
    
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy    