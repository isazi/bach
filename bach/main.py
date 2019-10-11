import argparse
import cv2
import bach.detector
import bach.video


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
    return parser.parse_args()


def demo(arguments):
    def draw_bounding_box(img, class_name, x, y, x_plus_w, y_plus_h):
        color = 15
        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
        cv2.putText(img, class_name, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

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
            frame = webcam.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            exit(-1)
        processed_frame = detector.preprocess_frame(frame)
        detections = detector.process_frame(processed_frame, threshold=arguments.threshold)
        for detection in detections:
            draw_bounding_box(frame,
                              detection[0],
                              int(detection[2][0] - detection[2][2] / 2),
                              int(detection[2][1] - detection[2][3] / 2),
                              int(detection[2][3]),
                              int(detection[2][2]))
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
