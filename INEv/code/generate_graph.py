#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:12:21 2021

@author: samira
"""
import networkx as nx
from networkx import DiGraph as gp
import Node
import pickle
from collections import deque
#from networkx.algorithms.components import is_connected
#import matplotlib.pyplot as plt
import sys
import random


def create_fog_graph(root, graph=None, nodes=set(), edges=set()):
    if graph is None:
        graph = nx.DiGraph()

    nodes = set()
    edges = set()

    # Use a queue to perform a breadth-first traversal of the tree
    queue = deque([root])

    while queue:
        current_node = queue.popleft()

        # Add the current node to the graph
        if current_node.id not in nodes:
            graph.add_node(current_node.id, label=str(current_node.id))
            nodes.add(current_node.id)

        # Handle child nodes (now an array)
        if current_node.Child is not None and isinstance(current_node.Child, list):
            for child in current_node.Child:
                if child.id not in nodes:
                    graph.add_node(child.id, label=str(child.id))
                    nodes.add(child.id)
                if (child.id, current_node.id) not in edges:
                        graph.add_edge(child.id, current_node.id)  # Edge from child to parent
                        edges.add((child.id, current_node.id))
                # Add the child to the queue for further processing
                queue.append(child)

        # Handle sibling nodes (now an array)
        if current_node.Sibling is not None and isinstance(current_node.Sibling, list):
            for sibling in current_node.Sibling:
                if sibling.id not in nodes:
                    graph.add_node(sibling.id, label=str(sibling.id))
                    nodes.add(sibling.id)
                if current_node.Parent and (current_node.Parent.id, sibling.id) not in edges:
                    graph.add_edge(child.id, current_node.id)  # Edge only from child to parent
                    edges.add((child.id, current_node.id))
                queue.append(sibling)

    return graph


def permute_edges(G,percentage): # new graph has less nodes as nodes are inferred from edges
    
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    new_edges = []
    for i in range(number):
        a = int(random.uniform(0, len(G.nodes)))
        b = int(random.uniform(0, len(G.nodes)))
        new_edges.append((a,b))
    my_edges=  list_edges[- (len(list_edges) - number):] + new_edges
    my_G = nx.Graph()
    my_G.add_edges_from(my_edges)
    while set(my_G) == set(G.edges) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        new_edges = []
        for i in range(number):
            a = int(random.uniform(0, len(G.nodes)))
            b = int(random.uniform(0, len(G.nodes)))
            new_edges.append((a,b))
        my_edges=  list_edges[- (len(list_edges) - number):] + new_edges
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G


def remove_edges(G,percentage): # not possible 
    
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    

    my_edges = list_edges[0:len(list_edges ) - number]
    my_G = nx.Graph()
    my_G.add_edges_from(my_edges)
    while not nx.is_connected(my_G) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        my_edges = list_edges[0:len(list_edges ) - number]
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G    

def add_edges(G,percentage):
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    new_edges = []
    for i in range(number):
        a = int(random.uniform(0, len(G.nodes)))
        b = int(random.uniform(0, len(G.nodes)))
        new_edges.append((a,b))
    my_edges = list_edges + new_edges 
    my_G = nx.Graph()
    my_G.add_edges_from(my_edges)
    while not nx.is_connected(my_G) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        new_edges = []
        for i in range(number):
            a = int(random.uniform(0, len(G.nodes)))
            b = int(random.uniform(0, len(G.nodes)))
            new_edges.append((a,b))
        my_edges = list_edges + new_edges 
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G
    
    
def main():
    
   with open('network', 'rb') as network_file:
            nw = pickle.load(network_file) 
 
   G = create_fog_graph(nw[0])

 
   with open('graph', 'wb') as graph_file:
         pickle.dump(G,graph_file)                
          
          
          
if __name__ == "__main__":
    main()          