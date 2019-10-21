
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
