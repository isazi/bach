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
    # Demo webcam
    parser_demo = subparsers.add_parser("demo-webcam")
    parser_demo.add_argument("--webcam", help="The ID of the webcam", type=int, required=True)
    parser_demo.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser_demo.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser_demo.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser_demo.add_argument("--gray", help="Convert input to grayscale", action="store_true")
    # Demo file
    parser_demo = subparsers.add_parser("demo-file")
    parser_demo.add_argument("--file", help="The file containing the video", type=str, required=True)
    parser_demo.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser_demo.add_argument("--gray", help="Convert input to grayscale", action="store_true")
    return parser.parse_args()


def demo(arguments, read_file=False):
    detector = bach.detector.Detector(arguments.config_path, arguments.meta_path, arguments.weights_path)
    code = detector.initialize()
    if not code:
        print("Impossible to initialize darknet.")
        exit(-1)
    if read_file:
        video = bach.video.VideoFile(arguments.file)
    else:
        video = bach.video.Webcam(webcam_id=arguments.webcam, width=arguments.width, height=arguments.height)
    video.initialize()
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    while True:
        try:
            frame = video.get_frame(gray=arguments.gray)
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
    if arguments.action == "demo-webcam":
        demo(arguments)
    elif arguments.action == "demo-file":
        demo(arguments, read_file=True)


__main__()
