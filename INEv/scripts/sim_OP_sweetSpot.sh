
#!/bin/sh

cd ../code
	
##
"""
Experiment to try and find the sweet Spot of Maximum Parents.
We vary:
1. Maximum Parents allowed
2. Query Size
"""
##
  echo "Script started at: $(date)"
for b in  2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
  for k in 5 10 20 # qwl amount
  do 


      
          echo "Starting outer loop with k=$k and h=$h at: $(date)"

          python3 generate_network.py -nw 50 -ner 0.5 -es 1.3 -ne 10 -mp $b
          python3 generate_graph.py
          python3 allPairs.py
     
          a=1
          while [ "$a" -lt 150 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py 6 $k	
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py "OP_SweetSpot_MaxParents_$b" $b

              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
    
        #   done

          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done
  done
  
  echo "Script completed at: $(date)"
  

