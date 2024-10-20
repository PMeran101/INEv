#!/bin/sh
cd ../code

echo "Lower Bound"

for z in 1 2 3 4
do
      for b in 2 3 4 5 6 7
      do
python3 generate_network.py -nw 50 -ner 0.5 -es 1.1 -ne 7 -mp $b
python3 generate_qwls.py 7 1
python3 generate_graph.py
python3 allPairs.py

for s in 0.01 0.001
do
python3 generate_selectivity.py $s
for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 
do
		a=0
		while [ $a -lt 50 ]
		do
		echo "Executing Time: $(date) Var: s=$s, j=$j , a=$a"
		# python3 generate_network.py -nw 50 -ner 0.5 -es $j -ne 7
		python3 write_config_single.py
		python3 determine_all_single_selectivities.py
		python3 generate_projections.py
		python3 combigen.py
		python3 computePlanCosts_aug.py lower+"$s"
		a=`expr $a + 1`
		done
done
done
done
done