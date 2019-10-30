import argparse
import cv2
from bach.darknet import set_gpu
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
    parser.add_argument("--gpu", help="ID of the GPU to use for Darknet", type=int, default=0)
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
    parser.add_argument("--ghost_threshold",
                        help="Number of frames without a new detection before the entity becomes a ghost",
                        type=int, default=25)
    parser.add_argument("--marker_distance", help="Maximum distance of a marker from an entity",
                        type=int, default=25)
    parser.add_argument("--max_distance", help="Maximum distance for the new position of an entity",
                        type=int, default=25)
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


def detect_entities(arguments, entities, detections, frame_counter):
    for entity in entities:
        closest_detections = dict()
        for detection in detections:
            new_position = bach.geometry.Point(detection[2][0], detection[2][1])
            new_box = bach.geometry.Rectangle(new_position, detection[2][2], detection[2][3])
            if entity.box.overlap(new_box):
                overlap = max([entity.box.overlap_area(new_box), new_box.overlap_area(entity.box)])
                if arguments.debug:
                    print("\t\tdetection: tl ({}, {}), br ({}, {}), w {}, h {}".format(new_box.top_left().x,
                                                                                       new_box.top_left().y,
                                                                                       new_box.bottom_right().x,
                                                                                       new_box.bottom_right().y,
                                                                                       new_box.width,
                                                                                       new_box.height))
                    print("\t\toverlap: {}".format(overlap))
                closest_detections[overlap] = detection
        if len(closest_detections) > 0:
            detection = closest_detections[max(closest_detections.keys())]
            entity.update_position(bach.geometry.Point(detection[2][0], detection[2][1]))
            entity.update_size(detection[2][2], detection[2][3])
            entity.frame_seen = frame_counter
            detections.remove(detection)
            if arguments.debug:
                print("\tUpdate entity \"{} {}\": new position tl ({}, {}), br ({}, {}), w {}, h {}".format(
                    entity.label, entity.marker, entity.top_left().x, entity.top_left().y, entity.bottom_right().x,
                    entity.bottom_right().y, entity.width, entity.height))


def video_detection(arguments, video):
    set_gpu(arguments.gpu)
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
    named_entities = dict()
    unnamed_entities = list()
    while video.ready():
        try:
            frame = video.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            break
        frame_counter = frame_counter + 1
        if arguments.debug:
            print("Frame: {}".format(frame_counter))
        detections = detector.detect_objects(frame, threshold=arguments.threshold)
        if arguments.debug:
            print("Darknet detections: {}".format(len(detections)))
        # Detect named entities
        detect_entities(arguments, named_entities.values(), detections, frame_counter)
        # Detect unnamed entities
        detect_entities(arguments, unnamed_entities, detections, frame_counter)
        # New entities
        for detection in detections:
            entity = bach.objects.Entity(label=detection[0], color=detector.colors[detection[0]],
                                         width=detection[2][2], height=detection[2][3], seen=frame_counter)
            entity.position = bach.geometry.Point(detection[2][0], detection[2][1])
            entity.box = bach.geometry.Rectangle(entity.position, entity.width, entity.height)
            unnamed_entities.append(entity)
            if arguments.debug:
                print("\tNew entity.")
        # Detect ArUco markers
        aruco_markers = detector.detect_markers(frame)
        if arguments.debug:
            print("ArUco detections: {}".format(len(aruco_markers)))
        for entity in unnamed_entities:
            for label, point in aruco_markers.items():
                if entity.position.distance(point) < arguments.marker_distance:
                    entity.marker = label
                    named_entities[label] = entity
                    unnamed_entities.remove(entity)
                    del aruco_markers[label]
                    break
        # Add detections to frame and eliminate ghosts
        ghosts = list()
        for label, entity in named_entities.items():
            if label != -1:
                bach.graphics.draw_bounding_box(frame, entity)
            if entity.frame_seen < frame_counter - arguments.ghost_threshold:
                ghosts.append(label)
        for ghost in ghosts:
            if arguments.debug:
                print("\tGhost \"{} {}\" deleted.".format(named_entities[ghost].label, named_entities[ghost].marker))
            del named_entities[ghost]
        for entity in unnamed_entities:
            if entity.frame_seen < frame_counter - arguments.ghost_threshold:
                if arguments.debug:
                    print("\tGhost deleted.")
                unnamed_entities.remove(entity)
        if arguments.debug:
            print("Entities: {}".format(len(named_entities)))
            print("Unnamed entities: {}".format(len(unnamed_entities)))
        # Store and show output
        if arguments.output:
            output.write(frame)
        cv2.imshow("BACH", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if arguments.debug:
            print()
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
