import argparse
import bach.video


def command_line():
    parser = argparse.ArgumentParser()
    # Devices
    parser.add_argument("--webcam", help="The ID of the webcam", type=int)
    parser.add_argument("--output", help="The file containing the video", type=str)
    parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    return parser.parse_args()


def __main__():
    arguments = command_line()
    video = bach.video.Webcam(webcam_id=arguments.webcam,
                              width=arguments.width,
                              height=arguments.height,
                              fps=arguments.fps)
    video.initialize()
    if not video.ready():
        print("Impossible to open video source.")
        exit(-1)
    output = bach.video.VideoWriter("{}.mp4".format(arguments.output), arguments.width, arguments.height, arguments.fps)
    output.initialize()
    while video.ready():
        try:
            frame = video.get_frame()
        except ValueError as err:
            print("Error: ".format(str(err)))
            break
        output.write(frame)


__main__()