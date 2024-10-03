#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 17:01:50 2021

@author: samira

Initialize all pair shortest paths for graph.

"""

import multiprocessing
import networkx as nx 
import pickle
import time
import numpy as np
import random as rd 
import os
print(os.getcwd())
with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)


myNodes = list(G.nodes)
allPairs = [[] for x in myNodes]

def fillMyMatrice(me):  
    myDistances = []
    for j in range(len(G.nodes)):   
        try:
            # Attempt to find the shortest path between me and j
            myDistances.append(len(nx.shortest_path(G, me, j, method='dijkstra')) - 1)
        except nx.NetworkXNoPath:
            # If no direct path exists, simulate travel via the cloud (node 0)
            try:
                # Find shortest path from me to the cloud (node 0) and j to the cloud (node 0)
                distance_me_to_cloud = len(nx.shortest_path(G, me, 0, method='dijkstra')) - 1
                distance_j_to_cloud = len(nx.shortest_path(G, j, 0, method='dijkstra')) - 1
                # Simulate the distance via the cloud by summing both distances
                myDistances.append(distance_me_to_cloud + distance_j_to_cloud)
            except nx.NetworkXNoPath:
                # If there is no path to the cloud, set a very high value or handle it appropriately
                myDistances.append(float('inf'))  # You can use a large number or some other placeholder
    return (me, myDistances)
         

pool = multiprocessing.Pool()
start = time.time()
result = pool.map(fillMyMatrice, myNodes)
for i in result:
    allPairs[i[0]] = i[1]
end = time.time()


#print("All Pairs " + str(end-start))


with open('allPairs', 'wb') as allPairs_file:
          pickle.dump(allPairs,allPairs_file)      
          
