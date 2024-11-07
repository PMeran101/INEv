cd ../code

for nw in 1000 5000 10000 100000 500000
do 
    nwsize=$nw
    # Calculate b as percentages of nw
    for perc in 2.5	1.67 1.25 1 0.83 0.71 0.63 0.55	0.5	0.45 0.41 0.38 0.35 0.33 0.3 0.2
    do
        
        # Calculate levels using bc
        levels=$(echo "scale=5; l($nwsize)/l(2)" | bc -l)
        
        # Calculate b as levels * perc / 100
        b=$(echo "$levels / $perc" | bc -l)
        max_parents=$(echo "$b/1" | bc)
        
    for h in 6 10 15
    do
    a=1
          while [ "$a" -lt 100 ]
          do
        python3 generate_network.py -nw $nw -ner 0.5 -es 1.3 -ne $h -mp $max_parents
        python3 generate_graph.py
        python3 allPairs.py
        python3 generate_qwls.py --length 6 --count 5
        python3 generate_selectivity.py 
        python3 write_config_single.py
        python3 determine_all_single_selectivities.py
        python3 generate_projections.py
        python3 combigen.py
        python3 computePlanCosts_aug.py --file "Experiment_Scaling" --number_parents $max_parents
        python3 generateEvalPlan.py
        python3 prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file "Experiment_Scaling"
        done
        done
    done
done
