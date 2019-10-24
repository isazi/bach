import math


class Point:
    def __init__(self, x, y):
        """
        Default constructor.
        """
        self.x = x
        self.y = y

    def distance(self, point):
        """
        Compute the Euclidean distance to another point.
        """
        return distance(self, point)


def distance(point_one, point_two):
    """
    Compute the Euclidean distance between two points.
    """
    return math.sqrt(math.pow(point_one.x - point_two.x, 2) + math.pow(point_one.y - point_two.y, 2))
