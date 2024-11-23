#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot a bar graph with range bars and outliers, adaptable Y-axis limits.

Original Author: samira
Modified to support dynamic Y-axis and customizable bounds.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_percentile_bars(input_files, y_columns, x_column, labels, output_file, colors=None, y_min=None, y_max=None, min_height=0.3, x_label=None, y_label=None, legend_labels=None):
    """
    Generates a bar graph where each unique x-axis point shows the range from the 10th to 90th percentile
    of y_column values, with whiskers extending to outliers.

    Parameters:
    - input_files: List of CSV file paths.
    - y_columns: List of Y-axis column names in the CSV files.
    - x_column: Name of the X-axis column in the CSV files.
    - labels: List of labels corresponding to each CSV file.
    - output_file: Path to save the output plot.
    - colors: List of colors for the bars (optional).
    - y_min: Minimum Y-axis limit (optional).
    - y_max: Maximum Y-axis limit (optional).
    - min_height: Minimum height for each bar to ensure visibility (default is 0.02).
    - x_label: Custom label for the x-axis (optional).
    - y_label: Custom label for the y-axis (optional).
    - legend_labels: Custom labels for the legend (optional).
    """
    # Validate file and label counts
    if len(input_files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")
    if colors and len(colors) != len(labels) * len(y_columns):
        raise ValueError("The number of colors must match the total number of bars (input files multiplied by Y columns).")

    # Default colors if not provided
    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Dictionary to hold data for each (x_point, label, y_column)
    data_dict = {}

    # Track overall min and max for dynamic Y-axis range calculation
    global_min, global_max = float('inf'), float('-inf')

    # Collect data from each file and y_column
    for idx, file in enumerate(input_files):
        label = labels[idx]
        df = pd.read_csv(file)

        for y_col in y_columns:
            if y_col not in df.columns:
                raise ValueError(f"Column '{y_col}' not found in file '{file}'.")

            # Group data by x_column and calculate percentiles
            grouped = df.groupby(x_column)[y_col]

            for x_point, group in grouped:
                key = (x_point, label, y_col)
                p10 = np.percentile(group, 10)
                p90 = np.percentile(group, 90)
                min_value = group.min()
                max_value = group.max()

                # Update global min and max
                global_min = min(global_min, min_value)
                global_max = max(global_max, max_value)

                data_dict[key] = {'p10': p10, 'p90': p90, 'min': min_value, 'max': max_value}

    # Get sorted unique x-axis points
    x_points = sorted(set([key[0] for key in data_dict.keys()]))
    n_labels = len(labels)
    n_y_columns = len(y_columns)
    n_bars_per_group = n_labels * n_y_columns

    # Prepare data for plotting
    bar_positions, bar_heights, bar_bottoms = [], [], []
    lower_whisker, upper_whisker, bar_labels, bar_colors = [], [], [], []

    total_width = 0.8
    bar_width = total_width / n_bars_per_group
    positions = np.arange(len(x_points))
    plt.rcParams.update({'font.size': 17})

    color_idx = 0  # Color index

    # Prepare bar data for each label and y_column
    for idx_label, label in enumerate(labels):
        for idx_y, y_col in enumerate(y_columns):
            position_offset = idx_label * n_y_columns + idx_y
            positions_i_j = positions - total_width / 2 + bar_width / 2 + position_offset * bar_width
            bar_positions.extend(positions_i_j)
            bar_labels.extend([f"{label} - {y_col}"] * len(x_points))
            bar_colors.extend([colors[color_idx % len(colors)]] * len(x_points))
            color_idx += 1

            heights, bottoms, err_lower, err_upper = [], [], [], []

            for x_point in x_points:
                key = (x_point, label, y_col)
                if key in data_dict:
                    p10 = data_dict[key]['p10']
                    p90 = data_dict[key]['p90']
                    min_value = data_dict[key]['min']
                    max_value = data_dict[key]['max']
                    bar_height = p90 - p10

                    # Enforce minimum bar height
                    if bar_height < min_height:
                        heights.append(min_height)
                        bottoms.append(p10 - (min_height - bar_height) / 2)
                    else:
                        heights.append(bar_height)
                        bottoms.append(p10)

                    err_lower.append(p10 - min_value)
                    err_upper.append(max_value - p90)
                else:
                    heights.append(np.nan)
                    bottoms.append(np.nan)
                    err_lower.append(None)
                    err_upper.append(None)

            bar_heights.append(heights)
            bar_bottoms.append(bottoms)
            lower_whisker.append(err_lower)
            upper_whisker.append(err_upper)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    capwidth = bar_width * 0.4

    total_bars = len(bar_positions)
    for i in range(total_bars):
        x_pos = bar_positions[i]
        height = bar_heights[i // len(x_points)][i % len(x_points)]
        bottom = bar_bottoms[i // len(x_points)][i % len(x_points)]
        lower_w = lower_whisker[i // len(x_points)][i % len(x_points)]
        upper_w = upper_whisker[i // len(x_points)][i % len(x_points)]
        color = bar_colors[i]

        ax.bar(x_pos, height, width=bar_width, bottom=bottom, color=color, align='center', zorder=2)

        # Lower whisker
        if lower_w is not None:
            ax.vlines(x_pos, bottom - lower_w, bottom, color='black', linestyle='-', zorder=3)
            ax.hlines(bottom - lower_w, x_pos - capwidth / 2, x_pos + capwidth / 2, color='black', zorder=3)
        # Upper whisker
        if upper_w is not None:
            ax.vlines(x_pos, bottom + height, bottom + height + upper_w, color='black', linestyle='-', zorder=3)
            ax.hlines(bottom + height + upper_w, x_pos - capwidth / 2, x_pos + capwidth / 2, color='black', zorder=3)

    # Set Y-axis limits
    if y_min is None:
        y_min = max(0, global_min - 0.1 * abs(global_min))  # 10% buffer
    if y_max is None:
        y_max = global_max + 0.1 * abs(global_max)  # 10% buffer
    ax.set_ylim(y_min, y_max)
    plt.ylabel(y_label if y_label else 'Computation Time',fontsize=25)

    # Customize ticks
    ax.set_yticks(np.linspace(y_min, y_max, 10))
    plt.yticks(fontsize=23)
    # X-axis labels
    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in x_points])

    plt.xticks(fontsize=23)
    plt.xlabel(x_label if x_label else x_column,fontsize=25)
    
    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = []
    custom_legend_labels = legend_labels if legend_labels else [f"{label} - {y_col}" for label in labels for y_col in y_columns]
    if len(custom_legend_labels) != n_labels * n_y_columns:
        raise ValueError("Number of legend labels must match the total number of input files and Y columns.")
    
    for idx, legend_label in enumerate(custom_legend_labels):
        color = colors[idx % len(colors)]
        legend_elements.append(Line2D([0], [0], color=color, lw=10, label=legend_label))

    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=2)

    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot a bar graph with percentile range and dynamic Y-axis.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="Input CSV files.")
    parser.add_argument('-y', '--y_columns', nargs='+', required=True, help="Y-axis column name(s).")
    parser.add_argument('-x', '--x_column', required=True, help="X-axis column name.")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the input files.")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the plot.")
    parser.add_argument('-c', '--colors', nargs='+', help="Colors for the bars (optional).")
    parser.add_argument('--y_min', type=float, help="Minimum Y-axis value (optional).")
    parser.add_argument('--y_max', type=float, help="Maximum Y-axis value (optional).")
    parser.add_argument('--x_label', help="Custom label for the x-axis")
    parser.add_argument('--y_label', help="Custom label for the y-axis")
    parser.add_argument('--legend_labels', nargs='+', help="Custom labels for the legend")

    args = parser.parse_args()

    plot_percentile_bars(
        args.input_files,
        args.y_columns,
        args.x_column,
        args.labels,
        args.output_file,
        colors=args.colors,
        y_min=args.y_min,
        y_max=args.y_max,
        x_label=args.x_label,
        y_label=args.y_label,
        legend_labels=args.legend_labels
    )

if __name__ == "__main__":
    main()
