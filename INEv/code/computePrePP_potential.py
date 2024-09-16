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


# Function to calculate total transmissions with push-pull strategy dynamically
def calculate_dynamic_push_pull_transmissions(rates_ev, rates_per_node, paths, single_select, projection_events):
    """
    Calculate total transmissions with and without optimization for any set of events dynamically.
    
    Parameters:
    - rates_ev: Dictionary of event rates for each event type (e.g., 'G', 'H', 'P').
    - rates_per_node: Event rate per node.
    - paths: Routing paths for each event instance.
    - single_select: Single selectivities for event pairs (e.g., 'H|GH', 'P|GHP').
    - projection_events: List of events in the projection.
    """

    # Find the event with the minimum event rate (this will be the event we "push")
    min_prim_event = min(rates_ev, key=rates_ev.get)
    print(f"Pushing event: {min_prim_event} (minimum rate event)")

    total_transmissions_no_optimization = 0
    total_transmissions_with_push_pull = 0

    # Iterate over each event instance (e.g., G2, H3, etc.)
    for instance, event_rate in rates_per_node.items():
        path = paths[instance]
        
        # Transmissions without push-pull: Every event is transmitted along its path
        transmissions_no_optimization = calculate_transmissions(event_rate, path)
        total_transmissions_no_optimization += transmissions_no_optimization

        # Push-pull strategy: Push the minimum event, pull others based on selectivity
        prim_event = instance[0]  # Extract the event type (e.g., 'G' in 'G2')

        # If the instance corresponds to the event we're pushing
        if prim_event == min_prim_event:
            transmissions_with_push_pull = calculate_transmissions(event_rate, path)
        else:
            # Adjust the event rate based on the selectivity
            for i in range(1, len(projection_events)):
                if prim_event == projection_events[i]:
                    # Construct the selectivity key (e.g., 'H|GH', 'P|GHP')
                    selectivity_key = f"{prim_event}|{''.join(projection_events[:i+1])}"
                    adjusted_event_rate = event_rate * single_select.get(selectivity_key, 1.0)
                    transmissions_with_push_pull = calculate_transmissions(adjusted_event_rate, path)
                    break

        total_transmissions_with_push_pull += transmissions_with_push_pull
        print(f"Instance {instance} (path {path}) has {transmissions_with_push_pull} transmissions with push-pull.")

    # Print transmission summary
    print(f"Total transmissions without optimization: {total_transmissions_no_optimization}")
    print(f"Total transmissions with push-pull: {total_transmissions_with_push_pull}")
    saved_transmissions = total_transmissions_no_optimization - total_transmissions_with_push_pull
    print(f"Saved transmissions using push-pull: {saved_transmissions}")


def main():
    """Main function to calculate the potential of push-pull communication dynamically."""
    print("Python version:", sys.version)

    # Load necessary files
    eval_plan = load_pickle('EvaluationPlan')
    nodes_dict = {node.id: node for node in load_pickle('network')}
    selectivities = load_pickle('selectivities')
    single_select = load_pickle('singleSelectivities')

    # Iterate over the EvaluationPlan object
    for i in eval_plan:
        if isinstance(i, EvaluationPlan):
            for proj in i.projections:
                # Extract projection name and events
                myEval = proj
                myProj = myEval.name.name
                projection_events = [str(x) for x in myProj.children]
                print(f"Processing projection: {projection_events}")

                # Collect source nodes and paths for the projection
                source_nodes = []
                paths = {}
                gen_nodes = myEval.name.combination
                for x in gen_nodes:
                    for instance in gen_nodes[x]:
                        source_nodes.append(instance.name)
                        for _, path in instance.routingDict.items():
                            paths[instance.name] = path

                # Calculate event rates for the projection
                rates_ev, rates_per_node = calculate_event_rates(source_nodes, nodes_dict)
                print(f"Event rates: {rates_ev}")

                # Calculate total transmissions with push-pull optimization for dynamic events
                calculate_dynamic_push_pull_transmissions(rates_ev, rates_per_node, paths, single_select, projection_events)

if __name__ == "__main__":
    main()