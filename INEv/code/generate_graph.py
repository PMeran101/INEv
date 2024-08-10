#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:12:21 2021

@author: samira
"""
import networkx as nx
from networkx import Graph as gp
import Node
import pickle
#from networkx.algorithms.components import is_connected
#import matplotlib.pyplot as plt
import sys
import random

def main():
    
   with open('network', 'rb') as network_file:
            nw = pickle.load(network_file) 
            print(nw)
  # percentage = 50
   outdegree = 3
   experiment = 'None'
   
     
   if len(sys.argv) > 1: 
      outdegree = int(sys.argv[1])      
   G = nx.Graph()
   G = create_fog_graph(nw[0], G)
   #G = nx.connected_watts_strogatz_graph(len(nw),outdegree,0.2)   
          
   print(G.edges)
   #print(nx.adjacency_matrix(G))

 
   with open('graph', 'wb') as graph_file:
         pickle.dump(G,graph_file)     



def create_fog_graph(node, graph=None, nodes=set(), edges=set()):
    if graph is None:
        graph = nx.Graph()

    if node.id not in nodes:
        graph.add_node(node.id, label=str(node.id))
        nodes.add(node.id)

    if node.Child is not None:
        if (node.id, node.Child.id) not in edges:
            graph.add_node(node.Child.id, label=str(node.Child.id))
            graph.add_edge(node.id, node.Child.id)
            edges.add((node.id, node.Child.id))
        create_fog_graph(node.Child, graph, nodes, edges)

    sibling = node.Sibling
    while sibling is not None:
        if sibling.id not in nodes:
            graph.add_node(sibling.id, label=str(sibling.id))
            nodes.add(sibling.id)
        if (node.Parent.id, sibling.id) not in edges:
            graph.add_edge(node.Parent.id, sibling.id)
            edges.add((node.Parent.id, sibling.id))
        create_fog_graph(sibling, graph, nodes, edges)
        sibling = sibling.Sibling

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
    
              
          
          
          
if __name__ == "__main__":
    main()          