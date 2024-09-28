#!/bin/sh
cd ../code
echo "EventNode_QWL"

<<<<<<< HEAD
python3 generate_network.py 20 0.5 1.3 25
=======
python3 generate_network.py -nw 50 -ner 0.5 -es 1.3 -ne 25 -mp 2
>>>>>>> fog_cloud_topology
python3 generate_graph.py
python3 allPairs.py
#5
for k in 10 20  
do 
<<<<<<< HEAD
    log_file="./logs/eventNode_qwl_k${k}.log"
    echo "Logging to $log_file"
    echo "Execution Time: $(date)" >> $log_file

=======
>>>>>>> fog_cloud_topology
	python3 generate_qwls.py 6 $k
	python3 generate_selectivity.py 
	for j in  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
	do
	for b in 2 3 4 5 6 7
      do
			a=0
			while [ $a -lt 75 ]
			do
			echo "Executing Time: $(date) Var: k=$k, j=$j , a=$a"
<<<<<<< HEAD
			python3 generate_network.py 20 $j 1.3 25
=======
			python3 generate_network.py -nw 50 -ner $j -es 1.3 -ne 25 -mp $b
>>>>>>> fog_cloud_topology
			python3 generate_graph.py
			python3 allPairs.py
			python3 write_config_single.py
			python3 determine_all_single_selectivities.py
			python3 generate_projections.py
			python3 combigen.py
<<<<<<< HEAD
			python3 computePlanCosts_aug.py eventNode_qwl+"$k"
=======
			python3 computePlanCosts_aug.py eventNode_qwl+"$k" $b
>>>>>>> fog_cloud_topology
			a=`expr $a + 1`
			done
	done
	done
done
