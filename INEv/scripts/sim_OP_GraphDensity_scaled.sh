
#!/bin/sh

cd ../code
for nw in 100 500 1000 5000 10000
do 
  for k in 5 10 20 # qwl amount
  do 
      for h in 6 10 15 20 25 # num event types
      do

    # Calculate b as percentages of nw
        for perc in 3 4 5 6 7 8 9 10 15 20 25 30
        do
              b=$(( nw * perc / 100 ))  # Calculate b as integer percentage of nw

              echo "  b is $b (which is $perc% of $nw)"
          #echo "Starting outer loop with k=$k and h=$h at: $(date)"

          python3 generate_network.py -nw $nw -ner 0.5 -es 1.3 -ne "$h" -mp $b
          python3 generate_graph.py
          python3 allPairs.py
     
          a=1
          while [ "$a" -lt 3 ]
          do
             # echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py --length 6 --count $k	
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py --file "OP_Network_Size_$nw" --number_parents $b

              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
        
        #   done
      done    
          #cho "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done
  done
  done
  
  #echo "Script completed at: $(date)"
  

