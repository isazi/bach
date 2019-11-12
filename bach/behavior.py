import itertools


def encounter(entities, encounters):
    """
    Detect encounters between entities in a group.
    """
    for pair in itertools.combinations(entities, 2):
        if pair[0].overlap(pair[1]):
            encounters.append(pair)
