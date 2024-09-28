#!/bin/sh

cd ../code
	
  echo "Script started at: $(date)"

  for k in 5 10 20 # qwl size
  do 
      for h in 6 10 15 20 25 # num event types
      do
<<<<<<< HEAD
          echo "Starting outer loop with k=$k and h=$h at: $(date)"

          Generate network and graph files
          python3 generate_network.py 20 0.5 1.3 "$h"
=======
      for b in 2 3 4 5 6 7
      do
      
          echo "Starting outer loop with k=$k and h=$h at: $(date)"

          Generate network and graph files
          python3 generate_network.py -nw 50 -ner 0.5 -es 1.3 -ne "$h" -mp $b
>>>>>>> fog_cloud_topology
          python3 generate_graph.py
          python3 allPairs.py
     
          a=1
<<<<<<< HEAD
          while [ "$a" -lt 50 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py 6 "$k"	
=======
          while [ "$a" -lt 3 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py 6 10	
>>>>>>> fog_cloud_topology
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
<<<<<<< HEAD
              python3 computePlanCosts_aug.py "QWL$k"
              
              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
          done
          
          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
=======
              python3 computePlanCosts_aug.py "QWL$k" $b
              
              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
        #   done
      done    
          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done
>>>>>>> fog_cloud_topology
  done
  
  echo "Script completed at: $(date)"
  

