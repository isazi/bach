import numpy
import cv2


class Detector:
    def __init__(self, configuration, names, weights):
        """
        Default constructor.
        """
        self.configuration_file = configuration
        self.names_file = names
        self.weights_file = weights
        self.names = None
        self.colors = None
        self.neural_net = None

    def initialize(self):
        """
        Initialize the detector.
        """
        if self.names_file:
            with open(self.names_file) as file:
                self.names = [line.strip() for line in file.readlines()]
        else:
            return False
        self.colors = numpy.random.uniform(0, 255, size=(len(self.names)))
        if self.configuration_file and self.weights_file:
            self.neural_net = cv2.dnn.readNet(self.weights_file, self.configuration_file)
        else:
            return False
        return True
