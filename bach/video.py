import cv2
import threading
import queue


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
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            return frame


class Webcam(Video):
    def __init__(self, webcam_id=0, width=640, height=480, fps=25):
        """
        Default constructor.
        """
        super().__init__()
        self.webcam_id = webcam_id
        self.width = width
        self.height = height
        self.fps = fps

    def initialize(self):
        """
        Initialize capture device.
        """
        self.video = cv2.VideoCapture(self.webcam_id)
        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.video.set(cv2.CAP_PROP_FPS, self.fps)
        self.video.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.video.set(cv2.CAP_PROP_AUTO_WB, 1)
        self.video.set(cv2.CAP_PROP_BRIGHTNESS, 130)


class VideoFile(Video):
    def __init__(self, file):
        """
        Default constructor.
        """
        super().__init__()
        self.filename = file
        self.width = 0
        self.height = 0
        self.fps = 0

    def initialize(self):
        """
        Open video file.
        """
        if self.filename:
            self.video = cv2.VideoCapture(self.filename)
            self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.video.get(cv2.CAP_PROP_FPS))


class VideoWriter:
    def __init__(self, file, width=640, height=480, fps=25):
        """
        Default constructor.
        """
        self.file = file
        self.width = width
        self.height = height
        self.fps = fps
        self.out = None

    def __del__(self):
        """
        Default destructor.
        """
        if self.out:
            self.out.release()

    def initialize(self):
        """
        Open output file and initialize video codec.
        """
        self.out = cv2.VideoWriter(self.file,
                                   cv2.VideoWriter_fourcc("m", "p", "4", "v"),
                                   self.fps,
                                   (self.width, self.height))

    def write(self, frame):
        """
        Save a frame in the file.
        """
        self.out.write(frame)


class VideoReader(threading.Thread):
    def __init__(self, video, buffer, timeout):
        threading.Thread.__init__(self)
        self.video = video
        self.queue = buffer
        self.timeout = timeout
        self.terminate = False

    def run(self):
        while self.video.ready():
            try:
                frame = self.video.get_frame()
                self.queue.put(frame, timeout=self.timeout)
            except ValueError as err:
                print("Error: ".format(str(err)))
                break
            except queue.Full:
                print("Error: queue full")
            if self.terminate:
                break


def frame_extraction(video, output_file, reduction=5):
    """
    Extract frames from a video and store them as images.
    """
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    frame_counter = 0
    while video.ready():
        try:
            frame = video.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            break
        if frame_counter % reduction == 0:
            cv2.imwrite("{}_{}.png".format(output_file, frame_counter), frame)
        frame_counter = frame_counter + 1
