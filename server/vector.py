import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def sub(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def mult(self, value):
        return Vector(self.x*value, self.y*value)

    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    
    def normalise(self):
        return self.mult(1/self.mag())
        
    def bearing(self):
        return math.atan2(self.x, self.y)

    def distance_to(self, other):
        return math.sqrt(self.quadrance_to(other))

    def quadrance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx*dx + dy*dy

    @staticmethod
    def fromAngle(angle):
        return Vector(math.cos(angle), math.sin(angle))

    def dot(self,other):
        return self.x*other.x+self.y*other.y

    def cross(self,other):
        return self.x*other.y - self.y*other.x