import argparse
import bach.geometry
import bach.entities
import bach.behavior


def command_line():
    parser = argparse.ArgumentParser()
    # Input file
    parser.add_argument("--input_file", help="The file containing the position of individuals", required=True, type=str)
    # Distance file
    parser.add_argument("--distance_file", help="Output file containing the distance between individuals", type=str,
                        default=None)
    # Debug
    parser.add_argument("--debug", help="Debug mode", action="store_true")
    return parser.parse_args()


def analysis(arguments, input_file):
    previous_frame = 0
    entities = dict()
    distances = dict()
    distance_file = None
    if arguments.distance_file is not None:
        distance_file = open(arguments.distance_file, "w+")
        distance_file.write("# frame id id distance\n")
    print("# frame id speed distance")
    for line in input_file:
        if line[0] == "#":
            continue
        items = line.split(sep=" ")
        frame_id = int(items[0])
        entity_id = int(items[1])
        new_point = bach.geometry.Point(float(items[2]), float(items[3]))
        distance = 0.0
        if entity_id in entities:
            distance = bach.geometry.distance(new_point, entities[entity_id].position())
            entities[entity_id].update_position(new_point, float(items[4]), float(items[5]), frame_id)
        else:
            entity = bach.entities.Entity(marker=entity_id,
                                          width=float(items[4]),
                                          height=float(items[5]),
                                          seen=frame_id)
            entity.box = bach.geometry.Rectangle(new_point, float(items[4]), float(items[5]))
            entities[entity_id] = entity
        # Output distance
        if arguments.distance_file is not None:
            if frame_id > previous_frame:
                for pair in distances:
                    distance_file.write("{} {} {}\n".format(previous_frame, pair, distances[pair]))
                distances.clear()
        # Output distance travelled and speed
        if entity_id != -1:
            print("{} {} {} {}".format(frame_id, entity_id, entities[entity_id].speed, distance))
        # Update distances
        if (arguments.distance_file is not None) and (entity_id != -1):
            for other_id in entities:
                if (entity_id != other_id) and (other_id != -1):
                    if entity_id < other_id:
                        distances["{} {}".format(entity_id, other_id)] = \
                            bach.geometry.distance(entities[entity_id].position(), entities[other_id].position())
                    else:
                        distances["{} {}".format(other_id, entity_id)] = \
                            bach.geometry.distance(entities[entity_id].position(), entities[other_id].position())
        previous_frame = frame_id
    print("\n\n")
    # Entity's average speed and total distance
    print("# id average_speed total_distance")
    for entity_id in entities:
        if entity_id != -1:
            print("# {} {} {}".format(entity_id, entities[entity_id].average_speed(), entities[entity_id].distance))
    # Clean up
    if arguments.distance_file is not None:
        distance_file.close()
    if arguments.debug:
        print("\n\n")
        print("# Entities: {}".format(len(entities)))
        print()


def __main__():
    arguments = command_line()
    input_file = open(arguments.input_file)
    if not input_file:
        print("Impossible to open input file \"{}\"".format(arguments.input_file))
        exit(-1)
    analysis(arguments, input_file)
    input_file.close()
    return 0


__main__()
