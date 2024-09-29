
"""
Generate network with given size (nwsize), node-event ratio (node_event_ratio), 
number of event types (num_eventtypes), event rate skew (eventskew)-
"""
import sys
import pickle
import numpy as np
import string
import random
from Node import Node
import argparse

""" Experiment network rates 

average event rates for google cluster data set first 12h, timewindow 30 min, 20 nodes
#ev = [[0,855, 212, 24, 400, 129, 0, 0.005,0.05]]
    
event rates push-pull comparison:
small:
ev_PP = [[0.2994830154521548 , 0.14354286459134916 , 0.009297964702092328 , 0.2568894819120937 , 0.0771288310049754 ,  0.009297964702092328, 0.2994830154521548 , 0.26592179047984055 ]]    
big: 
ev =  [[1, 6, 1, 1, 1, 7, 8777, 1, 542, 72, 39, 1, 1, 318, 3, 1, 17, 2, 12, 2]]


#ev =  [[1485,1000, 161, 300, 480, 229, 1, 1,20]] # average rates google cluster experiment
#ev =  [[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]] # average rates citibike experiment

"""    


with open('rates',  'rb') as  rates_file:
        res = pickle.load(rates_file)
        event_rates_file = res[0]
        event_node_assignment = res[1]
        

def generate_eventrates(eventskew,numb_eventtypes):
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    eventrates = eventrates / np.sum(eventrates)
    eventrates = eventrates * 10000
    return eventrates

# At one Node show in Array the Events which are generated at each node
# Looping through all Eventrates 
def generate_events(eventrates, n_e_r):
    myevents = []
    for i in range(len(eventrates)):
        x = np.random.uniform(0,1)
        if x < n_e_r:
            myevents.append(eventrates[i])
        else:
            myevents.append(0)
    
    return myevents

def regain_eventrates(nw):
    eventrates = [0 for i in range(len(nw[0]))]
    interdict = {}
    for i in nw:
        for j in range(len(i)):
            if i[j] > 0 and not j in interdict.keys():
                interdict[j] = i[j]
    for j in sorted(interdict.keys()):
        eventrates[j] = interdict[j]
    return eventrates 

def allEvents(nw):
    for i in range(len(nw[0])) :
        column = [row[i] for row in nw]
        if sum(column) == 0:
            return False
    return True

def swapRatesMax(eventtype, rates, maxmin):
    rates = list(rates)
    if maxmin == 'max':
        maxRate = max(rates)
    else: 
        maxRate = min(rates)
    maxIndex = rates.index(maxRate)
    eventTypeIndex = string.ascii_uppercase.index(eventtype)
    newRates = [x for x in rates]
    newRates[maxIndex], newRates[eventTypeIndex] =   newRates[eventTypeIndex], newRates[maxIndex]
    return newRates

def swapRates(numberofswaps,rates):
    newRates = [x for x in rates]
    for i in range(numberofswaps):        
        newRates = [x for x in newRates]
        index = int(len(newRates)/2)
        left = index - (i+1) 
        right = index + i
        newRates[left], newRates[right] = newRates[right], newRates[left]
    return newRates

def generate_assignment(nw, eventtypes):
    assignment = {k: [] for k in range(eventtypes)}
    for node in range(len(nw)):
        for eventtype in range(len(nw[node])):
            if nw[node][eventtype] > 0:
                assignment[eventtype].append(node)        
    return assignment

def generateFromAssignment(assignment, rates, nwsize):
    return [[rates[eventtype]  if x in assignment[eventtype] else 0 for eventtype in assignment.keys()] for x in range(nwsize)]


def parse_arguments():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Simulation parameters")

    # Add arguments with default values
    parser.add_argument('--nwsize', '-nw', type=int, default=10, help='Network size (default: 10)')
    parser.add_argument('--node_event_ratio', '-ner', type=float, default=0.5, help='Node event ratio (default: 0.5)')
    parser.add_argument('--num_eventtypes', '-ne', type=int, default=6, help='Number of event types (default: 20)')
    parser.add_argument('--eventskew', '-es', type=float, default=1.3, help='Event skew (default: 1.3)')
    parser.add_argument('--swaps', '-sw', type=int, default=0, help='Number of swaps (default: 0)')
    parser.add_argument('--toFile', '-tf', action='store_true', help='Write event types to file')
    parser.add_argument('--max_parents', '-mp', type=int, default=1, help='Maximum number of parents per node (default: 1)')
    parser.add_argument('--eventtype', '-et', type=str, default=None, help='Event type for experiments')
    parser.add_argument('--param', '-p', type=str, default=None, help='Parameter for event type (max/min) in experiments')

    # Parse the arguments
    args = parser.parse_args()

    # Return parsed arguments as a dictionary for convenience
    return vars(args)

def main():
        # Parse command-line arguments
    args = parse_arguments()

    # Now you can access the parsed arguments from the dictionary
    nwsize = args['nwsize']
    node_event_ratio = args['node_event_ratio']
    num_eventtypes = args['num_eventtypes']
    eventskew = args['eventskew']
    toFile = args['toFile']
    swaps = args['swaps']
    max_parents = args['max_parents']
    eventtype = args['eventtype']
    param = args['param']

    # The rest of your simulation logic goes here
    print(f"Max parents for nodes: {max_parents}")
    print(f"Network size: {nwsize}, Node event ratio: {node_event_ratio}, Event skew: {eventskew}")
    print(f"Number of event types: {num_eventtypes}, Swaps: {swaps}, To file: {toFile}")
    print(f"Event type: {eventtype}, Param: {param}")

    #eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
    eventrates =  generate_eventrates(eventskew,num_eventtypes)
    
    
    def create_random_tree(nwsize, eventrates, node_event_ratio, max_parents: int = 1):
        if nwsize <= 0:
            return None
        import math
        # Initialize the list to store all nodes
        nw = []

        levels = math.ceil(math.log2(nwsize))
        print(levels)
        # Create the root node
        root = Node(id=0, compute_power=math.inf, memore=math.inf )#, eventrate=generate_events(eventrates, node_event_ratio))
        nw.append(root)

        # Track nodes by level to manage the structure and prevent imbalance
        level_nodes = {0: [root]}

        # Create remaining nodes and build the tree
        for node_id in range(1, nwsize):
            # Determine the level for the new node
            level = min(levels - 1, node_id // (nwsize // levels) + 1)
            
            # Compute power and memory decrease as the level increases
            compute_power = levels - level
            memore = levels - level

            # Create the new node
            new_node = Node(id=node_id, compute_power=compute_power, memore=memore)

            # Ensure level-specific nodes exist in the dictionary
            if level not in level_nodes:
                level_nodes[level] = []
            
            # Randomly choose the number of parents between 1 and max_parents
            num_parents = random.randint(1,max_parents)
                
            # Randomly choose parents from the previous level
            parent_nodes = random.sample(level_nodes[level - 1], min(len(level_nodes[level - 1]), num_parents))

            # Set parents and add the new node to each parent's list of children
            for parent_node in parent_nodes:
                new_node.Parent.append(parent_node)
                parent_node.Child.append(new_node)


            # Add new node to the list and to the level-specific tracking
            nw.append(new_node)
            level_nodes[level].append(new_node)

        # Assign event rates to leaf nodes and initialize non-leaf nodes with empty event rates
        for node in nw:
            if len(node.Child) == 0:
   
                evtrate = generate_events(eventrates, node_event_ratio)

                with open('PrimitiveEvents', 'wb') as f:
                    pickle.dump(evtrate, f)
                node.eventrates = evtrate
            else:
                node.eventrates = [0] * len(eventrates)

        # post_order_sum_events(root)
        return root, nw
    
    nw = []
    root, nw = create_random_tree(nwsize, eventrates, node_event_ratio, max_parents)
    # for node in range(nwsize):
    #     no = Node(node, 0, 0, generate_events(eventrates, node_event_ratio))
    #     nw.append(no)
        
    #print(nw)     
    
    """
    TODO Rebuild the check for allEvents again
    """
    # print(allEvents(nw))
    # while not allEvents(nw):
    #     nw = []    

    #     for node in range(nwsize):
    #         nw.append(generate_events(eventrates, node_event_ratio))


    ## INSERT NETWORK HERE
    #nw = [[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40]]

    networkExperimentData = [eventskew, num_eventtypes, node_event_ratio, nwsize, min(eventrates)/max(eventrates)]
    with open('networkExperimentData', 'wb') as networkExperimentDataFile:
        pickle.dump(networkExperimentData, networkExperimentDataFile)
    
    with open('network', 'wb') as network_file:
          pickle.dump(nw, network_file)      
          
         
    
   
    print("NETWORK")  
    print("--------") 
    for i in range(len(nw)):
        print(nw[i])
    print("\n")
    
    nw[0].visualize_tree(nw[0])
    
    
        
if __name__ == "__main__":
    main()


        



