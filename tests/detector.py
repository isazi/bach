import cv2
import bach.detector
import bach.video
import bach.graphics

WEBCAM_ID = 0


detector = bach.detector.Detector("/home/alessio/Downloads/2019-10-10/yolo-ants.cfg",
                                  "/home/alessio/Downloads/2019-10-10/yolo-ants.data",
                                  "/home/alessio/Downloads/2019-10-10/yolo-ants_final.weights")
code = detector.initialize()
if not code:
    print("Impossible to initialize darknet.")
    exit(-1)
webcam = bach.video.Webcam(webcam_id=WEBCAM_ID, width=1920, height=1080)
webcam.initialize()
if not webcam.ready():
    exit(-1)
while True:
    try:
        frame = webcam.get_frame()
    except ValueError as err:
        print("Error: ".format(str(err)))
        exit(-1)
    processed_frame = detector.preprocess_frame(frame)
    detections = detector.process_frame(processed_frame, threshold=0.01)
    for detection in detections:
        bach.graphics.draw_bounding_box(frame,
                                        detection[0],
                                        0,
                                        detection[2][0], detection[2][1], detection[2][2], detection[2][3])
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
