import cv2
from cv2 import aruco
import bach.video


WEBCAM_ID = 0
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()
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
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imshow('frame', frame_markers)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
