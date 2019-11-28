import itertools


class Behavior:
    """
    Class representing a certain behavior.
    """
    def __init__(self, label, begin):
        """
        Default constructor.
        """
        self.label = label
        self.begin = begin
        self.last = begin
        self.participants = list()

    def duration(self):
        """
        Return the duration of the behavior.
        """
        return self.last - self.begin

    def is_participant(self, entity):
        """
        Check if a given entity is participating in this behavior.
        """
        for participant in self.participants:
            if participant.same(entity):
                return True
        return False


def encounter(frame_number, entities, encounters):
    """
    Detect encounters between entities in a group.
    """
    for pair in itertools.combinations(entities, 2):
        if pair[0].overlap(pair[1]):
            # Check if encounter was already taking place
            updated_event = False
            for event in encounters:
                if event.is_participant(pair[0]) and event.is_participant(pair[1]):
                    event.last = frame_number
                    updated_event = True
                    break
            if updated_event:
                continue
            # Register new encounter
            event = Behavior("encounter", frame_number)
            event.participants.append(pair[0])
            event.participants.append(pair[1])
            encounters.append(event)
