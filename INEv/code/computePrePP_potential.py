
import pickle
import os
import sys
from EvaluationPlan import EvaluationPlan, Projection, Instance
from tree import Tree

print(sys.version)


with open('EvaluationPlan', 'rb') as f:
    eval_plan = pickle.load(f)
    
source_nodes = [] 

paths = {}
# Iterate over the EvaluationPlan object
for i in eval_plan:
    if isinstance(i, EvaluationPlan):
    #     print("Projections")
    #     print(i.projections[0].name)
        for proj in i.projections:
        
            myEval = proj

            myname = myEval.name.name
            myProj = myname
            myEvents = [str(x) for x in myProj.children]
            print(myEvents)
            # print(type(myname.name))
            mysinks = str(myEval.name.sinks)
            sink_node = mysinks

            gen_nodes= myEval.name.combination
            for x in gen_nodes:
                for i in gen_nodes[x]:
                    # print(i)
                    source_nodes.append(i.name)
                    for key, path in i.routingDict.items():
                        paths[i.name] = path
            #        print(gen_nodes)
            print(f"name {myname}, sinks: {mysinks}")
            

            print(source_nodes)

            with open('network','rb') as f:
                nw = pickle.load(f)

            # print(nw)
            nodes_dict = {node.id: node for node in nw}
            # print(nodes_dict)


            with open('selectivities','rb') as f:
                selectivities = pickle.load(f)

            with open('singleSelectivities','rb') as f:
                singleSelect = pickle.load(f)
            #print(singleSelect)

            import string
            rates_ev = {}
            rates_per_node = {}
            for a in source_nodes:
                primEvent = a[0]
                nodeid = int(a[1])
                
                node = nodes_dict[nodeid]
                entry = string.ascii_uppercase.index(primEvent.upper())
                # print(entry)
                eventrate = node.eventrates[entry]
                # print(eventrate)
                if primEvent not in rates_ev:
                    rates_ev[primEvent] = 0  # Initialize with 0
                if a not in rates_per_node:
                    rates_per_node[a] = eventrate
                
                
                # Add the eventrate to the corresponding key in the dictionary
                rates_ev[primEvent] += eventrate

            #Hiervon Max nehmen und dass ist dann mein H H|GH 
            # bzw. das min wird gepulled alle anderen gepush
            print(rates_ev)
                


            with open('selectivities','rb') as f:
                selectivities = pickle.load(f)

            with open('singleSelectivities','rb') as f:
                singleSelect = pickle.load(f)

            total_transmissions_no_optimization = rates_ev['G'] + rates_ev['H'] + rates_ev['P']
            print(f"Total transmissions without optimization: {total_transmissions_no_optimization}")


            # Step 2: Calculate the number of H events after G
            expected_H_after_G = rates_ev['H'] * singleSelect['H|GH']

            # Step 3: Calculate the number of P events after G and H
            expected_P_after_GH = rates_ev['P'] * singleSelect['P|GHP']

            # Total transmissions with push-pull
            transmissions_with_push_pull = rates_ev['G'] + expected_H_after_G + expected_P_after_GH

            print(f"Total transmissions with push-pull: {transmissions_with_push_pull}")




            # Function to calculate total transmissions for an event instance
            def calculate_transmissions(event_instance, event_rate, path):
                num_hops = len(path) - 1  # Number of hops (nodes the event passes through)
                total_transmissions = event_rate * num_hops  # Total transmissions = event rate * hops
                return total_transmissions

            # Calculate total transmissions with and without push-pull strategy
            total_transmissions_no_optimization = 0
            total_transmissions_with_push_pull = 0

            for instance, event_rate in rates_per_node.items():
                path = paths[instance]
                
                # Transmissions without push-pull: Every event is transmitted along its path
                transmissions_no_optimization = calculate_transmissions(instance, event_rate, path)
                total_transmissions_no_optimization += transmissions_no_optimization
                
                # Push-pull strategy: Push G and pull the remaining events
                if 'G' in instance:  # Push G
                    transmissions_with_push_pull = calculate_transmissions(instance, event_rate, path)
                else:  # Pull H and P based on selectivity
                    if 'H' in instance:  # Pull H
                        adjusted_event_rate = event_rate * singleSelect.get('H|GH', 1.0)  # Adjust for selectivity
                    elif 'P' in instance:  # Pull P
                        adjusted_event_rate = event_rate * singleSelect.get('P|GHP', 1.0)  # Adjust for selectivity
                    transmissions_with_push_pull = calculate_transmissions(instance, adjusted_event_rate, path)
                
                total_transmissions_with_push_pull += transmissions_with_push_pull
                print(f"Instance {instance} (path {path}) has {transmissions_with_push_pull} transmissions with push-pull.")

            # Calculate total transmission savings
            saved_transmissions = total_transmissions_no_optimization - total_transmissions_with_push_pull

            # Print results
            print(f"Total transmissions without optimization: {total_transmissions_no_optimization}")
            print(f"Total transmissions with push-pull: {total_transmissions_with_push_pull}")
            print(f"Saved transmissions using push-pull: {saved_transmissions}")