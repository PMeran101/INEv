#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot grouped bar graph from multiple CSV files with multiple Y values for each X-axis entry.

Original Author: samira
Modified by Assistant to support multiple files with multiple Y columns.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to generate bar plot
def plot_bar(files, x_column, y_columns, labels, output_file):
    # Check that the number of input files and labels match
    if len(files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")

    # Initialize data structure for the bar plot
    data_means = []

    # Collect data from each file
    for file in files:
        data = pd.read_csv(file)
        
        # Ensure the specified columns exist in the data
        if x_column not in data.columns:
            raise ValueError(f"X-axis column '{x_column}' not found in file '{file}'.")
        for y_col in y_columns:
            if y_col not in data.columns:
                raise ValueError(f"Y-axis column '{y_col}' not found in file '{file}'.")

        # Calculate the mean for each Y column
        means = []
        for y_col in y_columns:
            mean_values = data.groupby(x_column)[y_col].mean().sort_index()
            means.append(mean_values)
        data_means.append(means)

    # Determine the unique X-axis values and number of groups and bars
    x_labels = data[x_column].unique()
    n_groups = len(x_labels)
    n_files = len(files)
    n_bars = len(y_columns)

    # Create positions for the bars
    total_width = 0.8
    bar_width = total_width / (n_bars * n_files)
    positions = np.arange(n_groups)

    # Set up the plot
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 17})

    # Colors for the bars
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if n_bars * n_files > len(colors):
        colors *= (n_bars * n_files // len(colors) + 1)

    # Plot each file's data
    for i, (means, label) in enumerate(zip(data_means, labels)):
        for j, (y_col, y_data) in enumerate(zip(y_columns, means)):
            # Calculate the position offset for each bar
            offset = (i * n_bars + j - (n_bars * n_files) / 2) * bar_width + bar_width / 2
            bar_positions = positions + offset

            # Plot bars for each Y column from each file
            plt.bar(bar_positions, y_data, width=bar_width, label=f"{label} - {y_col}", color=colors[(i * n_bars + j) % len(colors)], align='center')

    plt.xlabel(x_column)
    plt.ylabel('ComputationTime')
    plt.title(f'Computation Time for Different {x_column}')

    # Set x-axis labels and ensure alignment
    plt.xticks(positions, x_labels, rotation=45, ha='right')

    # Adjust y-axis limits
    max_y = max([y.max() for file_means in data_means for y in file_means]) * 1.1  # Add 10% buffer
    plt.ylim(0, max_y)

    # Add legend
    plt.legend()

    # Adjust layout
    plt.tight_layout()

    # Save the figure to a file
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot grouped bar graph from multiple CSV files with multiple Y values.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="List of input CSV files.")
    parser.add_argument('-x', '--x_column', required=True, help="Column name for x-axis.")
    parser.add_argument('-y', '--y_columns', nargs='+', required=True, help="Column names for y-axis (e.g., TransmissionRatio TransmissionRatioINEv)")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the files (e.g., File1 File2)")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the bar plot")

    args = parser.parse_args()

    # Call the plotting function
    plot_bar(args.input_files, args.x_column, args.y_columns, args.labels, args.output_file)

if __name__ == "__main__":
    main()