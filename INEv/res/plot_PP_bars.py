#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot bar graph from CSV files with multiple Y values.

Original Author: samira
Modified by Assistant to support multiple Y columns.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to generate bar plot
def plot_bar(files, y_columns, labels, output_file):
    # Check that the number of input files and labels match
    if len(files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")

    # Initialize data structure for the bar plot
    # Data will be a list of lists: data[file_index][y_column_index]
    data_means = []

    # Collect the mean of each y_column from each file
    for file in files:
        data = pd.read_csv(file)
        means = []
        for y_col in y_columns:
            if y_col not in data.columns:
                raise ValueError(f"Column '{y_col}' not found in file '{file}'.")
            mean_value = data[y_col].mean()
            means.append(mean_value)
        data_means.append(means)

    # Number of groups and bars
    n_groups = len(labels)
    n_bars = len(y_columns)

    # Create positions for the bars
    total_width = 0.8
    bar_width = total_width / n_bars
    positions = np.arange(n_groups)

    # Adjust labels if needed (e.g., extract numeric part from 'MaxParents_2')
    # Here, we extract the number after '_' in each label
    x_labels = [int(label.split('_')[1]) if '_' in label else label for label in labels]

    # Set up the plot
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 17})

    # Colors for the bars
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if n_bars > len(colors):
        # Extend the color list if not enough colors
        colors *= (n_bars // len(colors) + 1)

    # Plot each set of bars
    for i in range(n_bars):
        # Calculate the position offset for each bar in the group
        offset = (i - n_bars / 2) * bar_width + bar_width / 2
        bar_positions = positions + offset

        # Extract the means for the current y_column across all files
        means = [data_means[j][i] for j in range(n_groups)]

        # Plot bars
        plt.bar(bar_positions, means, width=bar_width, label=y_columns[i], color=colors[i % len(colors)], align='center')

        # Plot the trend line connecting the tops of the bars
        plt.plot(bar_positions, means, marker='o', linestyle='-', color='red')

    plt.xlabel('Max Parents')
    plt.ylabel('Mean Values')
    plt.title(f'Mean Values for Different MaxParents')
    
    # Set x-axis labels and ensure alignment
    plt.xticks(positions, x_labels, rotation=45, ha='right')

    # Set y-axis ticks
    max_y = max([max(means) for means in data_means]) * 1.1
    plt.yticks(np.linspace(0, 1, num=11))
    # plt.ylim(0, max_y)

    # Add legend
    plt.legend()

    # Adjust layout
    plt.tight_layout()

    # Save the figure to a file
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot bar graph from CSV files with multiple Y values.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="List of input CSV files.")
    parser.add_argument('-y', '--y_columns', nargs='+', required=True, help="Column names for y-axis (e.g., TransmissionRatio TransmissionRatioINEv)")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the files (e.g., MaxParents_2 MaxParents_3)")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the bar plot")

    args = parser.parse_args()

    # Call the plotting function
    plot_bar(args.input_files, args.y_columns, args.labels, args.output_file)

if __name__ == "__main__":
    main()
