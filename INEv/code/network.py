import string
from binary_helper import save_file, load_file

# Load the network data from the file
def load_network_data():
    return load_file('network')

# Create the network dictionary based on event rates
def load_network():
    nw = load_network_data()
    network = {}
    ind = 0
    for node in nw:
        network[ind] = [string.ascii_uppercase[eventtype]
                        for eventtype in range(len(node.eventrates))
                        if node.eventrates[eventtype] > 0]
        ind += 1
    return network

# Create the rates dictionary based on event rates
def load_rates():
    nw = load_network_data()
    rates = {}
    for node in nw:
        for eventtype in range(len(node.eventrates)):
            event = string.ascii_uppercase[eventtype]
            if node.eventrates[eventtype] > 0 and event not in rates:
                rates[event] = float(node.eventrates[eventtype])
    return rates

# Create the list of primitive events
def load_prim_events():
    nw = load_network_data()
    prim_events = []
    for node in nw:
        for eventtype in range(len(node.eventrates)):
            event = string.ascii_uppercase[eventtype]
            if node.eventrates[eventtype] > 0 and event not in prim_events:
                prim_events.append(event)
    return prim_events

# Return the events for a given node
def events(node, network):
    return network.get(node, [])

# Load the nodes where each event occurs
def load_nodes():
    print("Loading nodes")
    network = load_network()
    nodes = {}
    for node_index, event_list in network.items():
        for event in event_list:
            if event not in nodes:
                nodes[event] = [node_index]
            else:
                nodes[event].append(node_index)
    return nodes

# Calculate the number of instances for a given project
def instances_func(proj, nodes):
    num = 1
    for i in proj:
        if len(i) == 1:
            num *= len(nodes[i])
        else:
            for j in i:
                num *= len(nodes[j])
    return num

# Load the instances for each primitive event
def load_instances():
    nodes = load_nodes()
    prim_events = load_prim_events()
    instances = {event: len(nodes[event]) for event in prim_events}
    return instances
