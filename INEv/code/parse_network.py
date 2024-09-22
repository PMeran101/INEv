import string
from binary_helper import save_file, load_file

# Global caches for lazy loading
_nodes_cache = None
_network_cache = None
_rates_cache = None
_prim_events_cache = None
_instances_cache = None

def load_network_data():
    """
    Load the raw network data from a file using the load_file() function.
    
    Returns:
        list: The raw network data loaded from the 'network' file.
    """
    return load_file('network')

def get_network():
    """
    Retrieve the network data, loading it only once and caching the result.
    
    Returns:
        dict: A dictionary where each key is a node index, and the value is a list of event types produced by that node.
    """
    global _network_cache
    if _network_cache is None:
        print("Loading network")
        _network_cache = load_network()
    return _network_cache

def load_network():
    """
    Generate a dictionary that maps node indices to event types based on their event rates.
    
    Returns:
        dict: A dictionary where each key is a node index and the value is a list of event types (A, B, C, etc.) for that node.
    """
    nw = load_network_data()
    network = {}
    ind = 0
    for node in nw:
        network[ind] = [string.ascii_uppercase[eventtype]
                        for eventtype in range(len(node.eventrates))
                        if node.eventrates[eventtype] > 0]
        ind += 1
    return network

def get_rates():
    """
    Retrieve the rates dictionary, loading it only once and caching the result.
    
    Returns:
        dict: A dictionary where the key is the event type (A, B, etc.) and the value is the event rate.
    """
    global _rates_cache
    if _rates_cache is None:
        print("Loading rates")
        _rates_cache = load_rates()
    return _rates_cache

def load_rates():
    """
    Generate a dictionary of event rates for each event type.
    
    Returns:
        dict: A dictionary where the key is an event type (A, B, etc.), and the value is the event rate for that type.
    """
    nw = load_network_data()
    rates = {}
    for node in nw:
        for eventtype in range(len(node.eventrates)):
            event = string.ascii_uppercase[eventtype]
            if node.eventrates[eventtype] > 0 and event not in rates:
                rates[event] = float(node.eventrates[eventtype])
    return rates

def get_prim_events():
    """
    Retrieve the list of primitive event types, loading it only once and caching the result.
    
    Returns:
        list: A list of unique primitive event types (A, B, C, etc.).
    """
    global _prim_events_cache
    if _prim_events_cache is None:
        print("Loading primitive events")
        _prim_events_cache = load_prim_events()
    return _prim_events_cache

def load_prim_events():
    """
    Generate a list of primitive event types that are produced across the network.
    
    Returns:
        list: A list of event types (A, B, C, etc.) that are produced by any node in the network.
    """
    nw = load_network_data()
    prim_events = []
    for node in nw:
        for eventtype in range(len(node.eventrates)):
            event = string.ascii_uppercase[eventtype]
            if node.eventrates[eventtype] > 0 and event not in prim_events:
                prim_events.append(event)
    return prim_events

def get_nodes():
    """
    Retrieve the nodes dictionary, loading it only once and caching the result.
    
    Returns:
        dict: A dictionary where the key is the event type, and the value is a list of node indices that produce that event.
    """
    global _nodes_cache
    if _nodes_cache is None:
        print("Loading nodes")
        _nodes_cache = load_nodes()
    return _nodes_cache

def load_nodes():
    """
    Create a dictionary mapping event types to nodes that produce the event.
    
    Returns:
        dict: A dictionary where the key is an event type (A, B, etc.) and the value is a list of node indices that produce that event.
    """
    network = get_network()  # Use the cached network
    nodes = {}
    for node_index, event_list in network.items():
        for event in event_list:
            if event not in nodes:
                nodes[event] = [node_index]
            else:
                nodes[event].append(node_index)
    return nodes

def instances_func(proj):
    """
    Calculate the number of instances for a given projection of events based on the nodes producing them.
    
    Args:
        proj (list): A list of event types or groups of event types.
    
    Returns:
        int: The total number of instances for the given event projection.
    """
    nodes = get_nodes()
    num = 1
    for i in proj:
        if len(i) == 1:
            num *= len(nodes[i])
        else:
            for j in i:
                num *= len(nodes[j])
    return num

def get_instances():
    """
    Retrieve the instances dictionary, loading it only once and caching the result.
    
    Returns:
        dict: A dictionary where the key is the event type (A, B, C, etc.), and the value is the number of nodes producing that event.
    """
    global _instances_cache
    if _instances_cache is None:
        print("Loading instances")
        _instances_cache = load_instances()
    return _instances_cache

def load_instances():
    """
    Generate a dictionary mapping event types to the number of nodes that produce them.
    
    Returns:
        dict: A dictionary where the key is an event type (A, B, etc.), and the value is the number of nodes that produce that event.
    """
    nodes = get_nodes()  # Use the cached nodes
    prim_events = get_prim_events()  # Use the cached primitive events
    instances = {event: len(nodes[event]) for event in prim_events}
    return instances
