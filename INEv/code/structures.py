#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:45:00 2021

@author: samira
"""
from util import *

import copy
import numpy as np
import pickle
from tree import *
from helper import *
from parse_network import get_nodes, get_network

import networkx as nx 
from networkx.algorithms.approximation import steiner_tree
from networkx.algorithms.components import is_connected
from EvaluationPlan import *
import time
import numpy as np
from binary_helper import load_file

allPairs = load_file("allPairs")
G = load_file("graph")

# ETB = {} # {"A": {"A1": [2,3], "A3" = [3]}, "B" {"B1:[1,3]} ....}
# placementTreeDict = {} # {("D", "A1"): (5,[2,3,4], steinerTree(5234)} show steiner tree to connect all D's with A1 -> problem: what about multiple recipient event types? what about single sink placements=
# eventNodeDict =  {} # {0: ["B1", "A3", "E0"], 1: ["A1B2", "A1B3", "B1"]} which instances of events/projections are generated or sent to/via node x -> maybe reuse network dict, but atm used for other stuff

_ETB = None
_placementTreeDict = None
_eventNodeDict = None

def init_ETB():
    return {}

def init_placementTreeDict():
    return {}

def init_eventNodeDict():
    return {}

def get_ETB():
    global _ETB
    if _ETB is None:
        _ETB = init_ETB()
    return _ETB

def get_placementTreeDict():
    global _placementTreeDict
    if _placementTreeDict is None:
        _placementTreeDict = init_placementTreeDict()
    return _placementTreeDict

def get_eventNodeDict():
    global _eventNodeDict
    if _eventNodeDict is None:
        _eventNodeDict = init_eventNodeDict()
    return _eventNodeDict

# Global caches for lazy loading
_EventNodes = None
_IndexEventNodes = None
_projFilterDict = {}
def initEventNodes():  #matrice: comlumn indices are node ids, row indices correspond to etbs, for a given etb use IndexEventNodes to get row ID for given ETB
    #Storign all nodes producing a given event type with a 1 in the corresponding list
    # Node generating event type A would have: [1,0,0,0,...]
    myEventNodes = []
    #Storing a dictionary with the event type and node id as key and the index in the myEventNodes type for the list.
    myIndexEventNodes = {}
    offset = 0
    index = 0
    nodes = get_nodes()
    network = get_network()
    print(nodes)
    #For each primitve event
    for etype in nodes.keys():
        myetbs = []
        #each node producting the event type
        for node in nodes[etype]:

            #creating a list of zeros with the length of the network
            mylist = [0 for x in range(len(network.keys()))]
            #Adding a 1 at the position of the node producing the event
            mylist[node] = 1
            myEventNodes.append(mylist)
            myIndexEventNodes[etype+str(node)] = index
            index += 1
            myetbs.append(etype+str(node))
        myIndexEventNodes[etype] = myetbs
        offset = index
    return(myEventNodes, myIndexEventNodes)

def get_EventNodes():
    global _EventNodes
    if _EventNodes is None:
        _EventNodes = initEventNodes()[0]
    return _EventNodes

def get_IndexEventNodes():
    global _IndexEventNodes
    if _IndexEventNodes is None:
        _IndexEventNodes = initEventNodes()[1]
    return _IndexEventNodes

def get_projFilterDict():
    global _projFilterDict
    return _projFilterDict






def getETBs(node):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    mylist = column1s(column(EventNodes, node))       
    return [list(IndexEventNodes.keys())[list(IndexEventNodes.values()).index(x)] for x in mylist] # index from row id <-> etb

def getNodes(etb):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    return column1s(EventNodes[IndexEventNodes[etb]])

def setEventNodes(node, etb):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    EventNodes[IndexEventNodes[etb]][node] = 1
 
def unsetEventNodes(node, etb):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    EventNodes[IndexEventNodes[etb]][node] = 0    
    
def addETB(etb, etype):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    network = get_network()
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
    nodes = get_nodes()
    etbIDs = genericETB(parttype, projection)
    for projectionETB in etbIDs:
             addETB(projectionETB, projection)             
    for i in range(len(nodes[parttype])):
        setEventNodes(nodes[parttype][i], etbIDs[i])          


def genericETB(partType, projection):
    nodes = get_nodes()
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
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
    num = 1
    for etype in projection.leafs():
        num *= len(IndexEventNodes[etype])
    return num

def NumETBsByKey(etb, projection):
    EventNodes = get_EventNodes()
    IndexEventNodes = get_IndexEventNodes()
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


maxDist = max(sum(allPairs,[]))
