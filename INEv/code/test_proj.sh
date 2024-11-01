
# for max_p in 1 2 3 4
# do
#     a=0
#     while [ $a -lt 3 ]
#     do
        python3 generate_network.py -nw 15 -ner 0.5 -es 1 -ne 15 -mp 2 #$max_p
        python3 generate_graph.py
        echo "Finisehd graph"
        python3 allPairs.py
        python3 generate_qwls.py --length 6 --count 2	
        python3 generate_selectivity.py 
        python3 write_config_single.py
        python3 determine_all_single_selectivities.py
        python3 generate_projections.py
        python3 combigen.py
        python3 computePlanCosts_aug.py --file test --number_parents 1 
       # python3 generateEvaluationPlan.py
        python3 generateEvalPlan.py
        python prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file test
    #     a=`expr $a + 1`
    # done
#done