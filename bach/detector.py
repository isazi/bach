import cv2
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

    def initialize(self):
        """
        Initialize the detector.
        """
        if self.configuration_file and self.weights_file:
            darknet.initialize(self.configuration_file, self.weights_file, self.meta_file)
        else:
            return False
        for name in darknet.alt_names:
            # The color is in BGR format
            self.colors[name] = (numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255),
                                 numpy.random.randint(0, 255))
        return True

    @staticmethod
    def preprocess_frame(frame):
        """
        Preprocess a frame before detection.
        """
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.resize(processed_frame,
                   (darknet.lib.network_width(darknet.net_main),
                    darknet.lib.network_height(darknet.net_main)),
                   interpolation=cv2.INTER_NEAREST)
        return processed_frame

    @staticmethod
    def process_frame(frame, threshold=0.5):
        """
        Process a frame through the neural network.
        """
        detections = darknet.detect(darknet.net_main,
                                    darknet.meta_main,
                                    frame,
                                    threshold,
                                    threshold)
        return detections
