import tkinter
import networkx as nx
from Graph import GraphAgent
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from AStarAlgorithm import *
from tkinter import ttk

from IDSAlgorithm import ids_algorithm

matplotlib.use('TkAgg')

master = tkinter.Tk()
master.wm_title("Final Project - CS420")

figure = plt.figure(figsize=(19 , 11))

state = -1
agent = GraphAgent('test.txt')
pos = {}
names = {}
weights = {}
graph = agent.graph.copy()
for key in graph.nodes_iter():
    pos[key] = (graph.node[key]['x'], graph.node[key]['y'])
    names[key] = graph.node[key]['name'] + '\n\n'

for source , target , attribute in graph.edges_iter(data=True):
    weights[(source , target)] = attribute['cost']

nx.draw(graph, pos, node_color='#ff5722', edge_color='#2196f3', width=4, linewidths=0)
nx.draw_networkx_edge_labels(graph , pos , weights , font_size=13)
nx.draw_networkx_labels(graph, pos, names, font_size=13)

canvas = FigureCanvasTkAgg(figure, master)
canvas.show()
canvas.get_tk_widget().grid(row=0 , column=0 , rowspan=4)


def add_new_node():
    new_node_panel = tkinter.Toplevel()
    new_node_panel.wm_title('Add a new node to graph')
    message = tkinter.Message(new_node_panel , text='Message')
    message.pack()
    cancel = tkinter.Button(new_node_panel , text='Cancel' , command = new_node_panel.destroy)
    cancel.pack()

button_add_node = tkinter.Button(master , text='++Node' , command = add_new_node)
button_add_node.grid(row=0 , column=1)


def add_new_edge():
    new_node_panel = tkinter.Toplevel()
    new_node_panel.wm_title('Add a new edge to graph')
    message = tkinter.Message(new_node_panel, text='Message')
    message.pack()
    cancel = tkinter.Button(new_node_panel, text='Cancel', command=new_node_panel.destroy)
    cancel.pack()

button_add_edge = tkinter.Button(master , text='++Edge' , command = add_new_edge)
button_add_edge.grid(row=1 , column=1)


def next_stage():
    global state
    if state == -1:
        return
    try:
        stage = next(iterator)
        if state == 0:
            opened = stage['opened']
            closed = stage['closed']
            cost = stage['cost']
            total = stage['total']
            opened_labels = {}
            closed_labels = {}
            for node in opened:
                opened_labels[node] = '\n\nestimate=' + str(total[node]) + '\ncost=' + str(cost[node])
            for node in closed:
                closed_labels[node] = '\n\nestimate=' + str(total[node]) + '\ncost=' + str(cost[node])
            nx.draw_networkx_nodes(graph , pos , nodelist=stage['opened'] , node_color='#f44336' , label=opened_labels)
            nx.draw_networkx_nodes(graph , pos , nodelist=stage['closed'] , node_color='#3f51b5' , label=closed_labels)
        canvas.show()
    except StopIteration as exception:
        result = exception.value
        is_first = True
        previous = -1
        pair = []
        for node in result['path']:
            if is_first:
                is_first = False
                previous = node
            else:
                pair.append((previous , node))
                previous = node
        nx.draw_networkx_edges(graph , pos , edgelist=pair , edge_color='r' , width=4)
        canvas.show()
        print(result)

button_add_edge = tkinter.Button(master , text='Next' , command = next_stage)
button_add_edge.grid(row=2 , column=1)


def reset():
    pos.clear()
    names.clear()
    weights.clear()
    graph = agent.graph.copy()
    for key in graph.nodes_iter():
        pos[key] = (graph.node[key]['x'], graph.node[key]['y'])
        names[key] = graph.node[key]['name'] + '\n\n'

    for source, target, attribute in graph.edges_iter(data=True):
        weights[(source, target)] = attribute['cost']

    nx.draw(graph, pos, node_color='#ff5722', edge_color='#2196f3', width=4, linewidths=0)
    nx.draw_networkx_edge_labels(graph, pos, weights, font_size=13)
    nx.draw_networkx_labels(graph, pos, names, font_size=13)
    canvas.show()
    global state
    state = -1

button_reset = tkinter.Button(master , text='Reset' , command=reset)
button_reset.grid(row=3 , column=1)

combox_source = ttk.Combobox(master , values=list(names.values()), state='readonly')
combox_source.grid(row=4 , column=1)

combox_target = ttk.Combobox(master , values=list(names.values()), state='readonly')
combox_target.grid(row=5 , column=1)


def get_info():
    start_name = list(names.values())[combox_source.current()]
    goal_name = list(names.values())[combox_target.current()]
    start = goal = -1
    for node, value in names.items():
        if value == start_name:
            start = node
        elif value == goal_name:
            goal = node
    return start , goal

iterator = None


def launch_a_star():
    info = get_info()
    global iterator
    iterator = a_star_algorithm(agent , info[0] , info[1])
    global state
    state = 0

button_a_star = tkinter.Button(master , text='A*' , command=launch_a_star)
button_a_star.grid(row=6 , column=1)

master.mainloop()
