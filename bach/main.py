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
    # Live webcam detection
    parser_lwd = subparsers.add_parser("live_webcam_detection")
    parser_lwd.add_argument("--webcam", help="The ID of the webcam", type=int, required=True)
    parser_lwd.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser_lwd.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser_lwd.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser_lwd.add_argument("--gray", help="Convert input to grayscale", action="store_true")
    parser_lwd.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    parser_lwd.add_argument("--output", help="File where to save the output video", type=str)
    # Recorded video detection
    parser_rvd = subparsers.add_parser("recorded_video_detection")
    parser_rvd.add_argument("--file", help="The file containing the video", type=str, required=True)
    parser_rvd.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser_rvd.add_argument("--gray", help="Convert input to grayscale", action="store_true")
    parser_rvd.add_argument("--output", help="File where to save the output video", type=str)
    return parser.parse_args()


def video_detection(arguments, read_file=False):
    detector = bach.detector.Detector(arguments.config_path, arguments.meta_path, arguments.weights_path)
    code = detector.initialize()
    if not code:
        print("Impossible to initialize darknet.")
        exit(-1)
    if read_file:
        video = bach.video.VideoFile(arguments.file)
    else:
        video = bach.video.Webcam(webcam_id=arguments.webcam,
                                  width=arguments.width,
                                  height=arguments.height,
                                  fps=arguments.fps)
    video.initialize()
    if arguments.output:
        output = bach.video.VideoWriter("{}.mp4".format(arguments.output),
                                        width=video.width,
                                        height=video.height,
                                        fps=video.fps)
        output.initialize()
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
            bach.graphics.draw_bounding_box(processed_frame,
                                            detection[0],
                                            detector.colors[detection[0]],
                                            detection[2][0], detection[2][1], detection[2][2], detection[2][3])
        if arguments.output:
            output.write(processed_frame)
        cv2.imshow("BACH", processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    exit(0)


def __main__():
    arguments = command_line()
    if arguments.action == "live_webcam_detection":
        video_detection(arguments)
    elif arguments.action == "recorded_video_detection":
        video_detection(arguments, read_file=True)


__main__()
