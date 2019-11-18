import cv2
from cv2 import aruco
import numpy
from bach import darknet
import bach.geometry


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
            darknet.performDetect(imagePath="",
                                  configPath=self.configuration_file,
                                  weightPath=self.weights_file,
                                  metaPath=self.meta_file,
                                  showImage=False,
                                  initOnly=True)
        else:
            return False
        for name in darknet.altNames:
            # The color is in BGR format
            self.colors[name] = (numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255))
        # Initialize ArUco
        self.aruco_dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.aruco_parameters = aruco.DetectorParameters_create()
        self.aruco_parameters.adaptiveThreshWinSizeMin = 3
        self.aruco_parameters.adaptiveThreshWinSizeMax = 60
        self.aruco_parameters.adaptiveThreshWinSizeStep = 3
        self.aruco_parameters.minMarkerPerimeterRate = 0.004
        self.aruco_parameters.maxMarkerPerimeterRate = 0.032
        self.aruco_parameters.polygonalApproxAccuracyRate = 0.025
        self.aruco_parameters.markerBorderBits = 1
        self.aruco_parameters.maxErroneousBitsInBorderRate = 0.40
        self.aruco_parameters.errorCorrectionRate = 0.9
        self.aruco_parameters.detectInvertedMarker = False
        return True

    @staticmethod
    def preprocess_frame(frame):
        """
        Preprocess a frame before detection.
        """
        processed_frame = frame.copy()
        processed_frame = cv2.resize(processed_frame,
                                     (darknet.lib.network_width(darknet.netMain),
                                      darknet.lib.network_height(darknet.netMain)),
                                     interpolation=cv2.INTER_NEAREST)
        return processed_frame

    @staticmethod
    def detect_objects(frame, threshold=0.5):
        """
        Process a frame through the neural network and return detected objects.
        """
        detections = darknet.detect(darknet.netMain,
                                    darknet.metaMain,
                                    frame,
                                    threshold,
                                    threshold)
        return detections

    def detect_markers(self, frame):
        """
         Detect ArUco markers in a frame.
        """
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dictionary, parameters=self.aruco_parameters)
        markers = dict()
        if ids is not None:
            for index in range(0, len(ids)):
                x = 0
                y = 0
                for point in corners[index][0]:
                    x = x + point[0]
                    y = y + point[1]
                point = bach.geometry.Point(x / 4, y / 4)
                markers[ids[index][0]] = point
        return markers
