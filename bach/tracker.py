import argparse
import cv2
import queue
import time
from bach.darknet import set_gpu
import bach.detector
import bach.video
import bach.graphics
import bach.geometry
import bach.entities
import bach.behavior


def command_line():
    parser = argparse.ArgumentParser()
    # Devices
    parser.add_argument("--gpu", help="ID of the GPU to use for Darknet", type=int, default=0)
    parser.add_argument("--webcam", help="The ID of the webcam", type=int)
    parser.add_argument("--file", help="The file containing the video", type=str)
    parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    parser.add_argument("--video_output", help="File where to store the output video", type=str)
    parser.add_argument("--timeout", help="Timeout for the buffer", type=int, default=5)
    parser.add_argument("--buffer", help="The buffer size", type=int, default=25)
    # Darknet
    parser.add_argument("-c", "--config_path", help="File containing darknet configuration", type=str)
    parser.add_argument("-m", "--meta_path", help="File containing darknet metadata", type=str)
    parser.add_argument("-w", "--weights_path", help="File containing darknet weights", type=str)
    # Detection
    parser.add_argument("--show_video", help="Show video during detection", action="store_true")
    parser.add_argument("--video_width", help="Width of the shown video", type=int, default=0)
    parser.add_argument("--video_height", help="Height of the shown video", type=int, default=0)
    parser.add_argument("--threshold", help="Detection threshold", type=float, default=0.5)
    parser.add_argument("--ghost_threshold",
                        help="Number of frames without a new detection before the entity becomes a ghost",
                        type=int, default=25)
    parser.add_argument("--output_file", help="File where BACH output is stored", type=str)
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


def initialize_output(name, width, height, fps):
    video = bach.video.VideoWriter("{}.mp4".format(name), width, height, fps)
    video.initialize()
    return video


def detect_entities(arguments, entities, detections, frame_counter):
    detection_id = 0
    votes = list()
    for detection in detections:
        new_box = bach.geometry.Rectangle(bach.geometry.Point(detection[2][0], detection[2][1]),
                                          detection[2][2],
                                          detection[2][3])
        if arguments.debug:
            print("#\tDetection: tl ({}, {}), br ({}, {}), w {}, h {}".format(new_box.top_left().x,
                                                                              new_box.top_left().y,
                                                                              new_box.bottom_right().x,
                                                                              new_box.bottom_right().y,
                                                                              new_box.width,
                                                                              new_box.height))
        # Entities express interest for close detections
        for entity in entities:
            if entity.box.overlap(new_box):
                overlap = entity.box.overlap_area(new_box)
                if arguments.debug:
                    print("#\t\tEntity \"{} {}\" overlap: {}".format(entity.label, entity.marker(), overlap))
                votes.append((overlap, entity, detection_id))
        detection_id = detection_id + 1
    votes.sort(key=lambda item: item[0], reverse=True)
    assigned_detections = set()
    assigned_entities = set()
    for vote in votes:
        detection = vote[2]
        entity = vote[1]
        if (detections[detection] not in assigned_detections) and (entity not in assigned_entities):
            assigned_detections.add(detections[detection])
            assigned_entities.add(entity)
            entity.update_position(bach.geometry.Point(detections[detection][2][0],
                                                       detections[detection][2][1]),
                                   detections[detection][2][2],
                                   detections[detection][2][3],
                                   frame_counter
                                   )
            if arguments.debug:
                print("#\tUpdate entity \"{} {}\": new position tl ({}, {}), br ({}, {}), w {}, h {}".format(
                    entity.label, entity.marker(), entity.top_left().x, entity.top_left().y, entity.bottom_right().x,
                    entity.bottom_right().y, entity.width, entity.height))
    for detection in assigned_detections:
        detections.remove(detection)


def detect_aruco(arguments, aruco_markers, entities):
    votes = list()
    for label, point in aruco_markers.items():
        if arguments.debug:
            print("#\tArUco detection: {}".format(label))
        for entity in entities:
            if entity.contains(point):
                if arguments.debug:
                    print("#\t\tArUco overlap \"{} {}\": {}".format(entity.label, entity.marker(), label))
                votes.append((entity.position().distance(point), label, entity))
    votes.sort(key=lambda item: item[0])
    assigned_labels = set()
    assigned_entities = set()
    for vote in votes:
        label = vote[1]
        entity = vote[2]
        if (label not in assigned_labels) and (entity not in assigned_entities):
            entity.update_marker(label)
            assigned_labels.add(label)
            assigned_entities.add(entity)
            if arguments.debug:
                print("#\tUpdate entity \"{} {}\": new label {}".format(entity.label, entity.marker(), label))


def video_detection(arguments, video_queue, output_file):
    set_gpu(arguments.gpu)
    detector = bach.detector.Detector(arguments.config_path, arguments.meta_path, arguments.weights_path)
    return_code = detector.initialize()
    if not return_code:
        print("Impossible to initialize darknet.")
        exit(-1)
    video_output = None
    if arguments.video_output:
        video_output = initialize_output(arguments.video_output, arguments.width, arguments.height, arguments.fps)
    frame_counter = 0
    entities = list()
    while True:
        try:
            frame = video_queue.get(timeout=arguments.timeout)
            video_queue.task_done()
            if arguments.debug:
                print("# Queue size: {}".format(video_queue.qsize()))
        except queue.Empty:
            break
        if arguments.debug:
            print("# Frame: {}".format(frame_counter))
        detections = detector.detect_objects(frame, threshold=arguments.threshold)
        if arguments.debug:
            print("# Darknet detections: {}".format(len(detections)))
        # Detect entities
        detect_entities(arguments, entities, detections, frame_counter)
        # New entities
        for detection in detections:
            entity = bach.entities.Entity(label=detection[0], color=detector.colors[detection[0]],
                                          width=detection[2][2], height=detection[2][3], seen=frame_counter)
            entity.box = bach.geometry.Rectangle(bach.geometry.Point(detection[2][0], detection[2][1]),
                                                 entity.width,
                                                 entity.height)
            entities.append(entity)
            if arguments.debug:
                print("#\tNew entity \"{} {}\": position tl ({}, {}), br ({}, {}), w {}, h {}".format(
                    entity.label, entity.marker(), entity.top_left().x, entity.top_left().y, entity.bottom_right().x,
                    entity.bottom_right().y, entity.width, entity.height))
        # Detect ArUco markers
        aruco_markers = detector.detect_markers(frame)
        if arguments.debug:
            print("# ArUco detections: {}".format(len(aruco_markers)))
        detect_aruco(arguments, aruco_markers, entities)
        # Add detections to frame and eliminate ghosts
        for entity in entities:
            bach.graphics.draw_bounding_box(frame, entity)
            if entity.last_seen < frame_counter - arguments.ghost_threshold:
                if arguments.debug:
                    print("#\tGhost \"{} {}\" deleted".format(entity.label,
                                                              entity.marker()))
                entities.remove(entity)
        if arguments.debug:
            print("# Entities: {}".format(len(entities)))
        # Store and show output
        for entity in entities:
            if not arguments.debug and entity.marker() == -1:
                continue
            output_file.write("{} {} {} {} {} {}\n".format(frame_counter,
                                                           entity.marker(),
                                                           entity.position().x,
                                                           entity.position().y,
                                                           entity.width,
                                                           entity.height))
        if arguments.video_output:
            video_output.write(frame)
        if arguments.show_video:
            if (arguments.video_width > 0) and (arguments.video_height > 0):
                cv2.imshow("BACH", bach.graphics.resize(frame, arguments.video_width, arguments.video_height))
            else:
                cv2.imshow("BACH", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if arguments.debug:
            print()
        frame_counter = frame_counter + 1
    cv2.destroyAllWindows()


def __main__():
    arguments = command_line()
    video = initialize_input(arguments)
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    if arguments.output_file is None:
        print("Impossible to save output.")
        exit(-1)
    output_file = open(arguments.output_file, "w")
    output_file.write("# {}\n".format(time.strftime("%d/%m/%Y %H:%M:%S")))
    output_file.write("# time id x y width height\n")
    frame_queue = queue.Queue(maxsize=arguments.buffer)
    video_reader = bach.video.VideoReader(video, frame_queue, arguments.timeout)
    video_reader.start()
    video_detection(arguments, frame_queue, output_file)
    if video.ready():
        video_reader.terminate = True
    video_reader.join()
    output_file.close()
    return 0


__main__()
