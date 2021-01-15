import cv2
from cv2 import aruco
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
        # Darknet
        self.network = None
        self.classes = None
        self.colors = None
        # ArUCO
        self.aruco_dictionary = None
        self.aruco_parameters = None

    def initialize(self):
        """
        Initialize the detector.
        """
        # Initialize Darknet
        if self.configuration_file and self.weights_file:
            self.network, self.classes, self.colors = darknet.load_network(self.configuration_file,
                                                                           self.meta_file,
                                                                           self.weights_file)
        else:
            return False
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

    def preprocess_frame(self, frame):
        """
        Preprocess a frame before detection.
        """
        processed_frame = frame.copy()
        processed_frame = cv2.resize(processed_frame,
                                     (darknet.lib.network_width(self.network),
                                      darknet.lib.network_height(self.network)),
                                     interpolation=cv2.INTER_NEAREST)
        return processed_frame

    def detect_objects(self, frame, threshold=0.5):
        """
        Process a frame through the neural network and return detected objects.
        """
        processed_image = darknet.make_image(darknet.network_width(self.network),
                                             darknet.network_height(self.network),
                                             3)
        darknet.copy_image_from_bytes(processed_image, frame.tobytes())
        detections = darknet.detect_image(self.network,
                                          self.classes,
                                          processed_image,
                                          thresh=threshold,
                                          hier_thresh=threshold)
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
