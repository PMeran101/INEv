
#!/bin/sh

cd ../code
	
##
"""
Experiment to test the effect of changing Graph Density on the performance of the system
We vary:
1. Number of Queries 
2. Number of Event Types
3. Number of Max Parents
"""
##
  echo "Script started at: $(date)"

  for k in 5 10 20 # qwl amount
  do 
      for h in 6 10 15 20 25 # num event types
      do
      for b in 2 3 4 5 6 7
      do
      
          echo "Starting outer loop with k=$k and h=$h at: $(date)"

          python3 generate_network.py -nw 50 -ner 0.5 -es 1.3 -ne "$h" -mp $b
          python3 generate_graph.py
          python3 allPairs.py
     
          a=1
          while [ "$a" -lt 3 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py --length 6 --count $k	
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py --file "OP_MaxParents_$b" --number_parents $b

              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
        
        #   done
      done    
          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done
  done
  
  echo "Script completed at: $(date)"
  

