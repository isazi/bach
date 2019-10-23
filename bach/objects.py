
class Entity:
    def __init__(self, label="", color_id=0, width=1, height=1):
        """
        Default constructor.
        """
        self.label = label
        self.color_id = color_id
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

    def contains(self, point):
        """
        Check if the point is contained within the entity.
        """
        top_left = self.top_left()
        bottom_right = self.bottom_right()
        if ((point.x > top_left[0]) and (point.x < top_left[0] + self.width)) \
                and ((point.y > bottom_right[1]) and (point.y < bottom_right[1] + self.height)):
            return True
        return False

    def update_position(self, point):
        """
        Update the position of the entity.
        """
        self.position.x = (self.position.x + point.x) / 2
        self.position.y = (self.position.y + point.y) / 2
