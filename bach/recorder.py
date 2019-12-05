import argparse
import queue
import bach.video


def command_line():
    parser = argparse.ArgumentParser()
    # Devices
    parser.add_argument("--webcam", help="The ID of the webcam", type=int)
    parser.add_argument("--output", help="The file containing the video", type=str)
    parser.add_argument("--width", help="Webcam's resolution width", type=int, default=640)
    parser.add_argument("--height", help="Webcam's resolution height", type=int, default=480)
    parser.add_argument("--fps", help="Set the frames per second", type=int, default=25)
    parser.add_argument("--frames", help="The number of frames to record", type=int)
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
    frame_queue = queue.Queue()
    video_reader = bach.video.VideoReader(video, frame_queue)
    video_reader.start()
    frame_counter = 0
    while frame_counter < arguments.frames:
        try:
            frame = frame_queue.get(timeout=5)
            frame_counter = frame_counter + 1
        except queue.Empty:
            break
        output.write(frame)
    if video.ready():
        video_reader.terminate = True
    video_reader.join()


__main__()
