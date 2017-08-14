import copy

class Field2D(object):
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def add_from(self, other):
       self.x += other.x
       self.y += other.y

    def sub_from(self, other):
        self.x -= other.x
        self.y -= other.y

    def mul_by(self, coeff):
        self.x *= coeff
        self.y *= coeff

    def div_by(self, coeff):
        self.x /= coeff
        self.y /= coeff

    def in_bound(self, lower, higher):
        return self.x > lower and self.y > lower and self.x < higher and self.y < higher
    
    def __repr__(self):
        return "Field2D(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"