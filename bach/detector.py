import cv2
import bach.darknet


class Detector:
    def __init__(self, configuration, meta, weights):
        """
        Default constructor.
        """
        self.configuration_file = configuration
        self.meta_file = meta
        self.weights_file = weights

    def initialize(self):
        """
        Initialize the detector.
        """
        if self.configuration_file and self.weights_file:
            bach.darknet.initialize(self.configuration_file, self.weights_file, self.meta_file)
        else:
            return False
        return True

    @staticmethod
    def preprocess_frame(frame):
        """
        Preprocess a frame before detection.
        """
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.resize(processed_frame,
                   (bach.darknet.lib.network_width(bach.darknet.net_main),
                    bach.darknet.lib.network_height(bach.darknet.net_main)),
                   interpolation=cv2.INTER_NEAREST)
        return processed_frame

    @staticmethod
    def process_frame(frame, threshold=0.5):
        """
        Process a frame through the neural network.
        """
        detections = bach.darknet.detect(bach.darknet.net_main,
                                         bach.darknet.meta_main,
                                         frame,
                                         threshold,
                                         threshold)
        return detections
