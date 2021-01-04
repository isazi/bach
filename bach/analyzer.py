import argparse
import bach.geometry
import bach.entities
import bach.behavior


def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="The file containing the position of entities", required=True, type=str)
    # Debug
    parser.add_argument("--debug", help="Debug mode", action="store_true")
    return parser.parse_args()


def analysis(arguments, input_file):
    entities = dict()
    encounters = list()
    for line in input_file:
        if line[0] == "#":
            continue
        items = line.split(sep=" ")
        frame_counter = int(items[0])
        new_point = bach.geometry.Point(float(items[2]), float(items[3]))
        if items[1] in entities:
            entities[items[1]].update_position(new_point, float(items[4]), float(items[5]))
            entities[items[1]].last_seen = frame_counter
        else:
            entity = bach.entities.Entity(marker=int(items[1]),
                                          width=float(items[4]),
                                          height=float(items[5]),
                                          seen=frame_counter)
            entity.box = bach.geometry.Rectangle(new_point, float(items[4]), float(items[5]))
            entities[items[1]] = entity
        # Entity's average speed
        for entity in entities:
            print(entity)
        # Clean up
        if arguments.debug:
            print("# Entities: {}".format(len(entities)))
        if arguments.debug:
            print()


def __main__():
    arguments = command_line()
    input_file = open(arguments.file)
    if not input_file:
        print("Impossible to open input file")
        exit(-1)
    analysis(arguments, input_file)
    input_file.close()
    return 0


__main__()
