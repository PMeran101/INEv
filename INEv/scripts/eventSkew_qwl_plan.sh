#!/bin/sh
cd ../code

echo "Event_SKew_QWL PLAN"

python3 generate_network.py 100 0.5 1.3 25
python3 generate_graph.py
python3 allPairs.py

for k in 5 10 20  
do 

	python3 generate_qwls.py 6 $k
	python3 generate_selectivity.py 
	for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 
	do
			a=0
			while [ $a -lt 40 ]
			do
			python3 generate_network.py 100 0.5 $j 25 
			python3 generate_graph.py
			python3 allPairs.py
			python3 write_config_single.py
			python3 determine_all_single_selectivities.py
			python3 generate_projections.py
			python3 combigen.py
			python3 computePlanCosts_aug.py eventSkew_qwl+$k
			python3 generateEvaluationPlan.py
			a=`expr $a + 1`
			done
	done
done



