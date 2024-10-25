#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:43:03 2021

@author: samira
Modified to support multiple Y columns.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_percentile_bars(input_files, y_columns, x_column, labels, output_file, colors=None):
    """
    Generates a bar graph where for each unique x-axis point, the bar represents the range
    from the 10th percentile to the 90th percentile of the y_column values.
    Whiskers show the outliers (minimum to 10th percentile and 90th percentile to maximum).
    Allows customization of figure size and bar colors.

    Parameters:
    - input_files: List of CSV file paths.
    - y_columns: List of Y-axis column names in the CSV files.
    - x_column: Name of the X-axis column in the CSV files.
    - labels: List of labels corresponding to each CSV file.
    - output_file: Path to save the output plot.
    - colors: List of colors for the bars (optional).
    """
    # Check that the number of input files and labels match
    if len(input_files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")
    if colors and len(colors) != len(labels) * len(y_columns):
        raise ValueError("The number of colors must match the total number of bars (input files multiplied by Y columns).")

    # Set default colors if not provided
    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Dictionary to hold data for each (x_point, label, y_column)
    data_dict = {}

    # Collect data from each file and y_column
    for idx, file in enumerate(input_files):
        label = labels[idx]
        df = pd.read_csv(file)

        for y_col in y_columns:
            if y_col not in df.columns:
                raise ValueError(f"Column '{y_col}' not found in file '{file}'.")

            # Group data by x_column
            grouped = df.groupby(x_column)[y_col]

            for x_point, group in grouped:
                key = (x_point, label, y_col)
                # Calculate percentiles and min/max
                p10 = np.percentile(group, 10)
                p90 = np.percentile(group, 90)
                min_value = group.min()
                max_value = group.max()
                data_dict[key] = {'p10': p10, 'p90': p90, 'min': min_value, 'max': max_value}

    # Get sorted unique x-axis points
    x_points = sorted(set([key[0] for key in data_dict.keys()]))
    n_labels = len(labels)
    n_y_columns = len(y_columns)
    n_bars_per_group = n_labels * n_y_columns

    # Prepare data for plotting
    bar_positions = []
    bar_heights = []
    bar_bottoms = []
    lower_whisker = []
    upper_whisker = []
    bar_labels = []
    bar_colors = []

    # Width of each bar group and individual bars
    total_width = 0.8
    bar_width = total_width / n_bars_per_group

    # Positions for each group of bars
    positions = np.arange(len(x_points))

    # Adjust font size for consistency
    plt.rcParams.update({'font.size': 17})

    color_idx = 0  # Index for colors list

    for idx_label, label in enumerate(labels):
        for idx_y, y_col in enumerate(y_columns):
            position_offset = idx_label * n_y_columns + idx_y
            positions_i_j = positions - total_width / 2 + bar_width / 2 + position_offset * bar_width
            bar_positions.extend(positions_i_j)
            bar_labels.extend([f"{label} - {y_col}"] * len(x_points))
            bar_colors.extend([colors[color_idx % len(colors)]] * len(x_points))
            color_idx += 1

            heights = []
            bottoms = []
            err_lower = []
            err_upper = []

            for x_point in x_points:
                key = (x_point, label, y_col)
                if key in data_dict:
                    p10 = data_dict[key]['p10']
                    p90 = data_dict[key]['p90']
                    min_value = data_dict[key]['min']
                    max_value = data_dict[key]['max']
                    bar_height = p90 - p10

                    # Handle zero bar height
                    if round(bar_height, 2) == 0.0:
                        # Set minimal bar height
                        minimal_height = 0.015  # Adjust this value as needed
                        heights.append(minimal_height)
                        bottoms.append(p10 - minimal_height / 2)
                    else:
                        heights.append(bar_height)
                        bottoms.append(p10)

                    err_lower_value = p10 - min_value
                    err_upper_value = max_value - p90

                    # Handle zero whisker lengths
                    err_lower.append(err_lower_value if err_lower_value != 0 else None)
                    err_upper.append(err_upper_value if err_upper_value != 0 else None)
                else:
                    # If data is missing, use NaN
                    heights.append(np.nan)
                    bottoms.append(np.nan)
                    err_lower.append(None)
                    err_upper.append(None)

            bar_heights.append(heights)
            bar_bottoms.append(bottoms)
            lower_whisker.append(err_lower)
            upper_whisker.append(err_upper)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))  # Adjusted figure size
    capwidth = bar_width * 0.4  # Width of the whisker caps

    # Plot bars with whiskers
    total_bars = len(bar_positions)  # Total number of bars to plot
    for i in range(total_bars):
        x_pos = bar_positions[i]
        height = bar_heights[i // len(x_points)][i % len(x_points)]
        bottom = bar_bottoms[i // len(x_points)][i % len(x_points)]
        lower_whisker_value = lower_whisker[i // len(x_points)][i % len(x_points)]
        upper_whisker_value = upper_whisker[i // len(x_points)][i % len(x_points)]
        color = bar_colors[i]

        # Plot bar
        ax.bar(
            x_pos,
            height,
            width=bar_width,
            bottom=bottom,
            align='center',
            zorder=2,
            color=color
        )

        # Plot whiskers
        if not np.isnan(bottom):
            # Lower whisker
            if lower_whisker_value is not None:
                ax.vlines(
                    x_pos,
                    bottom - lower_whisker_value,
                    bottom,
                    color='black',
                    linestyle='-',
                    zorder=3
                )
                # Add cap
                ax.hlines(
                    bottom - lower_whisker_value,
                    x_pos - capwidth / 2,
                    x_pos + capwidth / 2,
                    color='black',
                    zorder=3
                )
            # Upper whisker
            if upper_whisker_value is not None:
                ax.vlines(
                    x_pos,
                    bottom + height,
                    bottom + height + upper_whisker_value,
                    color='black',
                    linestyle='-',
                    zorder=3
                )
                # Add cap
                ax.hlines(
                    bottom + height + upper_whisker_value,
                    x_pos - capwidth / 2,
                    x_pos + capwidth / 2,
                    color='black',
                    zorder=3
                )
            # If both whiskers are None and bar height is minimal, plot a marker
            if lower_whisker_value is None and upper_whisker_value is None and height == minimal_height:
                ax.plot(
                    x_pos,
                    bottom + height / 2,
                    marker='o',
                    color='black',
                    zorder=4
                )

    # Set y-axis range from 0 to 1 with appropriate steps
    ax.set_ylim(0, 1)
    ax.set_yticks(np.linspace(0, 1, 11))  # Set ticks at intervals of 0.1
    ax.set_yticklabels([f"{y:.1f}" for y in np.linspace(0, 1, 11)])

    # Set x-axis labels
    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in x_points])

    plt.xlabel(x_column)
    plt.ylabel("Values")
    # plt.title(f"{', '.join(y_columns)} vs {x_column} with 80% Range Bars and Outliers")
    # Create a custom legend
    from matplotlib.lines import Line2D
    legend_elements = []
    for idx_label, label in enumerate(labels):
        for idx_y, y_col in enumerate(y_columns):
            color = colors[(idx_label * n_y_columns + idx_y) % len(colors)]
            legend_elements.append(
                Line2D([0], [0], color=color, lw=10, label=f"{label} - {y_col}")
            )
    ax.legend(handles=legend_elements, title="Data Sets")
    plt.tight_layout()
    # plt.grid(axis='y', linestyle='--', zorder=0)

    # Save the plot
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot a bar graph with 80% range bars and outliers.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="Input CSV files.")
    parser.add_argument('-y', '--y_columns', nargs='+', required=True, help="Y-axis column name(s).")
    parser.add_argument('-x', '--x_column', required=True, help="X-axis column name.")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the input files.")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the plot.")
    parser.add_argument('-c', '--colors', nargs='+', help="Colors for the bars (optional).")
    parser.add_argument('--figsize', nargs=2, type=float, default=[10, 6], help="Figure size as width height (default: 10 6).")

    args = parser.parse_args()

    # Call the plotting function
    plot_percentile_bars(
        args.input_files,
        args.y_columns,
        args.x_column,
        args.labels,
        args.output_file,
        colors=args.colors
    )

if __name__ == "__main__":
    main()
