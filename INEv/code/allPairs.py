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
                # Get all shortest path lengths from me and j to all other nodes (including the cloud)
                me_shortest_paths = nx.single_source_dijkstra_path_length(G, me)
                j_shortest_paths = nx.single_source_dijkstra_path_length(G, j)
                
                # Find the common nodes (ancestors) reachable from both me and j
                common_ancestors = set(me_shortest_paths.keys()) & set(j_shortest_paths.keys())
                
                if common_ancestors:
                    # Calculate the combined path length for all common ancestors
                    combined_distances = [
                        me_shortest_paths[ancestor] + j_shortest_paths[ancestor] 
                        for ancestor in common_ancestors
                    ]
                    # Get the minimum combined distance
                    myDistances.append(min(combined_distances))
                else:
                    # Fallback to the cloud (node 0) if no other common ancestors exist
                    distance_me_to_cloud = me_shortest_paths.get(0, float('inf'))
                    distance_j_to_cloud = j_shortest_paths.get(0, float('inf'))
                    myDistances.append(distance_me_to_cloud + distance_j_to_cloud)
            except nx.NetworkXNoPath:
                # If there's no path to the cloud or any other intermediary, handle it appropriately
                myDistances.append(float('inf'))  # Or another placeholder value
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
          
