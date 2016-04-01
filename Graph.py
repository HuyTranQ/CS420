from sys import argv
import networkx as nx
from Node import Node
import cmath
import networkx as nx

class GraphAgent:
    """Artificial Intelligence Agent"""

    def __init__(self, filename):
        input_file = open(filename, 'r')
        self.node_size = int(input_file.readline())
        self.data = {}
        self.data = nx.Graph()
        for i in range(self.node_size):
            _key = int(input_file.readline())
            _name = input_file.readline().rstrip('\n')
            _x = int(input_file.readline())
            _y = int(input_file.readline())
            self.data.add_node(_key, name=_name, x=_x, y=_y)

        self.edge_size = int(input_file.readline())
        for i in range(self.edge_size):
            a = int(input_file.readline())
            b = int(input_file.readline())
            c = int(input_file.readline())
            self.data.add_edge(a, b, cost=c)

    @property
    def graph(self):
        return self.data

    def heuristic(self , source , target):
        x = self.graph.node[source]['x'] - self.graph.node[target]['x']
        y = self.graph.node[source]['y'] - self.graph.node[target]['y']
        return 1 + int(1.618 * cmath.sqrt(x * x + y * y))
