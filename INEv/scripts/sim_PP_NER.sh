
cd ../code

for k in 1 2 3 4 5 6 7 8
do 
for b in  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
do
          a=1
          while [ "$a" -lt 200 ]
          do
                        python3 generate_network.py -nw 50 -ner $b -es 1.3 -ne 10 -mp $k
          python3 generate_graph.py
          python3 allPairs.py
     
              python3 generate_qwls.py --length 6 --count 10	
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py --file "PP_NER_Combined" --number_parents $k
            python3 generateEvalPlan.py
            python3 prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file "PP_NER_Combined"
                
              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
    
        done

          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done