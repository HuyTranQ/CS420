import tkinter
import networkx as nx
from Graph import GraphAgent
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from AStarAlgorithm import *
from UCSAlgo import *
from tkinter import ttk
from tkinter import messagebox

from IDSAlgorithm import ids_algorithm

matplotlib.use('TkAgg')

master = tkinter.Tk()
master.wm_title("Final Project - CS420")

figure = plt.figure(figsize=(19 , 11))
mouse_x = tkinter.IntVar()
mouse_y = tkinter.IntVar()


def onclick(event):
    global mouse_x
    mouse_x.set(str(int(round(event.xdata))))
    global mouse_y
    mouse_y.set(str(int(round(event.ydata))))

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

canvas.mpl_connect('button_press_event', onclick)


def add_node(name, x, y):
    agent.add_node(name, x, y)
    reset()
    combox_source['values'] = list(names.values())
    combox_target['values'] = list(names.values())


def add_new_node_callback():
    new_node_panel = tkinter.Toplevel()
    new_node_panel.geometry("300x125")
    new_node_panel.wm_title('Add new nodes')

    info_frame = tkinter.Frame(new_node_panel)
    info_frame.pack()

    tkinter.Label(info_frame, text='Please fill in the following information').grid(row=0, columnspan=2)

    tkinter.Label(info_frame, text='Name').grid(row=1, column=0)
    _name = tkinter.StringVar()
    entry_name = tkinter.Entry(info_frame, textvariable=_name)
    entry_name.grid(row=1, column=1)

    tkinter.Label(info_frame, text='x').grid(row=2, column=0)
    entry_x = tkinter.Entry(info_frame, textvariable=mouse_x)
    entry_x.grid(row=2, column=1)

    tkinter.Label(info_frame, text='y').grid(row=3, column=0)
    entry_y = tkinter.Entry(info_frame, textvariable=mouse_y)
    entry_y.grid(row=3, column=1)

    action_frame = tkinter.Frame(new_node_panel)
    action_frame.pack(side=tkinter.BOTTOM)

    add = tkinter.Button(action_frame, text='Add node',
                         command=lambda : add_node(_name.get(), mouse_x.get(), mouse_y.get()))

    add.pack(side=tkinter.LEFT)
    cancel = tkinter.Button(action_frame, text='Exit', command=new_node_panel.destroy)
    cancel.pack(side=tkinter.LEFT)


def add_edge(source, target, weight):
    agent.add_edge(source, target, weight)
    reset()


def add_new_edge_callback():
    new_edge_panel = tkinter.Toplevel()
    new_edge_panel.geometry("300x125")
    new_edge_panel.wm_title('Add new edges')

    info_frame = tkinter.Frame(new_edge_panel)
    info_frame.pack()

    tkinter.Label(info_frame, text='Please fill in the following information').grid(row=0, columnspan=2)

    tkinter.Label(info_frame, text='Source').grid(row=1, column=0)
    cb_source = ttk.Combobox(info_frame, values=list(names.values()), state='readonly')
    cb_source.grid(row=1, column=1)

    tkinter.Label(info_frame, text='Target').grid(row=2, column=0)
    cb_target = ttk.Combobox(info_frame, values=list(names.values()), state='readonly')
    cb_target.grid(row=2, column=1)

    tkinter.Label(info_frame, text='Weight').grid(row=3, column=0)
    weight = tkinter.IntVar()
    entry_weight = tkinter.Entry(info_frame, textvariable=weight)
    entry_weight.grid(row=3, column=1)

    action_frame = tkinter.Frame(new_edge_panel)
    action_frame.pack(side=tkinter.BOTTOM)

    add = tkinter.Button(action_frame, text='Add edge',
                         command=lambda : add_edge(cb_source.current(),
                                                   cb_target.current(),
                                                   weight.get()))
    add.pack(side=tkinter.LEFT)
    cancel = tkinter.Button(action_frame, text='Exit', command=new_edge_panel.destroy)
    cancel.pack(side=tkinter.LEFT)

graph_control_frame = tkinter.Frame(master)
graph_control_frame.grid(row=0, column=1)

tkinter.Label(graph_control_frame, text="GRAPH", font=("Helvetica", 16)).pack(side=tkinter.TOP)

button_add_node = tkinter.Button(graph_control_frame, text='Add nodes' , command = add_new_node_callback)
button_add_node.pack()

button_add_edge = tkinter.Button(graph_control_frame, text='Add edges' , command = add_new_edge_callback)
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

        elif state == 7:
            node = set()
            new_labels = {}
            node.add(stage['node'])
            path = stage['path']
            cost = stage['cost']
            new_labels[stage['node']] = '\n\n\n\ncost = ' + str(cost)
            edges = []
            for i in range(0, len(path) - 1):
                edges.append((path[i], path[i + 1]))
            supernode = set()
            supernode.add(stage['start'])
            supernode.add(stage['goal'])

            nx.draw_networkx_nodes(graph, pos, nodelist=node, node_color='#3bd28a')
            nx.draw_networkx_nodes(graph, pos, nodelist=supernode, node_color='#512da8')
            nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='#2196f3', width=4)
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='#ffc0ff', width=4)
            nx.draw_networkx_labels(graph, pos, new_labels, font_weight='normal')

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
    names.clear()
    pos.clear()
    weights.clear()

    graph = agent.graph.copy()

    for key in graph.nodes_iter():
        pos[key] = (graph.node[key]['x'], graph.node[key]['y'])
        names[key] = graph.node[key]['name'] + '\n\n'

    for source , target , attribute in graph.edges_iter(data=True):
        weights[(source , target)] = attribute['cost']

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

def launch_ucs():
    info = get_info()
    global iterator
    iterator = UCS(agent , info[0] , info[1])
    global state
    state = 7

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

button_ucs = tkinter.Button(alg_frame, text='UCS', command=launch_ucs)
button_ucs.pack(side=tkinter.LEFT)

tkinter.Label(demo_frame, text="Control").pack(side=tkinter.TOP)
button_next = tkinter.Button(demo_frame, text='Next' , command = next_stage)
button_next.pack()

button_reset = tkinter.Button(demo_frame, text='Reset' , command=reset)
button_reset.pack()


def on_window_closed():
    agent.export('graph_export.txt')
    master.destroy()

master.protocol(name="WM_DELETE_WINDOW", func=on_window_closed)
master.mainloop()
