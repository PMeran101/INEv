import psutil
import os
import logging
from collections import deque
import networkx as nx
import pickle
from Node import Node
import sys


with open('network', 'rb') as network_file:
        nw = pickle.load(network_file) 
        
        
def create_fog_graph(nodes_list):
    import networkx as nx

    graph = nx.DiGraph()
    # Add all nodes with their attributes
    graph.add_nodes_from(
        (node.id, {
            'label': str(node.id),
            'computational_power': node.computational_power,
            'memory': node.memory,
            'eventrates': node.eventrates,
        })
        for node in nodes_list
    )
    
    # Collect all edges (from child to parent)
    edges = set()

    for node in nodes_list:
        # Add edges from child to parents
        if node.Parent:
            for parent_node in node.Parent:
                edges.add((node.id, parent_node.id))
    
    # Add edges to the graph in bulk
    graph.add_edges_from(edges)

    return graph

# Create a mapping from node IDs to Node instances
node_dict = [node for node in nw]

G = create_fog_graph(node_dict)

allPairs = dict(nx.all_pairs_shortest_path(G))
print(allPairs[2])
# print(allPairs)
with open('graph', 'wb') as graph_file:
    pickle.dump(G,graph_file)                
        
          
# F = create_graph(nw[0])

# print(G == F)

# print(F.nodes)
# print("----")
# print(G.nodes)
# print(G.nodes == F.nodes)
# print(G.edges == F.edges)