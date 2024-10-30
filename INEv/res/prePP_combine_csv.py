#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

def combine_csv_files(output_file):
    # Define schema
    columns = [
        "ID", "TransmissionRatio", "Transmission", "INEvTransmission", "FilterUsed", "Nodes",
        "EventSkew", "EventNodeRatio", "WorkloadSize", "NumberProjections", "MinimalSelectivity",
        "MedianSelectivity", "CombigenComputationTime", "Efficiency", "PlacementComputationTime",
        "HopCount", "Depth", "ProcessingLatencyRatio", "CentralTransmission", "LowerBound", 
        "EventTypes", "MaximumParents", "greedy_costs", "sampling_costs", "factorial_costs", 
        "exact_costs", "TransmissionRatioINEv", "TransmissionRatioCentral"
    ]

    # Initialize an empty DataFrame with specified schema
    combined_data = pd.DataFrame(columns=columns)

    # List of EventSkew values
    event_skew_values = [
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2
    ]
    
    # Loop through each EventSkew value to load the corresponding CSV file
    for k in event_skew_values:
        file_name = f"PP_EventSkew_{k}.csv"
        
        # Check if file exists
        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            
            # Ensure the data matches the required schema
            if set(columns).issubset(df.columns):
                df = df[columns]  # Select only the required columns
                combined_data = pd.concat([combined_data, df], ignore_index=True)
            else:
                print(f"Schema mismatch in file {file_name}. Skipping this file.")
        else:
            print(f"File {file_name} not found. Skipping.")

    # Save the combined data to a new CSV file
    combined_data.to_csv(output_file, index=False)
    print(f"Combined CSV saved as {output_file}")

if __name__ == "__main__":
    combine_csv_files("combined_output.csv")
