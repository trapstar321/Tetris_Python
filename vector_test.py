from rotation import rotate_around_origin_clockwise

if __name__=="__main__":
    print(rotate_around_origin_clockwise((15,3), (15,3)))

    d = {}
    d[0]=1
    d[1]=2
    
    for x in d:
        print x

#5,7 -> 4,8
#4,8 -> 3,7
#4,6 -> 5,7

#Point[5,7] Point[4,8]
#Point[4,6] Point[5,7]
#Point[4,8] Point[3,7]

#Point[4,8] Point[3,7]
#Point[5,7] Point[4,8]
#Point[3,7] Point[4,6]