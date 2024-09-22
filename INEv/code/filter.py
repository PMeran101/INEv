#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 13:03:07 2021

@author: samira

Output selector related methods.
"""
from structures import get_IndexEventNodes, getLongest, getNumETBs
from parse_network import get_nodes,get_rates,get_instances
from binary_helper import load_file

singleSelectivities = load_file("singleSelectivities")
projrates = load_file("projrates")

def computePromisingType(projection):
    "Loading data from parse_network"
    rates = get_rates()
    
    "Loading data from structures"
    IndexEventNodes = get_IndexEventNodes()
    longestPath = getLongest()
    
    promisingEvent = "X"
    currentSave = 0
    for primEvent in projection.leafs():
        decomposedSum = getDecomposedTotal([primEvent], projection)
        rateSaved = (projrates[projection][1] * numETBs("", projection)) - ((longestPath * rates[primEvent] * len(IndexEventNodes[primEvent])) +  decomposedSum)
        if rateSaved > currentSave and rateSaved > 0: #saved rate must include costs for routing promising event to dest, prob not necessary 
            currentSave = rateSaved
            promisingEvent = primEvent
    if promisingEvent != "X":
        return(promisingEvent, getDecomposed([promisingEvent], projection))
    else:
        return(promisingEvent, getDecomposed([promisingEvent], projection))
        
        
def numETBs(primEvents, projection):
    "Loading data from structures"
    IndexEventNodes = get_IndexEventNodes()
    count = 1
    for event in projection.leafs():
        if not event in primEvents:
            count *= len(IndexEventNodes[event])
    return count

def getDecomposed(primEvents, projection):
    "Loading data from parse_network"
    rates = get_rates()
    
    mysum = 0
    for event in  projection.leafs():
        if not event in primEvents:
            myKey = getKeySingleSelect(event, projection)
            mysum += singleSelectivities[myKey] * rates[event]
    return mysum        

def getDecomposedTotal(primEvents, projection): 
    "Loading data from parse_network"
    rates = get_rates()
    instances = get_instances()
    
    
    mysum = 0
    for event in [x for x in projection.leafs() if not x in primEvents]:    # implement for list of primEvents, to use during placement    
            myKey = getKeySingleSelect(event, projection)
            mysum += singleSelectivities[myKey] * rates[event] * instances[event]
    return mysum 
            
def getKeySingleSelect(primEvent, projection):
    myString = primEvent + "|" + "".join(sorted(projection.leafs()))
    return myString

def additionalFilters(projection, promisingEvent):
    "Loading data from parse_network"
    rates = get_rates()
    
    "Loading data from structures"
    IndexEventNodes = get_IndexEventNodes()
    longestPath = getLongest()
    
    additionalFiltersList = []
    for event in projection.leafs():
        if not event  == promisingEvent:
            myKey = getKeySingleSelect(event, projection)
            #commonETBS = len(IndexEventNodes[promisingEvent]) * numETBs([event, promisingEvent],projection)
            commonETBS = numETBs([event, promisingEvent],projection)
            additionalSavings = commonETBS *  singleSelectivities[myKey] * rates[event]
            additionalSavings -= rates[event] * longestPath        
            if additionalSavings > 0 :
                additionalSavings += rates[event] * longestPath # do not substract by upper bound of sending filters, as actual costs can be computed during placement
                additionalSavings *= len(IndexEventNodes[event])
                additionalFiltersList.append((event, additionalSavings))
    return additionalFiltersList 

ProjFilterDict = {}

def returnProjFilterDict(projection):
            ''' return for a projection with different subsets of primitive events that can be used as filters and the resulting rate of the projection '''
            ProjFilterDict = {}
            #totalRate = numETBs("", projection) * projrates[projection][1]
            totalRate = projrates[projection][1] #singleRate
            ProjFilterDict[projection] = {}
            ProjFilterDict[projection][""] = (totalRate, 0)
            promising = computePromisingType(projection)
            
            if promising[0] != "X" :
               currentKey = promising[0]
               currentRate = promising[1] 
               ProjFilterDict[projection][currentKey] = (currentRate, 0) 

            return ProjFilterDict    
               
def getMaximalFilter(filterdict, proj, *args):
    if args:
        if args[0] == 1:
            return sorted(filterdict[proj].keys(), key = len)[0]   # USED TO SUPRESS FILTER!!!
    return sorted(filterdict[proj].keys(), key = len, reverse = True)[0]          


def getPMs(projection, myfilter):
    totalETBs = numETBs("", projection)
    return 0


def returnAdditionalFilterDict():
    additional = {}
    for i in projrates.keys():
      additional[i] = {}
      myrate = projrates[i][1] * getNumETBs(i)
      for k in i.leafs():
          if getDecomposedTotal([k], i) < myrate:
              additional[i][k] = getDecomposed([k], i)
    return additional
