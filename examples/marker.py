import cv2
from cv2 import aruco
import bach.video


WEBCAM_ID = 0
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
parameters.adaptiveThreshWinSizeMin = 3
parameters.adaptiveThreshWinSizeMax = 60
parameters.adaptiveThreshWinSizeStep = 3
parameters.minMarkerPerimeterRate = 0.004
parameters.maxMarkerPerimeterRate = 0.032
parameters.markerBorderBits = 1
parameters.maxErroneousBitsInBorderRate = 0.40
parameters.errorCorrectionRate = 0.9
parameters.detectInvertedMarker = False
webcam = bach.video.Webcam(webcam_id=WEBCAM_ID, width=1920, height=1088)
webcam.initialize()

if not webcam.ready():
    exit(-1)

while webcam.ready():
    try:
        frame = webcam.get_frame()
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
