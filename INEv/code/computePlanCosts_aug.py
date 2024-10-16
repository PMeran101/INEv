#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:32:53 2021

@author: samira
"""
from placement_aug import *
import time
import csv
import sys


maxDist = max([max(x) for x in allPairs])

def getLowerBound(query): # lower bound -> for multiple projections, keep track of events sent as single sink and do not add up
    MS = []
    for e in query.leafs():        
        myprojs= [p for p in list(set(projsPerQuery[query]).difference(set([query]))) if totalRate(p)<rates[e] and not e in p.leafs()]
        if myprojs:
            MS.append(e)
        for p in [x for x in projsPerQuery[query] if e in x.leafs()]:
            part = returnPartitioning(p,p.leafs())            
            if e in part:
                MS.append(e)
    nonMS = [e for e in query.leafs() if not e in MS]  
    if nonMS:          
        minimalRate = sum(sorted([totalRate(e) for e in query.leafs() if not e in MS])) * longestPath
    else:
        minimalRate = min([totalRate(e) for e in query.leafs()]) * longestPath
    minimalProjs = sorted([totalRate(p) for p in projsPerQuery[query] if not p==query])[:len(list(set(MS)))-1]
    if not len(nonMS) == len(query.leafs()):
        minimalRate +=  sum(minimalProjs) * longestPath
    return minimalRate#, nonMS) 


def normalize(x, data):
    return x
    #return (x - min(data)) / (max(data) - min(data))

def main():
    
    
  
    Filters = []
    writeExperimentData = 0
    
    filename = "results"
    noFilter = 0 # NO FILTER
    
    #only write experiment data for shared costs, use ID and total costs for writing results of shared/seperate window
    if len(sys.argv) > 1:
         filename = sys.argv[1]
    if len(sys.argv) > 2:
        number_parents = sys.argv[2]
    # if len(sys.argv) > 1:
    #     
    # if len(sys.argv) > 2:
    #     noFilter = int(sys.argv[2])
    print(filename)
    ccosts = NEWcomputeCentralCosts(wl)
    #print("central costs : " + str(ccosts))
    centralHopLatency = max(allPairs[ccosts[1]])
    numberHops = sum(allPairs[ccosts[1]])
    print("centralCosts: " + str(ccosts[0]))
    print("Central Hops: " + str(numberHops))
    print("central Hop Latency: " + str(centralHopLatency))
    MSPlacements = {}
    curcosts = 1 
    start_time = time.time()
    
    hopLatency = {}
    
    #Reduce calls of initEventNodes
    init_eventNodes = initEventNodes()   
    EventNodes = init_eventNodes[0]
    IndexEventNodes = init_eventNodes[1]    
    
    myPlan = EvaluationPlan([], [])
    
    #transforming indexeventnodes into EvaluationPLan object with all entries as a instance
    #jede instance ist eine node ein event (nodes * events die produziert werden pro node)
    myPlan.initInstances(IndexEventNodes) # init with instances for primitive event types
    
    #mycombi = removeSisChains()
    unfolded = mycombi
    # print(unfolded)
    # print(projFilterDict.keys())
    # sharedDict = getSharedMSinput(unfolded, projFilterDict)    
    dependencies = compute_dependencies(unfolded)
    processingOrder = sorted(compute_dependencies(unfolded).keys(), key = lambda x : dependencies[x] ) # unfolded enthält kombi   
    costs = 0
    #processingOrder = compute_dependencies_alt(unfolded) # alternative processing order //
    for projection in processingOrder:  #parallelize computation for all projections at the same level
            if set(unfolded[projection]) == set(projection.leafs()): #initialize hop latency with maximum of children
               hopLatency[projection] = 0 
            else:
                hopLatency[projection] = max([hopLatency[x] for x in unfolded[projection] if x in hopLatency.keys()])

          
            partType = returnPartitioning(projection, unfolded[projection], criticalMSTypes)
            if False : 
                MSPlacements[projection] = partType
                result = computeMSplacementCosts(projection, unfolded[projection], partType, sharedDict, noFilter)
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[1]
                
                myPlan.addProjection(result[2]) #!
                
                for newin in result[2].spawnedInstances: # add new spawned instances
                    myPlan.addInstances(projection, newin) 
      
               #adding routing keys
                myPlan.updateInstances(result[3]) #! update instances
            
                
                Filters += result[4]
                # if partType, and projection in wl and partType kleene component of projection, add sink
                print("MS " + str(projection) + " At: " + str(partType) + " PC: " + str(additional) + " Hops:" + str(result[1]))


                if projection.get_original(wl) in wl and partType[0] in list(map(lambda x: str(x), projection.get_original(wl).kleene_components())):
                    
                    
                    result =  ComputeSingleSinkPlacement(projection.get_original(wl), [projection], noFilter)
                    additional = result[0]
                    costs += additional
                    print("SiS Sink for Kleene:" + str(projection.get_original(wl)) + " PC: " + str(additional) + " Hops:" + str(result[1]))
            else:
                
                result = ComputeSingleSinkPlacement(projection, unfolded[projection], noFilter)
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[2]
                myPlan.addProjection(result[3]) #!
                for newin in result[3].spawnedInstances: # add new spawned instances
                   
                    myPlan.addInstances(projection, newin)
                
                myPlan.updateInstances(result[4]) #! update instances
                Filters += result[5]
               
                print("SiS " + str(projection) + "PC: " + str(additional)  + " Hops: " + str(result[2]))
                
    mycosts = costs/ccosts[0]
    print("INEv Transmission " + str(costs) )
    if len(wl)>1 or wl[0].hasKleene() or wl[0].hasNegation():
        lowerBound = 0
    else:
      for query in wl:
        lowerBound= getLowerBound(query)
    print("Lower Bound: " + str(lowerBound / ccosts[0]))

    print("Transmission Ratio: " + str(mycosts))
    print("INEv Depth: " + str(float(max(list(dependencies.values()))+1)/2))
    
    ID = int(np.random.uniform(0,10000000))
    
    with open('EvaluationPlan',  'wb') as EvaluationPlan_file:
        pickle.dump([myPlan, ID, MSPlacements], EvaluationPlan_file)
    
    totaltime = str(round(time.time() - start_time, 2))


            
    #getNetworkParameters, selectivityParameters, combigenParameters
        
    with open('networkExperimentData', 'rb') as networkExperimentData_file: 
          networkParams = pickle.load(networkExperimentData_file)   
    with open('selectivitiesExperimentData', 'rb') as selectivities_file: 
          selectivityParams  = pickle.load(selectivities_file)   
    with open('combiExperimentData', 'rb') as combiExperimentData_file: 
          combigenParams = pickle.load(combiExperimentData_file) 
    with open('processingLatency', 'rb') as processingLatency_file: 
          processingLatencyParams = pickle.load(processingLatency_file)            
                      
    ID = int(np.random.uniform(0,10000000))
    hopfactor = processingLatencyParams[2]
  
    
    
   
    hoplatency = 0    
    totalLatencyRatio = 0
    myResult = [ID, mycosts, ccosts[0], costs,Filters, networkParams[3], networkParams[0], networkParams[2], len(wl), combigenParams[3], selectivityParams[0], selectivityParams[1], combigenParams[1], longestPath, totaltime, hoplatency, float(max(list(dependencies.values()))/2), totalLatencyRatio, ccosts[0], lowerBound / ccosts[0], networkParams[1], number_parents]
    schema = ["ID", "TransmissionRatio", "Transmission","INEvTransmission","FilterUsed", "Nodes", "EventSkew", "EventNodeRatio", "WorkloadSize", "NumberProjections", "MinimalSelectivity", "MedianSelectivity","CombigenComputationTime", "Efficiency", "PlacementComputationTime", "HopCount", "Depth", "ProcessingLatencyRatio", "CentralTransmission", "LowerBound", "EventTypes", "MaximumParents"] 
    
 
    new = False
    try:
         f = open("../res/"+str(filename)+".csv")   
    except FileNotFoundError:
         new = True           
        
    with open("../res/"+str(filename)+".csv", "a") as result:
       writer = csv.writer(result)  
       if new:
           writer.writerow(schema)              
       writer.writerow(myResult)
      

    with open('CentralEvaluationPlan',  'wb') as CentralEvaluationPlan_file:
        pickle.dump([ccosts[1],ccosts[3], wl], CentralEvaluationPlan_file)
    
    with open('ExperimentID',  'wb') as ExperimentID_file:
        pickle.dump([ID,ccosts[0]], ExperimentID_file)
    
    if writeExperimentData:
        with open('ExperimentResults',  'wb') as ExperimentID_file: 
            pickle.dump([ID,costs], ExperimentID_file)  # write only INEv Costs and ID for timewindow exp

    #for q in wl:
    #    print(projrates[q][1])
#    with open('ExperimentResults',  'wb') as ExperimentID_file: -> for adaptivity & topology?
#        pickle.dump([ID,mycosts,ccosts[0]], ExperimentID_file)  

if __name__ == "__main__":
    main()                    