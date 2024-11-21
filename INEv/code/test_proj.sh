
# for max_p in 1 2 3 4
# do
#     a=0
#     while [ $a -lt 3 ]
#     do
        python3 generate_network.py -nw 50 -ner 0.5 -es 1 -ne 15 -mp 12 #$max_p
        python3 generate_graph.py
        echo "Finisehd graph"
        python3 allPairs.py
        echo "Finished all pairs"
        python3 generate_qwls.py --length 12 --count 2
    #     echo "Finished qwls"
    #     python3 generate_selectivity.py 
    #     echo "Finished selectivity"
    #     python3 write_config_single.py
    #     echo "Finished config"
    #     python3 determine_all_single_selectivities.py
    #     echo "Finished selectivities"
    #     python3 generate_projections.py
    #     echo "Finished projections"
    #     python3 combigen.py
    #     echo "Finished combigen"
    #     python3 computePlanCosts_aug.py --file test --number_parents 12
    #     echo "Finished plan costs"
    #    # python3 generateEvaluationPlan.py
    #     python3 generateEvalPlan.py
    #     python prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file test
    # #     a=`expr $a + 1`
    # done
#done