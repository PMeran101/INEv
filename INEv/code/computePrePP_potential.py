import pickle
import os
import sys
from EvaluationPlan import EvaluationPlan, Projection, Instance
from tree import Tree
import string

# Helper function to load a pickle file
def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

# Function to calculate event rates for each projection
def calculate_event_rates(source_nodes, nodes_dict):
    """
    Calculate event rates for each primitive event.
    - rates_ev: Summed rates for each event type.
    - rates_per_node: Individual event rate for each node instance.
    """
    rates_ev = {}
    rates_per_node = {}

    for a in source_nodes:
        prim_event = a[0]  # Get the event type (e.g., 'H', 'P', 'G')
        
        # Ensure that the node name is in the correct format (e.g., 'H2', 'P3')
        if len(a) > 1 and a[1].isdigit():
            nodeid = int(a[1])  # Extract the node ID (e.g., '2', '3')
            node = nodes_dict[nodeid]

            entry = string.ascii_uppercase.index(prim_event.upper())  # Get the index of the event
            eventrate = node.eventrates[entry]

            # Initialize the event rate in rates_ev if it doesn't exist
            if prim_event not in rates_ev:
                rates_ev[prim_event] = 0
            if a not in rates_per_node:
                rates_per_node[a] = eventrate

            # Add the eventrate to the corresponding key in the dictionary
            rates_ev[prim_event] += eventrate
        else:
            print(f"Skipping invalid node name format: {a}")

    return rates_ev, rates_per_node


# Function to calculate total transmissions for an event instance
def calculate_transmissions(event_rate, path):
    num_hops = len(path) - 1  # Number of hops (nodes the event passes through)
    total_transmissions = event_rate * num_hops  # Total transmissions = event rate * hops
    return total_transmissions

def calculate_selectivity(event_structure, single_select, selectivities):
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


def calculate_dynamic_push_pull_transmissions(rates_ev, rates_per_node, paths, single_select, selectivities, projection_structure, projection_events):
    """
    Calculate total transmissions with and without optimization for any set of events dynamically,
    considering operators like AND and SEQ.

    Parameters:
    - rates_ev: Dictionary of event rates for each event type (e.g., 'G', 'H', 'P').
    - rates_per_node: Event rate per node.
    - paths: Routing paths for each event instance.
    - single_select: Single selectivities for events (e.g., 'H|GH').
    - selectivities: Selectivities for composite events (e.g., 'GH', 'HP').
    - projection_structure: Structured representation of the projection, including operators.
    - projection_events: List of events in the projection (e.g., ['G', 'H', 'P']).
    """

    # Calculate adjusted event rates for each event or composite event
    adjusted_event_rates = {}
    for event_structure in projection_structure:
        selectivity = calculate_selectivity(event_structure, single_select, selectivities)
        if isinstance(event_structure, dict):
            operator = event_structure['operator']
            events = event_structure['events']
            # For composite events, determine how to combine event rates
            event_rates = [rates_ev.get(e, 0) for e in events]
            combined_event_rate = min(event_rates) * selectivity
            key = (operator, tuple(events))
        else:
            # Primitive event
            event_rate = rates_ev.get(event_structure, 0)
            combined_event_rate = event_rate * selectivity
            key = event_structure
        adjusted_event_rates[key] = combined_event_rate

    # Find the event (or composite event) with the minimum adjusted event rate
    min_event = min(adjusted_event_rates, key=adjusted_event_rates.get)
    min_event_rate = adjusted_event_rates[min_event]
    print(f"Pushing event: {min_event} (minimum adjusted event rate {min_event_rate})")

    total_transmissions_no_optimization = 0
    total_transmissions_with_push_pull = 0

    # Now, iterate over each event instance
    for instance, event_rate in rates_per_node.items():
        path = paths[instance]
        num_hops = len(path) - 1  # Number of hops
        transmissions_no_optimization = event_rate * num_hops
        total_transmissions_no_optimization += transmissions_no_optimization

        # Determine if this instance corresponds to the pushed event
        prim_event = instance[0]  # Extract the event type from the instance name (e.g., 'G' from 'G2')
        push_event_types = []
        if isinstance(min_event, str):
            push_event_types = [min_event]
        elif isinstance(min_event, tuple):
            operator, events = min_event
            push_event_types = list(events)
        else:
            # Should not reach here
            push_event_types = []

            # Inside calculate_dynamic_push_pull_transmissions
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
        print(f"Instance {instance} (path {path}) has {transmissions_with_push_pull} transmissions with push-pull.")

    # Print transmission summary
    print(f"Total transmissions without optimization: {total_transmissions_no_optimization}")
    print(f"Total transmissions with push-pull: {total_transmissions_with_push_pull}")
    saved_transmissions = total_transmissions_no_optimization - total_transmissions_with_push_pull
    print(f"Saved transmissions using push-pull: {saved_transmissions}")



def extract_primitive_events(projection_events):
    """
    Extract all primitive events from the projection, ignoring operators like AND, SEQ.
    
    Parameters:
    - projection_events: List of events or nested operators (e.g., ['M', 'K', 'AND(P, R, S)'])
    
    Returns:
    - flat_events: A flat list of primitive events (e.g., ['M', 'K', 'P', 'R', 'S'])
    """
    flat_events = []
    
    for event in projection_events:
        if "AND" in event or "SEQ" in event:
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
    """Main function to calculate the potential of push-pull communication dynamically."""
    print("Python version:", sys.version)

    # Load necessary files
    eval_plan = load_pickle('EvaluationPlan')
    nodes_dict = {node.id: node for node in load_pickle('network')}
    selectivities = load_pickle('selectivities')
    single_select = load_pickle('singleSelectivities')

    print(nodes_dict)
    # Iterate over the EvaluationPlan object
    for i in eval_plan:
        if isinstance(i, EvaluationPlan):
            for proj in i.projections:
                # Extract projection name and events
                myEval = proj
                myProj = myEval.name.name
                projection_events = [str(x) for x in myProj.children]
                print(f"Processing projection: {projection_events}")

                # Parse the events, including operators
                projection_structure = extract_events_with_operators(projection_events)
                print(f"Structured events: {projection_structure}")

                # Collect source nodes and paths for the projection
                source_nodes = []
                paths = {}
                gen_nodes = myEval.name.combination
                for x in gen_nodes:
                    for instance in gen_nodes[x]:
                        # Check if the instance corresponds to a primitive event
                        if len(instance.name) > 1 and instance.name[1:].isdigit():
                            source_nodes.append(instance.name)
                            for _, path in instance.routingDict.items():
                                paths[instance.name] = path
                        else:
                            print(f"Skipping composite event instance: {instance.name}")
                print(source_nodes)
                # Calculate event rates for the projection
                rates_ev, rates_per_node = calculate_event_rates(source_nodes, nodes_dict)
                print(f"Event rates: {rates_ev}")

                # Apply push-pull strategy on the structured events
                calculate_dynamic_push_pull_transmissions(
                    rates_ev, rates_per_node, paths, single_select, selectivities, projection_structure, projection_events
                )

if __name__ == "__main__":
    main()
