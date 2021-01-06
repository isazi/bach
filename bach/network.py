

class Graph:
    """
    Class representing an undirected graph.
    """
    def __init__(self):
        self.graph = dict()

    def add_edge(self, i, j):
        """
        Add one edge to the graph.
        """
        self.graph[i][j] = 1

    def remove_edge(self, i, j):
        """
        Remove one edge from the graph.
        """
        self.graph[i][j] = 0

    def edge(self, i, j):
        """
        Check if one edge is in the graph.
        """
        try:
            if self.graph[i][j] == 1:
                return True
            elif self.graph[j][i] == 1:
                return True
        except KeyError:
            return False
        return False
