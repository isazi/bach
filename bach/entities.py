
class Entity:
    def __init__(self, label="", marker=-1, color=(0, 0, 0), width=1, height=1, seen=None):
        """
        Default constructor.
        """
        self.label = label
        self.marker = marker
        self.color = color
        self.width = width
        self.height = height
        self.last_seen = seen
        self.position = None
        self.box = None

    def top_left(self):
        """
        Coordinates of the top left corner of the entity.
        """
        return self.box.top_left()

    def bottom_right(self):
        """
        Coordinates of the bottom right corner of the entity.
        """
        return self.box.bottom_right()

    def contains(self, point):
        """
        Check if the point is contained within the entity.
        """
        return self.box.contains(point)

    def overlap(self, other):
        """
        Check if two entities are overlapping.
        """
        return self.box.overlap(other.box)

    def update_position(self, point):
        """
        Update the position of the entity.
        """
        self.position.x = (self.position.x + point.x) / 2
        self.position.y = (self.position.y + point.y) / 2
        self.box.update(self.position, self.width, self.height)

    def update_size(self, width, height):
        """
        Update the size of the entity.
        """
        self.width = (self.width + width) / 2
        self.height = (self.height + height) / 2
        self.box.update(self.position, self.width, self.height)
