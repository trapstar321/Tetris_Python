class Point():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        
    def as_tuple(self):
        return (self.x, self.y)
        
    def __str__(self):
        return 'Point[{0},{1}]'.format(self.x, self.y)