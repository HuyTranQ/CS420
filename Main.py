import tkinter
import networkx as nx
from Graph import GraphAgent
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

master = tkinter.Tk()
master.wm_title("Final Project - CS420")

figure = plt.figure(figsize=(19 , 11))

agent = GraphAgent('D:/Academics/CS420/test.txt')
pos = {}
names = {}
weights = {}
for key in agent.graph.nodes_iter():
    pos[key] = (agent.graph.node[key]['x'], agent.graph.node[key]['y'])
    names[key] = agent.graph.node[key]['name'] + '\n\n'

for source , target , attribute in agent.graph.edges_iter(data=True):
    weights[(source , target)] = attribute['cost']

nx.draw(agent.graph, pos, node_color='#ff5722', edge_color='#2196f3', width=4, linewidths=0)
nx.draw_networkx_edge_labels(agent.graph , pos , weights , font_size=13)
nx.draw_networkx_labels(agent.graph, pos, names, font_size=13)


def add_new_node():
    new_node_panel = tkinter.Toplevel()
    new_node_panel.wm_title('Add a new node to graph')
    message = tkinter.Message(new_node_panel , text='Message')
    message.pack()
    cancel = tkinter.Button(new_node_panel , text='Cancel' , command = new_node_panel.destroy)
    cancel.pack()

button_add_node = tkinter.Button(master , text='++Node' , command = add_new_node)
button_add_node.pack(side=tkinter.RIGHT , anchor='ne')


def add_new_edge():
    new_node_panel = tkinter.Toplevel()
    new_node_panel.wm_title('Add a new edge to graph')
    message = tkinter.Message(new_node_panel, text='Message')
    message.pack()
    cancel = tkinter.Button(new_node_panel, text='Cancel', command=new_node_panel.destroy)
    cancel.pack()

button_add_edge = tkinter.Button(master , text='++Edge' , command = add_new_edge)
button_add_edge.pack(side=tkinter.RIGHT)

canvas = FigureCanvasTkAgg(figure, master)
canvas.show()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

master.mainloop()
