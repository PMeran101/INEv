
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

def main():

    
    #default values for simulation 
    nwsize = 10
    node_event_ratio = 0.5
    num_eventtypes = 20
    eventskew = 1.3
    toFile = False
    swaps = 0   
    
      
    if len(sys.argv) > 1: #network size
        nwsize =int(sys.argv[1])
    if len(sys.argv) > 2:
        node_event_ratio = float(sys.argv[2]) # event node ratio
    if len(sys.argv) > 3: # event skew
        eventskew = float(sys.argv[3]) 
    if len(sys.argv) > 4: # size event universe        
        num_eventtypes = int(sys.argv[4])
    if len(sys.argv) > 4 and len(sys.argv) < 7 :   #write event types to file  
        #eventrates = generate_eventrates(eventskew,num_eventtypes)   
        toFile = False
    if len(sys.argv) > 5:     # generate event types from file and apply given number of swaps
        eventrates = event_rates_file # get event rates for event types
        nodeassignment = event_node_assignment  # get node assignment, which node generates which event types
        swaps = int(sys.argv[5]) # number of swaps
        toFile = False # do not save generated rates to file
        
    if len(sys.argv) > 6:        # for setting event types to min/max rates (kleene, nseq experiments)
        eventtype = str(sys.argv[6]) 
    
    if len(sys.argv) > 7: # set eventtype to param=max/min rate (kleene, nseq experiments)
        param = str(sys.argv[7])
        eventrates = swapRatesMax(eventtype, eventrates, param)   
    
    
    #eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
    eventrates =  generate_eventrates(eventskew,num_eventtypes)
    
        
    #if toFile:
    #    eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
    #    nw= []
    #    for node in range(nwsize):
    #        nw.append(generate_events(eventrates, node_event_ratio))
    #    
    #    nodeassignment = generate_assignment(nw, num_eventtypes)
    #    with open('rates', 'wb') as rates_file:
    #          pickle.dump((eventrates, nodeassignment), rates_file) 
                
    
    #if not toFile:
    #   nw= generateFromAssignment(nodeassignment, eventrates,  nwsize)

    #random.shuffle(eventrates)
    
    #eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
    #eventrates =  [990,666,107,200,320,152, 0.6, 0.6,13.3] #google 30
    #eventrates  =  [1485,1000, 161, 300, 480, 229, 1, 1,20] #google 20
    #eventrates = [2970, 2000, 322, 600, 960, 458,2, 2, 40] # google 10
    
    #eventrates =  [0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60] # citibike 20
    #eventrates = [1,12,2,272, 2000, 500, 1, 60, 120] # citibike 10
    ##eventrates = [0.3, 4, 0.6, 91, 666, 166, 0.3, 20, 40] # citibike 30

    #eventrates = [2,20,30,6,10,1,2, 2, 40] 
    # def post_order_sum_events(node):
    #     if not node:
    #         return

    #     # Initialize the event rates sum as empty or zeros
    #     if node.Child is not None:
    #         node.eventrates = [0] * len(node.eventrates)

    #     # Traverse the child nodes first
    #     child = node.Child
    #     while child is not None:
    #         post_order_sum_events(child)
    #         # Sum the child event rates into the parent node
    #         node.eventrates = [sum(x) for x in zip(node.eventrates, child.eventrates)]
    #         child = child.Sibling
    
    
    def create_random_tree(nwsize, eventrates, node_event_ratio):
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

            # Randomly choose a parent from the previous level
            parent_node = random.choice(level_nodes[level - 1])

            # Add the new node as a child or sibling
            if parent_node.Child is None:
                parent_node.Child = new_node
            else:
                current = parent_node.Child
                while current.Sibling is not None:
                    current = current.Sibling
                current.Sibling = new_node

            # Set the new node's parent
            new_node.Parent = parent_node

            # Add new node to the list and to the level-specific tracking
            nw.append(new_node)
            level_nodes[level].append(new_node)

        # Assign event rates to leaf nodes and initialize non-leaf nodes with empty event rates
        for node in nw:
            if node.Child is None:
   
                evtrate = generate_events(eventrates, node_event_ratio)

                with open('PrimitiveEvents', 'wb') as f:
                    pickle.dump(evtrate, f)
                node.eventrates = evtrate
            else:
                node.eventrates = [0] * len(eventrates)

        # post_order_sum_events(root)
        return root, nw
    
    nw = []
    root, nw = create_random_tree(nwsize, eventrates, node_event_ratio)
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
          
         
    
   
    # print("NETWORK")  
    # print("--------") 
    # for i in range(len(nw)):
    #     print(nw[i])
    # print("\n")
    
    nw[0].visualize_tree(nw[0])
    
    
        
if __name__ == "__main__":
    main()


        



