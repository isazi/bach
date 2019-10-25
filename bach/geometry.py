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


class Rectangle:
    def __init__(self, center, width, height):
        """
        Default constructor.
        """
        self.vertices = list()
        self.vertices.append(Point(int(center.x - (width / 2)), int(center.y - (height / 2))))
        self.vertices.append(Point(int(self.vertices[0].x + width), int(self.vertices[0].y)))
        self.vertices.append(Point(int(self.vertices[0].x), int(self.vertices[0].y + height)))
        self.vertices.append(Point(int(self.vertices[0].x + width), int(self.vertices[0].y + height)))

    def update(self, center, width, height):
        """
        Update the position of the rectangle.
        """
        self.vertices[0].x = int(center.x - (width / 2))
        self.vertices[0].y = int(center.y - (height / 2))
        self.vertices[1].x = int(self.vertices[0].x + width)
        self.vertices[1].y = int(self.vertices[0].y)
        self.vertices[2].x = int(self.vertices[0].x)
        self.vertices[2].y = int(self.vertices[0].y + height)
        self.vertices[3].x = int(self.vertices[0].x + width)
        self.vertices[3].y = int(self.vertices[0].y + height)

    def top_left(self):
        """
        Return the top left point of the rectangle.
        """
        return self.vertices[0]

    def bottom_right(self):
        """
        Return the bottom right point of the rectangle.
        """
        return self.vertices[3]

    def contains(self, point):
        """
        Check if the point is contained within the rectangle.
        """
        if ((point.x > self.vertices[0].x) and (point.x < self.vertices[3].x)) \
                and ((point.y > self.vertices[0].y) and (point.y < self.vertices[3].y)):
            return True
        return False

    def overlap(self, other):
        """
        Check if two rectangles overlap by any margin.
        """
        for vertex in self.vertices:
            if not other.contains(vertex):
                return False
        for vertex in other.vertices:
            if not self.contains(vertex):
                return False
        return True


def distance(point_one, point_two):
    """
    Compute the Euclidean distance between two points.
    """
    return math.sqrt(math.pow(point_one.x - point_two.x, 2) + math.pow(point_one.y - point_two.y, 2))
