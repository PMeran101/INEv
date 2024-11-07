
cd ../code

for k in 1 2 3 4 5 6 7 8
do 
for b in  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
do

      
          echo "Starting outer loop with k=$k and h=$h at: $(date)"

          python3 generate_network.py -nw 50 -ner $b -es 1.3 -ne 10 -mp $k
          python3 generate_graph.py
          python3 allPairs.py
     
          a=1
          while [ "$a" -lt 100 ]
          do
              echo "  Starting inner loop iteration $a with k=$k at: $(date)"
              
              python3 generate_qwls.py --length 6 --count 10	
              python3 generate_selectivity.py 
              python3 write_config_single.py
              python3 determine_all_single_selectivities.py
              python3 generate_projections.py
              python3 combigen.py
              python3 computePlanCosts_aug.py --file "OP_NER_Combined" --number_parents $k

              echo "  Completed inner loop iteration $a with k=$k at: $(date)"
              a=$((a + 1))
    
        done

          echo "Completed outer loop with k=$k and h=$h at: $(date)"
      done
      done