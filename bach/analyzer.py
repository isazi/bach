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
    for line in input_file:
        if line[0] == "#":
            continue
        items = line.split(sep=" ")
        frame_counter = int(items[0])
        entity_id = int(items[1])
        new_point = bach.geometry.Point(float(items[2]), float(items[3]))
        if entity_id in entities:
            entities[entity_id].update_position(new_point, float(items[4]), float(items[5]), frame_counter)
        else:
            entity = bach.entities.Entity(marker=entity_id,
                                          width=float(items[4]),
                                          height=float(items[5]),
                                          seen=frame_counter)
            entity.box = bach.geometry.Rectangle(new_point, float(items[4]), float(items[5]))
            entities[entity_id] = entity
        # Entity's current speed
        if entity_id != -1:
            print("{} {} {}".format(frame_counter, entity_id, entities[entity_id].speed))
    # Entity's average speed
    for entity_id in entities:
        if entity_id != -1:
            print("{} {}".format(entity_id, entities[entity_id].average_speed()))
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
