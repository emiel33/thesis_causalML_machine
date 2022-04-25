import matplotlib.pyplot as plt
import networkx as nx

dirGraph = nx.DiGraph()
dirGraph.add_nodes_from([1, 1])
dirGraph.add_edge(1,2)


nx.draw(dirGraph, with_labels=True, font_weight='bold')
plt.savefig("hi")