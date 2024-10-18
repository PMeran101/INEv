#!/bin/sh

cd ../code
	
  echo "Script started at: $(date)"


for k in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2
do

      
          echo "Starting outer loop with k=$k and h=$h at: $(date)"


     
          a=1
          while [ "$a" -lt 150 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
            python3 generate_network.py -nw 50 -ner 0.5 -es $k -ne 10 -mp 4
            python3 generate_graph.py
            python3 allPairs.py 
            python3 generate_qwls.py 6 10
            python3 generate_selectivity.py 
            python3 write_config_single.py
            python3 determine_all_single_selectivities.py
            python3 generate_projections.py
            python3 combigen.py
            python3 computePlanCosts_aug.py "PP_EventSkew_$k" 4
            python3 generateEvaluationPlan.py
            python3 generateEvalPlan.py
            python prepp.py --input_file plans/curr_MS --method ppmuse --algorithm e --samples 0  --topk 0  --runs 1 --plan_print f --output_file "PP_EventSkew_$k"
            
            echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
              sleep 1
        #   done
      done    
          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
#       done
#   done
  
  echo "Script completed at: $(date)"
  

