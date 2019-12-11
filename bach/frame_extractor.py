import argparse
import bach.video


def command_line():
    parser = argparse.ArgumentParser()
    # Devices
    parser.add_argument("--webcam", help="The ID of the webcam", type=int)
    parser.add_argument("--file", help="The file containing the video", type=str)
    parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    # Frame extraction
    parser.add_argument("--reduction", help="The number of frames skipped for every frame stored", type=int, default=1)
    parser.add_argument("--frame_file", help="The base file name for the stored frames", type=str)
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


def __main__():
    arguments = command_line()
    video = initialize_input(arguments)
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    bach.video.frame_extraction(video, arguments.frame_file, arguments.reduction)
    return 0


__main__()
