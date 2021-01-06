from math import isclose
import bach.geometry


class Entity:
    def __init__(self, label="", marker=-1, color=(0, 0, 0), width=1, height=1, seen=1):
        """
        Default constructor.
        """
        self.label = label
        self.color = color
        self.width = width
        self.height = height
        self.last_seen = seen
        self.first_seen = seen
        self.detections = 1
        self.markers = dict()
        self.markers[marker] = 1
        self.box = None
        self.distance = 0
        self.speed = 0.0

    def position(self):
        """
        Return the position of the entity.
        """
        return self.box.center

    def marker(self):
        """
        Return the current best marker.
        """
        max_marker = max(self.markers.values())
        for key, value in self.markers.items():
            if value == max_marker:
                return key

    def same(self, other):
        """
        Check if two entities are the same.
        """
        if self.label == other.label and self.marker() == other.marker():
            if isclose(self.position().x, other.position().x) and isclose(self.position().y, other.position().y):
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

    def update_marker(self, marker):
        """
        Update the marker associated with an entity.
        """
        try:
            self.markers[marker] = self.markers[marker] + 1
        except KeyError:
            self.markers[marker] = 1

    def update_position(self, point, width, height, seen):
        """
        Update the position of the entity.
        """
        new_position = point
        self.width = width
        self.height = height
        self.distance = self.distance + bach.geometry.distance(self.position(), new_position)
        if (seen - self.last_seen) > 0:
            self.speed = bach.geometry.distance(self.position(), new_position) / (seen - self.last_seen)
        self.box.update(new_position, self.width, self.height)
        self.last_seen = seen
        self.detections = self.detections + 1

    def average_speed(self):
        """
        Return the average speed of the entity, in pixels per frame.
        """
        return self.distance / (self.last_seen - self.first_seen)
