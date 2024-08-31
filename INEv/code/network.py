import string
import pickle
"""
used to load and process following variables:
- network
- rates
- primEvents
- nodes
- instances 
"""


# Module-level variables to store the loaded and processed data
_network = None
_rates = None
_primEvents = None
_nodes = None
_instances = None

def load_network(file_path):
    """Load the network from a pickle file."""
    with open(file_path, 'rb') as nw_file:
        return pickle.load(nw_file)

def process_network(nw):
    """Process the network data and populate the module-level variables."""
    global _network, _rates, _primEvents, _nodes, _instances

    _network = {}
    _rates = {}
    _primEvents = []
    _nodes = {}

    ind = 0
    for node in nw:
        _network[ind] = []
        for eventtype in range(len(node.eventrates)):
            if node.eventrates[eventtype] > 0:
                event = string.ascii_uppercase[eventtype]
                _network[ind].append(event)
                if event not in _primEvents:
                    _primEvents.append(event)
                if event not in _rates:
                    _rates[event] = float(node.eventrates[eventtype])
        ind += 1

    # Build nodes structure
    for i in _network.keys():
        for event in _network[i]:
            if event not in _nodes:
                _nodes[event] = [i]
            else:
                _nodes[event].append(i)

    # Calculate instances
    _instances = {}
    for event in _primEvents:
        _instances[event] = len(_nodes[event])

def get_network(file_path="network"):
    """Return the network structure, loading and processing if necessary."""
    global _network
    if _network is None:
        if file_path is None:
            raise ValueError("Network data must be loaded at least once with a valid file path.")
        nw = load_network(file_path)
        process_network(nw)
    return _network

def get_rates(file_path="network"):
    """Return the rates dictionary, loading and processing if necessary."""
    global _rates
    if _rates is None:
        if file_path is None:
            raise ValueError("Network data must be loaded at least once with a valid file path.")
        nw = load_network(file_path)
        process_network(nw)
    return _rates

def get_primEvents(file_path="network"):
    """Return the list of primary events, loading and processing if necessary."""
    global _primEvents
    if _primEvents is None:
        if file_path is None:
            raise ValueError("Network data must be loaded at least once with a valid file path.")
        nw = load_network(file_path)
        process_network(nw)
    return _primEvents

def get_nodes(file_path="network"):
    """Return the nodes dictionary, loading and processing if necessary."""
    global _nodes
    if _nodes is None:
        if file_path is None:
            raise ValueError("Network data must be loaded at least once with a valid file path.")
        nw = load_network(file_path)
        process_network(nw)
    return _nodes

def get_instances(file_path="network"):
    """Return the instances dictionary, loading and processing if necessary."""
    global _instances
    if _instances is None:
        if file_path is None:
            raise ValueError("Network data must be loaded at least once with a valid file path.")
        nw = load_network(file_path)
        process_network(nw)
    return _instances

def events(node, file_path="network"):
    """Return the events for a given node, loading and processing if necessary."""
    network = get_network(file_path)
    return network[node]

def instances_func(proj, file_path="network"):
    """Calculate the number of instances based on the project."""
    nodes = get_nodes(file_path)
    num = 1
    for i in proj:
        if len(i) == 1:
            num *= len(nodes[i])
        else:
            for j in i:
                num *= len(nodes[j])
    return num
