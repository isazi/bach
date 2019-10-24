import itertools


def encounter(entities):
    """
    Detect encounters between entities in a group.
    """
    for pair in itertools.combinations(entities, 2):
        if entities[pair[0]].marker != -1 and entities[pair[1]].marker != -1:
            if entities[pair[0]].overlap(entities[pair[1]]):
                print("Interaction: {} <-> {}".format(pair[0], pair[1]))
