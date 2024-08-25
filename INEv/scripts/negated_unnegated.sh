#!/bin/sh
cd ../code

echo "Negated"

for j in  1.1  1.3  1.5  1.7  1.9 
do
		a=0
		while [ $a -lt 50 ]
		do
		python3 generate_network.py 20 0.5 $j # generate rates
                # start with min
		# q nseq
		# q seq
		# generate with max 
		# q nseq
		for param in 'max' 'min'
                        do
			python3 generate_network.py 20 0.5 $j 10 10 'A' $param
			python3 generate_qwls.py 10 5 0
			python3 write_config_single.py
		        python3 determine_all_single_selectivities.py
			for neg in 0 1
				do
				python3 generate_qwls.py 10 5 $neg
				python3 generate_projections.py
				python3 combigen.py
				python3 computePlanCosts_aug.py KL+$param+$neg #unconstrainedFilter
				done
			python3 generate_qwls.py 10 5 2 #NSEQ QUERY
			python3 generate_projections.py
			python3 combigen.py
			python3 computePlanCosts_aug.py  NSEQ+$param+$neg #unconstrainedFilter

		done
		a=`expr $a + 1`
		done
done
