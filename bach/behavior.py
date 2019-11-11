import itertools


def encounter(entities):
    """
    Detect encounters between entities in a group.
    """
    for pair in itertools.combinations(entities, 2):
        if pair[0].overlap(pair[1]):
            print("Encounter: {} <-> {}".format(pair[0].marker, pair[1].marker))
