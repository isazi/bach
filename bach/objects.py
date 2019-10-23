from bach.geometry import Point


class Entity:
    def __init__(self, label="", marker=-1, color=(0, 0, 0), width=1, height=1):
        """
        Default constructor.
        """
        self.label = label
        self.marker = marker
        self.color = color
        self.width = width
        self.height = height
        self.position = None

    def top_left(self):
        """
        Coordinates of the top left corner of the entity.
        """
        return Point(int(self.position.x - (self.width / 2)), int(self.position.y - (self.height / 2)))

    def bottom_right(self):
        """
        Coordinates of the bottom right corner of the entity.
        """
        return Point(int(self.position.x + (self.width / 2)), int(self.position.y + (self.height / 2)))

    def contains(self, point):
        """
        Check if the point is contained within the entity.
        """
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        if ((point.x > top_left.x) and (point.x < bottom_right.x)) \
                and ((point.y > top_left.y) and (point.y < bottom_right.y)):
            return True
        return False

    def update_position(self, point):
        """
        Update the position of the entity.
        """
        self.position.x = (self.position.x + point.x) / 2
        self.position.y = (self.position.y + point.y) / 2

    def update_size(self, width, height):
        """
        Update the size of the entity.
        """
        self.width = (self.width + width) / 2
        self.height = (self.height + height) / 2
