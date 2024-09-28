#!/bin/sh
cd ../code
echo "Computation Time"
for j in 4 5 6 7 8
do
<<<<<<< HEAD
    log_file="./logs/compute-time+${j}.log"
    echo "Logging to $log_file"
    echo "Execution Time: $(date)" >> $log_file
=======
      for b in 2 3 4 5 6 7
      do
>>>>>>> fog_cloud_topology
		a=0
		while [ $a -lt 60 ]
		do		
		echo "Executing Time: $(date) Var: j=$j , a=$a"
<<<<<<< HEAD
		python3 generate_network.py 20 0.5 1.4 $j
=======
		python3 generate_network.py -nw 50 -ner 0.5 -es 1.4 -ne $j -mp $b
>>>>>>> fog_cloud_topology
		python3 generate_qwls.py $j 1
		python3 generate_selectivity.py 		
		python3 generate_graph.py
		python3 allPairs.py
		python3 write_config_single.py
		python3 determine_all_single_selectivities.py
		python3 generate_projections.py
		python3 combigen.py
<<<<<<< HEAD
		python3 computePlanCosts_aug.py computationTime
=======
		python3 computePlanCosts_aug.py computationTime $b
>>>>>>> fog_cloud_topology
		a=`expr $a + 1`
		done
		done
done
