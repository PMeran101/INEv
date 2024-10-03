python3 generate_network.py -nw 15 -ner 0.5 -es 1.3 -ne 15 -mp 2
python3 generate_graph.py
python3 allPairs.py
python3 generate_qwls.py 6 10	
python3 generate_selectivity.py 
python3 write_config_single.py
python3 determine_all_single_selectivities.py
python3 generate_projections.py
python3 combigen.py
python3 computePlanCosts_aug.py
python3 generateEvalPlan.py
python prepp.py plans/curr_MS ppmuse s 0 0 5 f