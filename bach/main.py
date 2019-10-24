import argparse
import cv2
import bach.detector
import bach.video
import bach.graphics
import bach.geometry
import bach.objects


def command_line():
    parser = argparse.ArgumentParser()
    # Actions
    parser.add_argument("--action",
                        help="The action to perform",
                        choices=["detection", "frame_extraction"],
                        required=True)
    # Devices
    parser.add_argument("--webcam", help="The ID of the webcam", type=int)
    parser.add_argument("--file", help="The file containing the video", type=str)
    parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    parser.add_argument("--output", help="File where to save the output video", type=str)
    # Darknet
    parser.add_argument("-c", "--config_path", help="File containing darknet configuration", type=str)
    parser.add_argument("-m", "--meta_path", help="File containing darknet metadata", type=str)
    parser.add_argument("-w", "--weights_path", help="File containing darknet weights", type=str)
    # Detection
    parser.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser.add_argument("--min_frames", help="Frame detection threshold", type=int, default=10)
    # Frame extraction
    parser.add_argument("--reduction", help="The number of frames skipped for every frame stored", type=int, default=1)
    # Debug
    parser.add_argument("--debug", help="Debug mode", action="store_true")
    return parser.parse_args()


def initialize_input(arguments):
    """
    Initialize the input.
    """
    if arguments.file:
        video = bach.video.VideoFile(arguments.file)
    else:
        video = bach.video.Webcam(webcam_id=arguments.webcam,
                                  width=arguments.width,
                                  height=arguments.height,
                                  fps=arguments.fps)
    video.initialize()
    return video


def video_detection(arguments, video):
    detector = bach.detector.Detector(arguments.config_path, arguments.meta_path, arguments.weights_path)
    return_code = detector.initialize()
    if not return_code:
        print("Impossible to initialize darknet.")
        exit(-1)
    output = None
    if arguments.output:
        output = bach.video.VideoWriter("{}.mp4".format(arguments.output),
                                        width=video.width,
                                        height=video.height,
                                        fps=video.fps)
        output.initialize()
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    frame_counter = 0
    entities = list()
    while video.ready():
        try:
            frame = video.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            break
        frame_counter = frame_counter + 1
        # Detect entities
        detections = detector.detect_objects(frame, threshold=arguments.threshold)
        for entity in entities:
            for detection in detections:
                new_position = bach.geometry.Point(detection[2][0], detection[2][1])
                if entity.contains(new_position):
                    entity.update_position(new_position)
                    entity.update_size(detection[2][2], detection[2][3])
                    entity.detections = entity.detections + 1
                    detections.remove(detection)
                    break
        for detection in detections:
            entity = bach.objects.Entity(label=detection[0], color=detector.colors[detection[0]],
                                         width=detection[2][2], height=detection[2][3])
            entity.position = bach.geometry.Point(detection[2][0], detection[2][1])
            entities.append(entity)
        # Detect ArUco markers
        aruco_markers = detector.detect_markers(frame)
        for entity in entities:
            for label, point in aruco_markers.items():
                if entity.contains(point):
                    entity.marker = label
                    del aruco_markers[label]
                    break
        # Add detections to frame and eliminate ghosts
        for entity in entities:
            if entity.detections > arguments.min_frames:
                bach.graphics.draw_bounding_box(frame, entity)
            else:
                if frame_counter % 100 == 0:
                    entities.remove(entity)
                    if arguments.debug:
                        print("Ghost deleted.")
        # Store and show output
        if arguments.output:
            output.write(frame)
        cv2.imshow("BACH", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def frame_extraction(arguments, video):
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    frame_counter = 0
    while video.ready():
        try:
            frame = video.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            break
        if frame_counter % arguments.reduction == 0:
            cv2.imwrite("{}_{}.png".format(arguments.output, frame_counter), frame)
        frame_counter = frame_counter + 1


def __main__():
    arguments = command_line()
    video = initialize_input(arguments)
    if arguments.action == "detection":
        video_detection(arguments, video)
    elif arguments.action == "frame_extraction":
        frame_extraction(arguments, video)
    return 0


__main__()
