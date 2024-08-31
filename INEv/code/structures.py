#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:45:00 2021

@author: samira
"""
from util import column,column1s,reverseDict

# from network import *

import numpy as np
import pickle
from tree import Tree,AND,SEQ,PrimEvent,NSEQ,KL
from helper import *
from parse_network import *
from network import get_network,get_nodes

network = get_network()
nodes = get_nodes()
#import matplotlib.pyplot as plt
import networkx as nx 
from networkx.algorithms.approximation import steiner_tree
from networkx.algorithms.components import is_connected
from EvaluationPlan import *
import time
import numpy as np
#G = nx.Graph()

with open("allPairs", "rb") as allPairs_file:
    allPairs = pickle.load(allPairs_file)

with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)
ETB = {} # {"A": {"A1": [2,3], "A3" = [3]}, "B" {"B1:[1,3]} ....}
placementTreeDict = {} # {("D", "A1"): (5,[2,3,4], steinerTree(5234)} show steiner tree to connect all D's with A1 -> problem: what about multiple recipient event types? what about single sink placements=
eventNodeDict =  {} # {0: ["B1", "A3", "E0"], 1: ["A1B2", "A1B3", "B1"]} which instances of events/projections are generated or sent to/via node x -> maybe reuse network dict, but atm used for other stuff


# Module-level variables
EventNodes = None
IndexEventNodes = None

def initEventNodes():
    """Initialize EventNodes and IndexEventNodes."""
    global EventNodes, IndexEventNodes
    
    myEventNodes = []
    myIndexEventNodes = {}
    index = 0

    for etype in nodes.keys():
        myetbs = []
        for node in nodes[etype]:
            mylist = [0 for _ in range(len(network.keys()))]
            mylist[node] = 1
            myEventNodes.append(mylist)
            myIndexEventNodes[etype + str(node)] = index
            index += 1
            myetbs.append(etype + str(node))
        myIndexEventNodes[etype] = myetbs

    EventNodes = myEventNodes
    IndexEventNodes = myIndexEventNodes

def get_EventNodes():
    """Return EventNodes, initializing if necessary."""
    if EventNodes is None:
        initEventNodes()
    return EventNodes

def get_IndexEventNodes():
    """Return IndexEventNodes, initializing if necessary."""
    if IndexEventNodes is None:
        initEventNodes()
    return IndexEventNodes
projFilterDict = {}


def getETBs(node):
    mylist = column1s(column(EventNodes, node))       
    return [list(IndexEventNodes.keys())[list(IndexEventNodes.values()).index(x)] for x in mylist] # index from row id <-> etb

def getNodes(etb):
    return column1s(EventNodes[IndexEventNodes[etb]])

def setEventNodes(node, etb):
    EventNodes[IndexEventNodes[etb]][node] = 1
 
def unsetEventNodes(node, etb):
    EventNodes[IndexEventNodes[etb]][node] = 0    
    
def addETB(etb, etype):
    mylist = [0 for x in range(len(network.keys()))]
    EventNodes.append(mylist)
    index = len(EventNodes)-1
    IndexEventNodes[etb] = index
    if not etype in IndexEventNodes:
        IndexEventNodes[etype] = [etb]
    else:
        IndexEventNodes[etype].append(etb)
    
def SiSManageETBs(projection, node):
    etbID = genericETB("", projection)[0]
    addETB(etbID, projection)           
    setEventNodes(node, etbID)       

def MSManageETBs(projection, parttype):
    etbIDs = genericETB(parttype, projection)
    for projectionETB in etbIDs:
             addETB(projectionETB, projection)             
    for i in range(len(nodes[parttype])):
        setEventNodes(nodes[parttype][i], etbIDs[i])          


def genericETB(partType, projection):
    ETBs = []   
    if len(partType) == 0 or not partType in projection.leafs():
        myID = ""
        for etype in projection.leafs():
            myID += etype
        ETBs.append(myID)
    else:
        for node in nodes[partType]:   
            myID = ""
            for etype in projection.leafs():
                myID += etype
                if etype == partType:
                    myID += str(node)
            ETBs.append(myID)
    return ETBs

def getNumETBs(projection):
    num = 1
    for etype in projection.leafs():
        num *= len(IndexEventNodes[etype])
    return num

def NumETBsByKey(etb, projection):
    instancedEvents = []
    index = 0
    if len(projection) == 1:
        return 1
    for i in range(1, len(etb)):       
        if not etb[i] in projection.leafs() and etb[index] in projection.leafs() and not etb[index] in instancedEvents:
            instancedEvents.append(etb[index])
        elif etb[i] in projection.leafs():
            index = i
    
    num = getNumETBs(projection)
    for etype in instancedEvents:
        num = num / len(IndexEventNodes[etype])
    return num

def getLongest():
    avs  = []
    for i in allPairs:
        avs.append(np.average(i))
    return np.median(avs)


longestPath = getLongest()
maxDist = max(sum(allPairs,[]))

   
