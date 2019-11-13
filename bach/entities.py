from math import isclose


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
        self.detections = 1
        self.position = None
        self.box = None

    def same(self, other):
        """
        Check if two entities are the same.
        """
        if self.label == other.label and self.marker == other.marker:
            if isclose(self.position.x, other.position.x) and isclose(self.position.y, other.position.y):
                return True
        return False

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

    def update_position(self, point, average=False):
        """
        Update the position of the entity.
        """
        if average:
            self.position.x = self.position.x + ((point.x - self.position.x) / self.detections)
            self.position.y = self.position.y + ((point.y - self.position.y) / self.detections)
        else:
            self.position.x = point.x
            self.position.y = point.y
        self.box.update(self.position, self.width, self.height)

    def update_size(self, width, height, average=False):
        """
        Update the size of the entity.
        """
        if average:
            self.width = self.width + ((width - self.width) / self.detections)
            self.height = self.height + ((height - self.height) / self.detections)
        else:
            self.width = width
            self.height = height
        self.box.update(self.position, self.width, self.height)
