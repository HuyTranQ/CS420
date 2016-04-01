import cmath

class Node:

    """Node in AI Graph Agent"""

    def __init__(self , name , x , y):
        self._name = name
        self._x = x
        self._y = y

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    def estimate(self , target):
        return 1 + int(cmath.sqrt(pow(self._x - target.x , 2) + pow(self._y - target.y , 2)))

    def __str__(self):
        return 'Node ' + str(self._name) + ' is at (' + str(self._x) + ' ; ' + str(self._y) + ')'
