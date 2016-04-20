from sys import argv
import networkx as nx
from Node import Node
import math
import networkx as nx


class GraphAgent:
    """Artificial Intelligence Agent"""

    def __init__(self, filename=None):
        if filename is None:
            self.node_size = 0
            self.edge_size = 0
            self.data = nx.Graph()
            return

        with open(filename, 'r') as input_file:
            self.node_size = int(input_file.readline())
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
        return 1 + int(1.618 * math.sqrt(x ** 2 + y ** 2))

    def add_node(self, name, x, y):
        self.data.add_node(self.node_size, name=name, x=x, y=y)
        self.node_size += 1

    def add_edge(self, source, target, weight):
        self.data.add_edge(source, target, cost=weight)
        self.edge_size += 1

    def export(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(str(self.node_size) + '\n')

            for node in self.data.nodes_iter():
                output_file.write(str(node) + '\n')
                attr = self.data.node[node]
                output_file.write(str(attr['name']) + '\n')
                output_file.write(str(attr['x']) + '\n')
                output_file.write(str(attr['y']) + '\n')

            output_file.write(str(self.edge_size) + '\n')
            for source, target in self.data.edges_iter():
                attr = self.data.edge[source][target]
                output_file.write(str(source) + '\n')
                output_file.write(str(target) + '\n')
                output_file.write(str(attr['cost']) + '\n')
