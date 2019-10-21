
class Entity:
    def __init__(self, label="", width=1, height=1):
        """
        Default constructor.
        """
        self.label = label
        self.width = width
        self.height = height
        self.position = None
