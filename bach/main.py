import argparse
import cv2
import bach.detector
import bach.video
import bach.graphics


def command_line():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")
    # Required files for darknet
    parser.add_argument("-c", "--config_path", help="File containing darknet configuration", type=str, required=True)
    parser.add_argument("-m", "--meta_path", help="File containing darknet metadata", type=str, required=True)
    parser.add_argument("-w", "--weights_path", help="File containing darknet weights", type=str, required=True)
    # Demo
    parser_demo = subparsers.add_parser("demo")
    parser_demo.add_argument("--webcam", help="The ID of the webcam", type=int, required=True)
    parser_demo.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser_demo.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser_demo.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser_demo.add_argument("--gray", help="Convert input to grayscale", type=bool, action="store_true")
    return parser.parse_args()


def demo(arguments):
    detector = bach.detector.Detector(arguments.config_path, arguments.meta_path, arguments.weights_path)
    code = detector.initialize()
    if not code:
        print("Impossible to initialize darknet.")
        exit(-1)
    webcam = bach.video.Webcam(webcam_id=arguments.webcam, width=arguments.width, height=arguments.height)
    webcam.initialize()
    if not webcam.ready():
        print("Impossible to initialize webcam.")
        exit(-1)
    while True:
        try:
            frame = webcam.get_frame(gray=arguments.gray)
        except ValueError as err:
            print("Error: ".format(str(err)))
            exit(-1)
        processed_frame = detector.preprocess_frame(frame)
        detections = detector.process_frame(processed_frame, threshold=arguments.threshold)
        for detection in detections:
            bach.graphics.draw_bounding_box(frame,
                                            detection[0],
                                            0,
                                            detection[2][0], detection[2][1], detection[2][2], detection[2][3])
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    exit(0)


def __main__():
    arguments = command_line()
    if arguments.action == "demo":
        demo(arguments)


__main__()
