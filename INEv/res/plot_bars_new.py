#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for plotting bar graphs from CSV files with customizable parameters.

Features:
1. Bar graph plotting.
2. Supports multiple y-columns for comparison.
3. Parameterized via command-line arguments.
4. Allows specifying x and y axes.
5. Lets you edit the legend through parameters.
6. Supports multiple bars for different columns.

Usage example:
python plot_bars_new.py -i latency_test.csv -x MaximumParents -y "Transmission Ratio" "TransmissionRatioCentral" \
    -c tab:blue tab:orange -l "Base" "Hybrid" -o Exp4_MaxParents_total.pdf \
    --x_label "Max parents" --y_label "Transmission ratio"
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate Bar Graphs from CSV data')
    myargs = myparse_args(parser)

    # Load the data
    data = pd.read_csv(myargs.inputs[0])  # Assuming single input CSV for simplicity

    # Ensure the x and y columns exist
    if myargs.xC not in data.columns:
        print(f"X-axis column '{myargs.xC}' does not exist in the input data.")
        print("Available columns:", list(data.columns))
        return

    for yC in myargs.yC:
        if yC not in data.columns:
            print(f"Y-axis column '{yC}' does not exist in the input data.")
            print("Available columns:", list(data.columns))
            return

    # Prepare data for plotting
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 17})
    plt.xlabel(myargs.x_label if myargs.x_label else myargs.xC, fontsize=25)
    plt.ylabel(myargs.y_label if myargs.y_label else "Values", fontsize=25)
    plt.ylim(0, 1.05)
    plt.yticks(np.linspace(0, 1, 11),fontsize=23)
    # X-axis categories
    x_categories = sorted(data[myargs.xC].unique())
    x_indices = np.arange(len(x_categories))
    bar_width = 0.8 / len(myargs.yC)  # Adjust bar width based on the number of y-columns

    # Colors and labels
    colors = myargs.colors if myargs.colors else ['b', 'g', 'r', 'c', 'm', 'y', 'k'] * len(myargs.yC)
    labels = myargs.labels if myargs.labels else myargs.yC

    # Plot bars for each y-column
    for idx, yC in enumerate(myargs.yC):
        # Aggregate data (e.g., mean) for each category in the x-axis
        agg_data = data.groupby(myargs.xC)[yC].mean().reset_index()

        # Positions for the bars
        positions = x_indices + idx * bar_width

        plt.bar(
            positions,
            agg_data[yC],
            width=bar_width,
            color=colors[idx % len(colors)],
            label=labels[idx % len(labels)]
        )

    plt.xticks(
        x_indices + bar_width * (len(myargs.yC) - 1) / 2,
        x_categories,
        fontsize=15
    )

    # Add legend and save the plot
    plt.legend(fontsize=15, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(labels), frameon=True)
    #plt.tight_layout()
    plt.savefig(str(myargs.outname), format='pdf', bbox_inches='tight')
    print(f"Plot saved as {myargs.outname}")

def myparse_args(parser):
    parser.add_argument('-i', '--inputs', nargs=1, help='Input CSV file', required=True)
    parser.add_argument('-x', '--xC', help='x-axis column identifier (categories)', required=True)
    parser.add_argument('-y', '--yC', nargs='+', help='y-axis columns for multiple bars', required=True)
    parser.add_argument('-c', '--colors', nargs='+', required=False, help='Colors for each bar')
    parser.add_argument('-l', '--labels', nargs='+', required=False, help='Custom labels for each column')
    parser.add_argument('-o', '--outname', required=False, default="plot.pdf", help='Output file name')
    parser.add_argument('--x_label', required=False, help='Custom label for the X-axis')
    parser.add_argument('--y_label', required=False, help='Custom label for the Y-axis')
    return parser.parse_args()

if __name__ == "__main__":
    main()
