cd ../code
	
  echo "Script started at: $(date)"


python3 generate_network.py -nw 20 -ner 0.5 -es 1.3 -ne 20
python3 generate_graph.py
python3 allPairs.py


python3 generate_qwls.py 6 2
python3 generate_selectivity.py 
python3 write_config_single.py
python3 determine_all_single_selectivities.py
python3 generate_projections.py
python3 combigen.py
python3 computePlanCosts_aug.py "PrePP_QWL2"
        
