import cv2


class Video:
    def __init__(self):
        """
        Default constructor.
        """
        self.video = None

    def __del__(self):
        """
        Default destructor.
        """
        if self.video:
            self.video.release()

    def ready(self):
        """
        Check if the video is ready.
        """
        if self.video:
            return self.video.isOpened()

    def get_frame(self, gray=False):
        """
        Return the current frame from the video.
        """
        if self.video:
            code, frame = self.video.read()
            if not code:
                raise ValueError("Impossible to retrieve current frame.")
            if gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame


class Webcam(Video):
    def __init__(self, webcam_id=0, width=640, height=480):
        """
        Default constructor.
        """
        super().__init__()
        self.webcam_id = webcam_id
        self.width = width
        self.height = height

    def initialize(self):
        """
        Initialize capture device.
        """
        self.video = cv2.VideoCapture(self.webcam_id)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)


class VideoFile(Video):
    def __init__(self, file):
        """
        Default constructor.
        """
        super().__init__()
        self.filename = file
        self.width = 0
        self.height = 0

    def initialize(self):
        """
        Open video file.
        """
        if self.filename:
            self.video = cv2.VideoCapture(self.filename)
            self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

class VideoWriter():
    def __init__(self, file, width=640, height=480):
        """
        Default constructor.
        """
        self.file = file
        self.width = width
        self.height = height
        self.out = None

    def __del__(self):
        """
        Default destructor.
        """
        self.file.release()

    def initialize(self):
        """
        Open output file and initialize video codec.
        """
        self.out = cv2.VideoWriter(self.file, cv2.VideoWriter_fourcc("M", "P", "4", "2"), 25, (self.width, self.height))

    def write(self, frame):
        """
        Save a frame in the file.
        """
        self.out.write(frame)
