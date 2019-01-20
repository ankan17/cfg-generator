import networkx as nx
import matplotlib.pyplot as plt

from parser import PythonParser


graph_obj = PythonParser('test.py').construct_graph()

G = nx.DiGraph()
G.add_nodes_from(graph_obj.nodes)
G.add_edges_from(graph_obj.edges)
nx.draw(G, with_labels=True)
plt.show()
