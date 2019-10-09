import cv2


class Webcam:
    def __init__(self, webcam_id=0, width=640, height=480):
        """Default constructor."""
        self.webcam_id = webcam_id
        self.width = width
        self.height = height
        self.webcam = None

    def __del__(self):
        """Default destructor."""
        self.webcam.release()

    def initialize(self):
        """Initialize capture device."""
        self.webcam = cv2.VideoCapture(self.webcam_id)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def ready(self):
        """Check if the webcam is ready to stream."""
        return self.webcam.isOpened()

    def get_width(self):
        """Retrieve the image width."""
        return self.width

    def get_height(self):
        """Retrieve the image height."""
        return self.height

    def get_frame(self, gray=False):
        """Return the current frame from the webcam."""
        code, frame = self.webcam.read()
        if not code:
            raise ValueError("Impossible to retrieve the frame.")
        if gray:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame
