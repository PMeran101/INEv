#!/bin/sh
cd ../code

echo "Negated"

for j in  1.1  1.3  1.5  1.7  1.9 
do
<<<<<<< HEAD
    log_file="./logs/negated_un+${j}.log"
    echo "Logging to $log_file"
    echo "Execution Time: $(date)" >> $log_file
		a=0
		while [ $a -lt 50 ]
		do
		python3 generate_network.py 20 0.5 $j # generate rates
=======
      for b in 2 3 4 5 6 7
      do
		a=0
		while [ $a -lt 50 ]
		do
		python3 generate_network.py -nw 50 -ner 0.5 -es $j # generate rates
>>>>>>> fog_cloud_topology
                # start with min
		# q nseq
		# q seq
		# generate with max 
		# q nseq
		for param in 'max' 'min'
                        do
<<<<<<< HEAD
			python3 generate_network.py 20 0.5 $j 10 10 'A' $param
=======
			python3 generate_network.py -nw 50 -ner 0.5 -es $j -ne 10 -sw 10 -et 'A' -p $param -mp $b
>>>>>>> fog_cloud_topology
			python3 generate_qwls.py 10 5 0
			python3 write_config_single.py
		        python3 determine_all_single_selectivities.py
			for neg in 0 1
				do
				echo "Executing Time: $(date) Var: j=$j , a=$a, param=$param, neg=$neg"
				python3 generate_qwls.py 10 5 $neg
				python3 generate_projections.py
				python3 combigen.py
<<<<<<< HEAD
				python3 computePlanCosts_aug.py KL+$param+$neg #unconstrainedFilter
=======
				python3 computePlanCosts_aug.py KL+$param+$neg $b
>>>>>>> fog_cloud_topology
				done
			python3 generate_qwls.py 10 5 2 #NSEQ QUERY
			python3 generate_projections.py
			python3 combigen.py
<<<<<<< HEAD
			python3 computePlanCosts_aug.py  NSEQ+$param+$neg #unconstrainedFilter
=======
			python3 computePlanCosts_aug.py  NSEQ+$param+$neg $b
>>>>>>> fog_cloud_topology

		done
		a=`expr $a + 1`
		done
		done
done
