import cv2
from cv2 import aruco
import numpy
from bach import darknet


class Detector:
    def __init__(self, configuration, meta, weights):
        """
        Default constructor.
        """
        self.configuration_file = configuration
        self.meta_file = meta
        self.weights_file = weights
        self.colors = dict()
        self.aruco_dictionary = None
        self.aruco_parameters = None

    def initialize(self):
        """
        Initialize the detector.
        """
        # Initialize Darknet
        if self.configuration_file and self.weights_file:
            darknet.initialize(self.configuration_file, self.weights_file, self.meta_file)
        else:
            return False
        for name in darknet.alt_names:
            # The color is in BGR format
            self.colors[name] = (numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255))
        # Initialize ArUco
        self.aruco_dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        return True

    @staticmethod
    def preprocess_frame(frame):
        """
        Preprocess a frame before detection.
        """
        processed_frame = frame.copy()
        processed_frame = cv2.resize(processed_frame,
                                     (darknet.lib.network_width(darknet.net_main),
                                      darknet.lib.network_height(darknet.net_main)),
                                     interpolation=cv2.INTER_NEAREST)
        return processed_frame

    @staticmethod
    def detect_objects(frame, threshold=0.5):
        """
        Process a frame through the neural network and return detected objects.
        """
        detections = darknet.detect(darknet.net_main,
                                    darknet.meta_main,
                                    frame,
                                    threshold,
                                    threshold)
        return detections

    def detect_markers(self, frame):
        """
         Detect ArUco markers in a frame.
        """
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dictionary, parameters=self.aruco_parameters)
        return corners, ids
