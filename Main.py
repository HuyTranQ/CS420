import tkinter
import networkx as nx
from Graph import GraphAgent
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from AStarAlgorithm import *
from tkinter import ttk
from tkinter import messagebox

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
canvas.get_tk_widget().grid(row=0 , column=0 , rowspan=3)


def add_new_node():
    new_node_panel = tkinter.Toplevel(width=500, height=200)
    new_node_panel.wm_title('Add a new node to graph')
    message = tkinter.Message(new_node_panel , text='Please fill in the following information')
    message.pack()
    cancel = tkinter.Button(new_node_panel , text='Cancel' , command = new_node_panel.destroy)
    cancel.pack()


def add_new_edge():
    new_node_panel = tkinter.Toplevel(master=None, width=500, height=200)
    new_node_panel.wm_title('Add a new edge to graph')
    message = tkinter.Message(new_node_panel, text='Message')
    message.pack()
    cancel = tkinter.Button(new_node_panel, text='Cancel', command=new_node_panel.destroy)
    cancel.pack()
    new_node_panel.mainloop()

graph_control_frame = tkinter.Frame(master)
graph_control_frame.grid(row=0, column=1)

tkinter.Label(graph_control_frame, text="GRAPH", font=("Helvetica", 16)).pack(side=tkinter.TOP)

button_add_node = tkinter.Button(graph_control_frame, text='++Node' , command = add_new_node)
button_add_node.pack()

button_add_edge = tkinter.Button(graph_control_frame, text='++Edge' , command = add_new_edge)
button_add_edge.pack()

node_labels = {}


def next_stage():
    global state
    if state == -1:
        return
    try:
        stage = next(iterator)
        global graph
        graph = agent.graph.copy()
        if state == 0:
            # names.clear()
            opened = stage['opened']
            closed = stage['closed']
            cost = stage['cost']
            total = stage['total']
            previous = stage['previous']
            edges = []
            global node_labels
            new_labels = {}
            renew_labels = {}
            for node in opened:
                new_value = '\n\n\n\nf=' + str(total[node]) + '\ng=' + str(cost[node])
                if node not in node_labels:
                    new_labels[node] = new_value
                else:
                    renew_labels[node_labels[node]] = new_value
                node_labels[node] = new_value
            for node in closed:
                new_value = '\n\n\n\nf=' + str(total[node]) + '\ng=' + str(cost[node])
                if node not in node_labels:
                    new_labels[node] = new_value
                else:
                    renew_labels[node_labels[node]] = new_value
                node_labels[node] = new_value
            for a , b in previous.items():
                edges.append((a , b))
            nx.draw_networkx_nodes(graph , pos , nodelist=opened , node_color='#f44336')
            nx.draw_networkx_nodes(graph , pos , nodelist=closed , node_color='#3f51b5')
            nx.draw_networkx_labels(graph , pos , new_labels , font_weight='normal')
            nx.relabel_nodes(graph , renew_labels)
            nx.draw_networkx_edges(graph , pos , edgelist=edges , edge_color='#1b5e20' , width=4)

        elif state == 1:
            # names.clear()
            edges = []
            cur_path = stage['current path']
            opened = stage['opened']

            if stage['depth changed']:
                plt.clf()
                graph = agent.graph.copy()

                nx.draw(graph, pos, node_color='#ff5722', edge_color='#2196f3', width=4, linewidths=0)
                nx.draw_networkx_edge_labels(graph , pos , weights , font_size=13)
                nx.draw_networkx_labels(graph, pos, names, font_size=13)

                canvas.show()
                node_labels.clear()

            # new_labels = {}
            # renew_labels = {}
            # for i, node in enumerate(cur_path):
            #     new_value = 'd=' + str(i)
            #     if node not in node_labels:
            #         new_labels[node] = '\n\n\n\n' + new_value
            #         node_labels[node] = '\n\n\n\n' + new_value
            #     elif node in renew_labels:
            #         renew_labels[renew_labels[node]] = renew_labels[node] + '\n' + new_value
            #     else:
            #         renew_labels[node_labels[node]] = node_labels[node] + '\n' + new_value

            for i in range(0, len(cur_path) - 1):
                edges.append((cur_path[i], cur_path[i + 1]))

            opened_nodes = set()
            for node in opened:
                opened_nodes.add(node[0])
            for node in cur_path:
                opened_nodes.add(node)

            nx.draw_networkx_nodes(graph, pos, nodelist=opened_nodes, node_color='#4caf50')
            # nx.draw_networkx_nodes(graph, pos, nodelist=cur_path, node_color='#3f51b5')
            # nx.draw_networkx_labels(graph, pos, node_labels, font_weight='normal')
            # nx.relabel_nodes(graph, renew_labels)
            nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='#2196f3', width=4)
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='#1b5e20', width=4)
        canvas.show()
    except StopIteration as exception:
        result = exception.value
        if result is None:
            return
        is_first = True
        previous = -1
        pair = []
        node_labels = {}
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


def reset():
    plt.clf()
    # pos.clear()
    # weights.clear()
    graph = agent.graph.copy()
    # for key in graph.nodes_iter():
    #    pos[key] = (graph.node[key]['x'], graph.node[key]['y'])

    nx.draw(graph, pos, node_color='#ff5722', edge_color='#2196f3', width=4, linewidths=0)
    nx.draw_networkx_edge_labels(graph , pos , weights , font_size=13)
    nx.draw_networkx_labels(graph, pos, names, font_size=13)
    canvas.show()
    global state
    state = -1


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

iterator = {}


def launch_a_star():
    info = get_info()
    global iterator
    iterator = a_star_algorithm(agent , info[0] , info[1])
    global state
    state = 0


def launch_ids():
    info = get_info()
    global iterator
    iterator = ids_algorithm(agent , info[0] , info[1])
    global state
    state = 1

demo_frame = tkinter.Frame(master)
demo_frame.grid(row=2, column=1)

tkinter.Label(demo_frame, text="DEMO", font=("Helvetica", 16)).pack(side=tkinter.TOP)
tkinter.Label(demo_frame, text="Source").pack(side=tkinter.TOP)
combox_source = ttk.Combobox(demo_frame, values=list(names.values()), state='readonly')
combox_source.pack()

tkinter.Label(demo_frame, text="Target").pack(side=tkinter.TOP)
combox_target = ttk.Combobox(demo_frame , values=list(names.values()), state='readonly')
combox_target.pack()

alg_frame = tkinter.Frame(demo_frame)
alg_frame.pack(side=tkinter.TOP)

tkinter.Label(alg_frame, text="Algorithm").pack(side=tkinter.TOP)

button_a_star = tkinter.Button(alg_frame, text='A*' , command=launch_a_star)
button_a_star.pack(side=tkinter.LEFT)

button_ids = tkinter.Button(alg_frame, text='IDS', command=launch_ids)
button_ids.pack(side=tkinter.LEFT)

button_ucs = tkinter.Button(alg_frame, text='UCS', command=None)
button_ucs.pack(side=tkinter.LEFT)

tkinter.Label(demo_frame, text="Control").pack(side=tkinter.TOP)
button_next = tkinter.Button(demo_frame, text='Next' , command = next_stage)
button_next.pack()

button_reset = tkinter.Button(demo_frame, text='Reset' , command=reset)
button_reset.pack()
agent.export('graph_export.txt')
master.mainloop()
