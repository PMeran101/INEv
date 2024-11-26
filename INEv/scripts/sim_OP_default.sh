
cd ../code

for e in 5 6 7 8
do
for k in 5 10 15 20 25
do 

          a=1
          while [ "$a" -lt 100 ]
          do

            python3 generate_network.py -nw 50 -ner 0.5 -es 1.3 -ne $k -mp $e
            python3 generate_graph.py
            python3 allPairs.py
            python3 generate_qwls.py --length 6 --count 10	
            python3 generate_selectivity.py 
            python3 write_config_single.py
            python3 determine_all_single_selectivities.py
            python3 generate_projections.py
            python3 combigen.py
            python3 computePlanCosts_aug.py --file "combined_for_latency" --number_parents $e
            python3 generateEvalPlan.py
            python3 prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file "combined_for_latency"
              a=$((a + 1))
    done
        done

          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done