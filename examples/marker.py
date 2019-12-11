import cv2
from cv2 import aruco
import argparse
import bach.video


def initialize_input(arguments):
    if arguments.file:
        video = bach.video.VideoFile(arguments.file)
    else:
        video = bach.video.Webcam(webcam_id=arguments.webcam,
                                  width=arguments.width,
                                  height=arguments.height,
                                  fps=arguments.fps)
    video.initialize()
    return video


parser = argparse.ArgumentParser()
parser.add_argument("--webcam", help="The ID of the webcam", type=int)
parser.add_argument("--file", help="The file containing the video", type=str)
parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
arguments = parser.parse_args()

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
parameters.adaptiveThreshWinSizeMin = 3
parameters.adaptiveThreshWinSizeMax = 60
parameters.adaptiveThreshWinSizeStep = 3
parameters.minMarkerPerimeterRate = 0.004
parameters.maxMarkerPerimeterRate = 0.032
parameters.polygonalApproxAccuracyRate = 0.025
parameters.markerBorderBits = 1
parameters.maxErroneousBitsInBorderRate = 0.40
parameters.errorCorrectionRate = 0.9
parameters.detectInvertedMarker = False

video = initialize_input(arguments)

while video.ready():
    try:
        frame = video.get_frame()
    except ValueError as err:
        print("Error: ".format(str(err)))
        break
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    if ids is not None:
        print("Detections: {}".format(len(ids)))
        for detection in ids:
            print("\tID: {}".format(detection))
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imshow('frame', frame_markers)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
