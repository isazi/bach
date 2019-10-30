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
        self.center = center
        self.width = width
        self.height = height
        self.vertices = list()
        self.vertices.append(Point(int(center.x - (width / 2)), int(center.y - (height / 2))))
        self.vertices.append(Point(int(self.vertices[0].x + width), int(self.vertices[0].y)))
        self.vertices.append(Point(int(self.vertices[0].x), int(self.vertices[0].y + height)))
        self.vertices.append(Point(int(self.vertices[0].x + width), int(self.vertices[0].y + height)))

    def update(self, center, width, height):
        """
        Update the position of the rectangle.
        """
        self.center = center
        self.width = width
        self.height = height
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

    def area(self):
        """
        Computes the area of the rectangle.
        """
        return self.width * self.height

    def contains(self, point):
        """
        Check if the point is contained within the rectangle.
        """
        if ((point.x >= self.vertices[0].x) and (point.x <= self.vertices[3].x)) \
                and ((point.y >= self.vertices[0].y) and (point.y <= self.vertices[3].y)):
            return True
        return False

    def overlap(self, other):
        """
        Check if two rectangles overlap by any margin.
        """
        for vertex in self.vertices:
            if other.contains(vertex):
                return True
        for vertex in other.vertices:
            if self.contains(vertex):
                return True
        return False

    def overlap_area(self, other):
        """
        Measure the area of the overlap between two rectangles.
        """
        inside_vertices = 0
        for vertex in other.vertices:
            if self.contains(vertex):
                inside_vertices = inside_vertices + 1
        width = 0
        height = 0
        if inside_vertices == 1:
            width = min([other.bottom_right().x - self.top_left().x, self.bottom_right().x - other.top_left().x])
            height = min([other.bottom_right().y - self.top_left().y, self.bottom_right().y - other.top_left().y])
        elif inside_vertices == 2:
            width = min(
                [other.bottom_right().x - other.top_left().x,
                 other.bottom_right().x - self.top_left().x,
                 self.bottom_right().x - other.top_left().x]
            )
            height = min(
                [other.bottom_right().y - other.top_left().y,
                 other.bottom_right().y - self.top_left().y,
                 self.bottom_right().y - other.top_left().y]
            )
        elif inside_vertices == 4:
            width = other.width
            height = other.height
        return width * height


def distance(point_one, point_two):
    """
    Compute the Euclidean distance between two points.
    """
    return math.sqrt(math.pow(point_one.x - point_two.x, 2) + math.pow(point_one.y - point_two.y, 2))
