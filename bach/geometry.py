
class Point:
    def __init__(self, x, y):
        """
        Default constructor.
        """
        self.x = x
        self.y = y


def inside_box(point, box_upper_left, w, h):
    """
    Check if a point is inside a box.
    """
    if ((point.x > box_upper_left.x) and (point.x < box_upper_left.x + w)) \
            and ((point.y > box_upper_left.y) and (point.y < box_upper_left.y + h)):
        return True
    return False
