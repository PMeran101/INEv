#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for plotting bar graphs from CSV files with customizable parameters.

Features:
1. Bar graph plotting.
2. Parameterized via command-line arguments.
3. Accepts multiple CSV files as input parameters.
4. Allows specifying x and y axes.
5. Lets you edit the legend through parameters.
6. Groups values to be shown as bars based on a specified column.
7. Allows prefiltering specific group values to reduce the number of bars.

Usage example:
python script.py -i data1.csv data2.csv -x category -y value -groupC parameter -group_values 0.4 0.8 1.3 \
-c red blue green -l "Param=0.4" "Param=0.8" "Param=1.3" -o output.pdf \
--x_label "Categories" --y_label "Values"
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate Bar Graphs from CSV data')
    myargs = myparse_args(parser)
    data_list = []

    # Load and combine data from multiple CSV files
    for input_file in myargs.inputs:
        df = pd.read_csv(input_file)
        data_list.append(df)
    data = pd.concat(data_list, ignore_index=True)

    # Ensure the x and y columns exist
    if myargs.xC not in data.columns:
        print(f"X-axis column '{myargs.xC}' does not exist in the input data.")
        print("Available columns:", list(data.columns))
        return

    if myargs.yC not in data.columns:
        print(f"Y-axis column '{myargs.yC}' does not exist in the input data.")
        print("Available columns:", list(data.columns))
        return

    # Ensure the group column exists
    if myargs.groupC and myargs.groupC not in data.columns:
        print(f"Group column '{myargs.groupC}' does not exist in the input data.")
        print("Available columns:", list(data.columns))
        return

    # Filter group values if specified
    if myargs.groupC:
        if myargs.group_values:
            group_values = [type(data[myargs.groupC].iloc[0])(val) for val in myargs.group_values]
            data = data[data[myargs.groupC].isin(group_values)]
        unique_groups = sorted(data[myargs.groupC].unique())
    else:
        unique_groups = [None]  # No grouping, plot all data in one bar

    # Prepare data for plotting
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 17})
    plt.xlabel(myargs.x_label if myargs.x_label else myargs.xC, fontsize=25)
    plt.ylabel(myargs.y_label if myargs.y_label else myargs.yC, fontsize=25)
    # Calculate dynamic y-axis limits
    y_min = 0
    y_max = data[myargs.yC].max() #* 0.6

    # Remove outliers based on IQR
    # q1 = data[myargs.yC].quantile(0.25)  # First quartile
    # q3 = data[myargs.yC].quantile(0.75)  # Third quartile
    # iqr = q3 - q1  # Interquartile range
    # upper_bound = q3 + 1.5 * iqr  # Upper bound for outlier detection

    # # Adjust y_max to exclude outliers if necessary
    # if y_max > upper_bound:
    #     print(f"Excluding outliers above {upper_bound:.2f}")
    #     y_max = upper_bound

    # Add a small margin for better visualization
    y_margin = (y_max - y_min) * 0.05  # 5% margin
    y_max += y_margin

    # # Generate ticks dynamically
    # y_ticks = np.round(np.linspace(0, y_max, num=11),2)  # 11 ticks for consistent spacing

    # # Set y-axis limits and ticks dynamically
    # plt.ylim(0, y_max)
    # plt.yticks(y_ticks, fontsize=23)


    plt.ylim(0, 1.05)
    plt.yticks(np.linspace(0, 1, 11),fontsize=23)
    
    
    colors = myargs.colors if myargs.colors else ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    labels = myargs.labels if myargs.labels else [f"{myargs.groupC}={group}" for group in unique_groups]

    # Check for mismatches in customization
    if len(colors) < len(unique_groups):
        print("Not enough colors specified for the number of groups. Repeating colors.")
    if len(labels) < len(unique_groups):
        print("Not enough labels specified for the number of groups. Using default labels.")

    x_categories = sorted(data[myargs.xC].unique())
    x_indices = np.arange(len(x_categories))
    bar_width = 0.8 / len(unique_groups)  # Adjust bar width based on the number of groups

    # Create a mapping from category to index for positioning
    category_to_index = {category: idx for idx, category in enumerate(x_categories)}

    # Plot each group
    for idx, group in enumerate(unique_groups):
        if group is not None:
            group_data = data[data[myargs.groupC] == group]
        else:
            group_data = data

        # Aggregate data (e.g., mean) for each category
        agg_data = group_data.groupby(myargs.xC)[myargs.yC].mean().reset_index()

        # Positions for the bars
        positions = [category_to_index[cat] + idx * bar_width for cat in agg_data[myargs.xC]]

        plt.bar(
            positions,
            agg_data[myargs.yC],
            width=bar_width,
            label=labels[idx % len(labels)],
            color=colors[idx % len(colors)]
        )

    plt.xticks(
        x_indices + bar_width * (len(unique_groups) - 1) / 2,
        x_categories,
        fontsize=15
    )
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=int(len(labels)/2), borderaxespad=0., frameon=True)
    plt.savefig(str(myargs.outname), format='svg', bbox_inches='tight')
    print(f"Plot saved as {myargs.outname}")

def myparse_args(parser):
    parser.add_argument('-i', '--inputs', nargs='+', help='Input CSV file(s)', required=True)
    parser.add_argument('-x', '--xC', help='x-axis column identifier (categories)', required=True)
    parser.add_argument('-y', '--yC', help='y-axis column identifier (values)', required=True)
    parser.add_argument('-groupC', help='Column to group bars by', required=False)
    parser.add_argument('-group_values', nargs='+', help='Specific values of the group column to include (optional)', required=False)
    parser.add_argument('-c', '--colors', nargs='+', required=False, help='Colors for each group')
    parser.add_argument('-l', '--labels', nargs='+', required=False, help='Custom labels for each group')
    parser.add_argument('-o', '--outname', required=False, default="plot.pdf", help='Output file name')
    parser.add_argument('--x_label', required=False, help='Custom label for the X-axis')
    parser.add_argument('--y_label', required=False, help='Custom label for the Y-axis')
    return parser.parse_args()

if __name__ == "__main__":
    main()
