import cv2
import bach.video

WEBCAM_ID = 0


webcam = bach.video.Webcam(webcam_id=WEBCAM_ID, width=1920, height=1080)
webcam.initialize()

if webcam.ready():
    print("Webcam")
    print("\tResolution: {}x{}".format(webcam.width, webcam.height))

while webcam.ready():
    try:
        frame = webcam.get_frame()
    except ValueError as err:
        print("Error: ".format(str(err)))
        exit(-1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    try:
        frame = webcam.get_frame(gray=True)
    except ValueError as err:
        print("Error: ".format(str(err)))
        exit(-1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
