#!/bin/sh
cd ../code

echo "nwSize_SQL"

# Initial network generation (if required)
python3 generate_network.py -nw 20 -ner 0.5 -es 1.3 -ne 25
python3 generate_graph.py
python3 allPairs.py

# Define scaling parameters
divisor=4
max_limit=20
min_parents=2  # Define a minimum number of parents

# Loop over k values
for k in 10 20  
do 
    echo "Processing k=$k at: $(date)"
    
    # Execute scripts dependent on k
    python3 generate_qwls.py 6 "$k"
    python3 generate_selectivity.py 

    # Loop over network sizes
    for j in 20 50 100 150 200 
    do
        echo "Processing network size j=$j at: $(date)"
        
        # Calculate max_parents based on nwsize with bounds
        calculated_max_parents=$((j / divisor))
        
        # Enforce minimum and maximum bounds
        if [ "$calculated_max_parents" -lt "$min_parents" ]; then
            calculated_max_parents="$min_parents"
        elif [ "$calculated_max_parents" -gt "$max_limit" ]; then
            calculated_max_parents="$max_limit"
        fi

        echo "Calculated max_parents for nwsize=$j: $calculated_max_parents"

        # Initialize iteration counter
        a=0
        while [ "$a" -lt 2 ]
        do
            echo "Starting iteration $a for nwsize=$j, k=$k at: $(date)"
            
            # Execute the sequence of Python scripts with the current parameters
            python3 generate_network.py -nw "$j" -ner 0.5 -es 1.3 -ne 25 -mp "$calculated_max_parents"
            python3 generate_graph.py
            python3 allPairs.py
            python3 write_config_single.py
            python3 determine_all_single_selectivities.py
            python3 generate_projections.py
            python3 combigen.py
            python3 computePlanCosts_aug.py "nwSize_qwl_$k" "$calculated_max_parents"
            
            # Increment the iteration counter
            a=$((a + 1))
        done
        
        # Echo completion of the current network size
        echo "Finished k=$k, j=$j, a=$a"
    done
    
    # Echo completion of the current k value
    echo "Finished k=$k, all j values, a=$a"
done

