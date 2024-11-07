
#!/bin/sh

cd ../code
for nw in 1000 5000 10000 100000 500000
do 

      for h in 6 10 15
      do

    # Calculate b as percentages of nw
        for perc in 3 4 5 6 7 8 9 10 15 20 25 30
        do
              b=$(( nw * perc / 100 )) 

          a=1
          while [ "$a" -lt 100 ]
          do
             # echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              python3 generate_network.py -nw $nw -ner 0.5 -es 1.3 -ne "$h" -mp $b
              python3 generate_graph.py
              python3 allPairs.py
              python3 generate_qwls.py --length 6 --count 5
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py --file "Experiment_Scaling" --number_parents $b
              python3 generateEvalPlan.py
              python3 prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file "Experiment_Scaling"
             
              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
        
        #   done 
          #cho "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done
  done
  done
  
  #echo "Script completed at: $(date)"
  

