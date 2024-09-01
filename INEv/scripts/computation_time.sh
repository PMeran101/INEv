#!/bin/sh
cd ../code
echo "Computation Time"
for j in 4 5 6 7 8
do
		a=0
		while [ $a -lt 60 ]
		do		
		echo "Executing Time: $(date) Var: j=$j , a=$a"
		python3 generate_network.py 100 0.5 1.4 $j
		python3 generate_qwls.py $j 1
		python3 generate_selectivity.py 		
		python3 generate_graph.py
		python3 allPairs.py
		python3 write_config_single.py
		python3 determine_all_single_selectivities.py
		python3 generate_projections.py
		python3 combigen.py
		python3 computePlanCosts_aug.py computationTime
		a=`expr $a + 1`
		done
done
