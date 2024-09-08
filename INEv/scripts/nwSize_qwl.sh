#!/bin/sh
cd ../code

echo "nwSize_SQL"

python3 generate_network.py -nw 20 -ner 0.5 -es 1.3 -ne 25
python3 generate_graph.py
python3 allPairs.py

for k in 10 20  
do 

	python3 generate_qwls.py 6 $k
	python3 generate_selectivity.py 
	for j in 20 50 100 150 200 
	do
			a=0
			while [ $a -lt 60 ]
			do
			python3 generate_network.py -nw $j -ner 0.5 -es 1.3 -ne 25
			python3 generate_graph.py
			python3 allPairs.py
			python3 write_config_single.py
			python3 determine_all_single_selectivities.py
			python3 generate_projections.py
			python3 combigen.py
			python3 computePlanCosts_aug.py nwSize_qwl+$k
			a=`expr $a + 1`
			done
			echo "finished k=$K , j=$j , a=$a"
	done
	echo "finished k=$K , j=$j , a=$a"
done

