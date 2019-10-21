
class Entity:
    def __init__(self, label="", width=1, height=1):
        """
        Default constructor.
        """
        self.label = label
        self.width = width
        self.height = height
        self.position = None

    def top_left(self):
        """
        Coordinates of the top left corner of the entity.
        """
        return int(self.position.x - (self.width / 2)), int(self.position.y - (self.height / 2))

    def bottom_right(self):
        """
        Coordinates of the bottom right corner of the entity.
        """
        return int(self.position.x + (self.width / 2)), int(self.position.y + (self.height / 2))

    def is_inside(self, point):
        """
        Check if a point is inside the entity.
        """
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        if ((point.x > top_left[0]) and (point.x < top_left[0] + self.width)) \
                and ((point.y > bottom_right[1]) and (point.y < bottom_right[1] + self.height)):
            return True
        return False
