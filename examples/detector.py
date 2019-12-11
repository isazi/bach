import cv2
import bach.detector
import bach.video
import bach.graphics

WEBCAM_ID = 0


detector = bach.detector.Detector("yolo.cfg",
                                  "yolo.data",
                                  "yolo.weights")
code = detector.initialize()
if not code:
    print("Impossible to initialize darknet.")
    exit(-1)

webcam = bach.video.Webcam(webcam_id=WEBCAM_ID, width=1920, height=1080)
webcam.initialize()

while webcam.ready():
    try:
        frame = webcam.get_frame()
    except ValueError as err:
        print("Error: ".format(str(err)))
        break
    detections = detector.detect_objects(frame, threshold=0.25)
    aruco_boxes, aruco_ids = detector.detect_markers(frame)
    for detection in detections:
        bach.graphics.draw_bounding_box(frame,
                                        detection[0],
                                        detector.colors[detection[0]],
                                        detection[2][0], detection[2][1], detection[2][2], detection[2][3])
    frame = cv2.aruco.drawDetectedMarkers(frame, aruco_boxes, aruco_ids)
    cv2.imshow('Detector Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
