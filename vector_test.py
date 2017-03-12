from rotation import rotate_around_origin

print(rotate_around_origin((1,1), (0,1)))
print(rotate_around_origin((1,1), (1,2)))
print(rotate_around_origin((1,1), (2,1)))

print(rotate_around_origin((1,1), (1,0)))
print(rotate_around_origin((1,1), (0,1)))
print(rotate_around_origin((1,1), (1,2)))

#5,7 -> 4,8
#4,8 -> 3,7
#4,6 -> 5,7

#Point[5,7] Point[4,8]
#Point[4,6] Point[5,7]
#Point[4,8] Point[3,7]

#Point[4,8] Point[3,7]
#Point[5,7] Point[4,8]
#Point[3,7] Point[4,6]