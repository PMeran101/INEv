import pickle
import os
import sys
from EvaluationPlan import EvaluationPlan, Projection, Instance
from tree import Tree
import string

def load_pickle(file_name):
    """
    Helper function to load a pickle file.

    Parameters:
    - file_name (str): The name of the pickle file to load.

    Returns:
    - The object loaded from the pickle file.
    """
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def calculate_event_rates(source_node_names, nodes_dict):
    """
    Calculate event rates for each primitive event and per node instance.

    Parameters:
    - source_node_names (list): List of node names (e.g., ['H2', 'P3']).
    - nodes_dict (dict): Dictionary mapping node IDs to Node objects.

    Returns:
    - event_rates (dict): Total event rates per event type (e.g., {'H': 3855, 'P': 60}).
    - rates_per_node (dict): Event rates per node instance (e.g., {'H2': 1285, 'P3': 20}).
    """
    event_rates = {}
    rates_per_node = {}

    for node_name in source_node_names:
        event_type = node_name[0]  # Extract the event type (e.g., 'H', 'P', 'G')
        
        # Ensure that the node name is in the correct format (e.g., 'H2', 'P3')
        if len(node_name) > 1 and node_name[1:].isdigit():
            node_id = int(node_name[1:])  # Extract the node ID (e.g., '2', '3')
            node = nodes_dict[node_id]

            event_index = string.ascii_uppercase.index(event_type.upper())  # Get the index of the event
            event_rate = node.eventrates[event_index]

            # Initialize the event rate in event_rates if it doesn't exist
            if event_type not in event_rates:
                event_rates[event_type] = 0
            if node_name not in rates_per_node:
                rates_per_node[node_name] = event_rate

            # Add the event_rate to the corresponding key in the dictionary
            event_rates[event_type] += event_rate
        else:
            print(f"Skipping invalid node name format: {node_name}")

    return event_rates, rates_per_node

def calculate_transmissions(event_rate, path):
    """
    Calculate total transmissions for an event instance.

    Parameters:
    - event_rate (float): The event rate.
    - path (list): The path the event takes (list of node IDs).

    Returns:
    - total_transmissions (float): Total transmissions = event rate * number of hops.
    """
    num_hops = len(path) - 1  # Number of hops (nodes the event passes through)
    total_transmissions = event_rate * num_hops  # Total transmissions = event rate * hops
    return total_transmissions

def calculate_selectivity(event_structure, single_select, selectivities):
    """
    Calculate the selectivity based on the event structure.

    Parameters:
    - event_structure: Event structure, which can be a primitive event (str) or a dict for composite events.
    - single_select (dict): Dictionary of single selectivities for events.
    - selectivities (dict): Dictionary of selectivities for composite events.

    Returns:
    - selectivity (float): The calculated selectivity.
    """
    if isinstance(event_structure, dict):
        operator = event_structure['operator']
        events = event_structure['events']
        if operator in ['AND', 'SEQ']:
            # Construct the key for selectivity lookup
            key = ''.join(events)
            selectivity = selectivities.get(key, None)
            if selectivity is None and operator == 'AND':
                # Try permutations since order doesn't matter in AND
                from itertools import permutations
                for perm in permutations(events):
                    perm_key = ''.join(perm)
                    selectivity = selectivities.get(perm_key, None)
                    if selectivity is not None:
                        break
            if selectivity is None:
                selectivity = 1.0  # Default value if not found
            return selectivity
        else:
            print(f"Unknown operator: {operator}")
            return 1.0
    else:
        # Primitive events have a selectivity of 1.0
        return 1.0

def calculate_dynamic_push_pull_transmissions(event_rates, rates_per_node, paths, single_select, selectivities, projection_structure, projection_events):
    """
    Calculate total transmissions with and without optimization for any set of events dynamically,
    considering operators like AND and SEQ.

    Parameters:
    - event_rates (dict): Dictionary of event rates for each event type (e.g., {'G': 55, 'H': 3855, 'P': 60}).
    - rates_per_node (dict): Event rate per node.
    - paths (dict): Routing paths for each event instance.
    - single_select (dict): Single selectivities for events (e.g., {'H|GH': 0.0347887}).
    - selectivities (dict): Selectivities for composite events (e.g., {'GH': 0.0012}).
    - projection_structure (list): Structured representation of the projection, including operators.
    - projection_events (list): List of events in the projection (e.g., ['G', 'H', 'P']).
    """
    # Calculate adjusted event rates for each event or composite event
    adjusted_event_rates = {}
    for event_structure in projection_structure:
        selectivity = calculate_selectivity(event_structure, single_select, selectivities)
        if isinstance(event_structure, dict):
            operator = event_structure['operator']
            events = event_structure['events']
            # For composite events, determine how to combine event rates
            event_rates_list = [event_rates.get(e, 0) for e in events]
            combined_event_rate = min(event_rates_list) * selectivity
            key = (operator, tuple(events))
        else:
            # Primitive event
            event_rate = event_rates.get(event_structure, 0)
            combined_event_rate = event_rate * selectivity  # selectivity is 1.0 for primitives
            key = event_structure
        adjusted_event_rates[key] = combined_event_rate

    # Find the event with the minimum adjusted event rate
    min_event = min(adjusted_event_rates, key=adjusted_event_rates.get)
    min_event_rate = adjusted_event_rates[min_event]
    print(f"Pushing event: {min_event} (minimum adjusted event rate {min_event_rate})")

    total_transmissions_no_optimization = 0
    total_transmissions_with_push_pull = 0

    for instance_name, event_rate in rates_per_node.items():
        path = paths[instance_name]
        num_hops = len(path) - 1  # Number of hops
        transmissions_no_optimization = event_rate * num_hops
        total_transmissions_no_optimization += transmissions_no_optimization

        prim_event = instance_name[0]  # Extract the event type
        push_event_types = []
        if isinstance(min_event, str):
            push_event_types = [min_event]
        elif isinstance(min_event, tuple):
            operator, events = min_event
            push_event_types = list(events)
        else:
            push_event_types = []

        if prim_event in push_event_types:
            # This is the pushed event
            transmissions_with_push_pull = event_rate * num_hops
        else:
            # Pulled event, adjusted by selectivity
            # Construct the selectivity key to match the single_select dictionary
            selectivity_key = f"{prim_event}|{''.join(push_event_types + [prim_event])}"
            selectivity = single_select.get(selectivity_key, 1.0)
            adjusted_event_rate = event_rate * selectivity
            transmissions_with_push_pull = adjusted_event_rate * num_hops

        total_transmissions_with_push_pull += transmissions_with_push_pull
        print(f"Instance {instance_name} (path {path}) has {transmissions_with_push_pull} transmissions with push-pull.")

    # Print transmission summary
    print(f"Total transmissions without optimization: {total_transmissions_no_optimization}")
    print(f"Total transmissions with push-pull: {total_transmissions_with_push_pull}")
    saved_transmissions = total_transmissions_no_optimization - total_transmissions_with_push_pull
    print(f"Saved transmissions using push-pull: {saved_transmissions}")

def extract_primitive_events(projection_events):
    """
    Extract all primitive events from the projection, ignoring operators like AND, SEQ.

    Parameters:
    - projection_events (list): List of events or nested operators (e.g., ['M', 'K', 'AND(P, R, S)']).

    Returns:
    - flat_events (list): A flat list of primitive events (e.g., ['M', 'K', 'P', 'R', 'S']).
    """
    flat_events = []
    for event in projection_events:
        if "AND(" in event or "SEQ(" in event:
            # Extract inner events from AND/SEQ (e.g., 'AND(P, R, S)' -> ['P', 'R', 'S'])
            inner_events = event.replace("AND(", "").replace("SEQ(", "").replace(")", "").split(", ")
            flat_events.extend(inner_events)
        else:
            # If it's a simple event, add it directly
            flat_events.append(event)
    return flat_events

def extract_events_with_operators(projection_events):
    """
    Extract events and operators from the projection.
    Returns a structured representation.

    Parameters:
    - projection_events (list): List of events or nested operators (e.g., ['M', 'K', 'AND(P, R, S)']).

    Returns:
    - structured_events (list): A list where primitive events are strings and composite events are dictionaries.
    """
    structured_events = []
    for event in projection_events:
        if "AND(" in event or "SEQ(" in event:
            operator = 'AND' if 'AND(' in event else 'SEQ'
            inner_events = event.replace(f"{operator}(", "").replace(")", "").split(", ")
            structured_events.append({
                'operator': operator,
                'events': inner_events
            })
        else:
            structured_events.append(event)
    return structured_events

def main():
    """
    Main function to calculate the potential of push-pull communication dynamically.
    """
    print("Python version:", sys.version)

    # Load necessary files
    eval_plan = load_pickle('EvaluationPlan')
    nodes_dict = {node.id: node for node in load_pickle('network')}
    selectivities = load_pickle('selectivities')
    single_select = load_pickle('singleSelectivities')

    print(nodes_dict)
    # Iterate over the EvaluationPlan object
    for item in eval_plan:
        if isinstance(item, EvaluationPlan):
            for proj in item.projections:
                # Extract projection name and events
                evaluation = proj
                projection_name = evaluation.name.name
                projection_events = [str(x) for x in projection_name.children]
                print(f"Processing projection: {projection_events}")

                # Parse the events, including operators
                projection_structure = extract_events_with_operators(projection_events)
                print(f"Structured events: {projection_structure}")

                # Collect source nodes and paths for the projection
                source_node_names = []
                paths = {}
                gen_nodes = evaluation.name.combination
                for x in gen_nodes:
                    for instance in gen_nodes[x]:
                        # Check if the instance corresponds to a primitive event
                        if len(instance.name) > 1 and instance.name[1:].isdigit():
                            source_node_names.append(instance.name)
                            for _, path in instance.routingDict.items():
                                paths[instance.name] = path
                        else:
                            print(f"Skipping composite event instance: {instance.name}")
                print(source_node_names)
                # Calculate event rates for the projection
                event_rates, rates_per_node = calculate_event_rates(source_node_names, nodes_dict)
                print(f"Event rates: {event_rates}")

                # Apply push-pull strategy on the structured events
                calculate_dynamic_push_pull_transmissions(
                    event_rates, rates_per_node, paths, single_select, selectivities, projection_structure, projection_events
                )

if __name__ == "__main__":
    main()
