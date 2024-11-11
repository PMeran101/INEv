import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def plot_percentile_bars(input_files, y_columns, x_column, labels, output_file, colors=None, hatches=None, legend_names=None, x_label=None, y_label=None):
    # Validate inputs
    if len(input_files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")
    if colors and len(colors) != len(labels) * len(y_columns):
        raise ValueError("The number of colors must match the total number of bars (input files multiplied by Y columns).")
    if hatches and len(hatches) != len(labels) * len(y_columns):
        raise ValueError("The number of hatches must match the total number of bars (input files multiplied by Y columns).")
    if legend_names and len(legend_names) != len(labels) * len(y_columns):
        raise ValueError("The number of legend names must match the total number of bars (input files multiplied by Y columns).")

    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if not hatches:
        hatches = [''] * (len(labels) * len(y_columns))

    data_dict = {}
    for idx, file in enumerate(input_files):
        label = labels[idx]
        df = pd.read_csv(file)

        for y_col in y_columns:
            if y_col not in df.columns:
                raise ValueError(f"Column '{y_col}' not found in file '{file}'.")
            grouped = df.groupby(x_column)[y_col]
            for x_point, group in grouped:
                key = (x_point, label, y_col)
                p10 = np.percentile(group, 10)
                p90 = np.percentile(group, 90)
                min_value = group.min()
                max_value = group.max()
                data_dict[key] = {'p10': p10, 'p90': p90, 'min': min_value, 'max': max_value}

    x_points = sorted(set([key[0] for key in data_dict.keys()]))
    n_labels = len(labels)
    n_y_columns = len(y_columns)
    n_bars_per_group = n_labels * n_y_columns

    bar_positions = []
    bar_heights = []
    bar_bottoms = []
    lower_whisker = []
    upper_whisker = []
    bar_colors = []
    bar_hatches = []

    total_width = 0.7
    bar_width = total_width / n_bars_per_group
    bar_spacing = 0.05

    positions = np.arange(len(x_points))
    plt.rcParams.update({'font.size': 17})

    color_idx = 0

    for idx_label, label in enumerate(labels):
        for idx_y, y_col in enumerate(y_columns):
            position_offset = idx_label * n_y_columns + idx_y
            positions_i_j = positions - total_width / 2 + bar_width / 2 + position_offset * (bar_width + bar_spacing)
            bar_positions.extend(positions_i_j)
            bar_colors.extend([colors[color_idx % len(colors)]] * len(x_points))
            bar_hatches.extend([hatches[color_idx % len(hatches)]] * len(x_points))
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

                    if round(bar_height, 2) == 0.0:
                        minimal_height = 0.015
                        heights.append(minimal_height)
                        bottoms.append(p10 - minimal_height / 2)
                    else:
                        heights.append(bar_height)
                        bottoms.append(p10)

                    err_lower_value = p10 - min_value
                    err_upper_value = max_value - p90
                    err_lower.append(err_lower_value if err_lower_value != 0 else None)
                    err_upper.append(err_upper_value if err_upper_value != 0 else None)
                else:
                    heights.append(np.nan)
                    bottoms.append(np.nan)
                    err_lower.append(None)
                    err_upper.append(None)

            bar_heights.append(heights)
            bar_bottoms.append(bottoms)
            lower_whisker.append(err_lower)
            upper_whisker.append(err_upper)

    fig, ax = plt.subplots(figsize=(12, 6))
    capwidth = bar_width * 0.4

    total_bars = len(bar_positions)
    for i in range(total_bars):
        x_pos = bar_positions[i]
        height = bar_heights[i // len(x_points)][i % len(x_points)]
        bottom = bar_bottoms[i // len(x_points)][i % len(x_points)]
        lower_whisker_value = lower_whisker[i // len(x_points)][i % len(x_points)]
        upper_whisker_value = upper_whisker[i // len(x_points)][i % len(x_points)]
        color = bar_colors[i]
        hatch = bar_hatches[i]

        ax.bar(
            x_pos,
            height,
            width=bar_width,
            bottom=bottom,
            align='center',
            zorder=2,
            color=color,
            hatch=hatch
        )

        if not np.isnan(bottom):
            if lower_whisker_value is not None:
                ax.vlines(
                    x_pos,
                    bottom - lower_whisker_value,
                    bottom,
                    color='black',
                    linestyle='-',
                    zorder=3
                )
                ax.hlines(
                    bottom - lower_whisker_value,
                    x_pos - capwidth / 2,
                    x_pos + capwidth / 2,
                    color='black',
                    zorder=3
                )
            if upper_whisker_value is not None:
                ax.vlines(
                    x_pos,
                    bottom + height,
                    bottom + height + upper_whisker_value,
                    color='black',
                    linestyle='-',
                    zorder=3
                )
                ax.hlines(
                    bottom + height + upper_whisker_value,
                    x_pos - capwidth / 2,
                    x_pos + capwidth / 2,
                    color='black',
                    zorder=3
                )

    ax.set_ylim(0, 1.05)
    ax.set_yticks(np.linspace(0, 1, 11))
    ax.set_yticklabels([f"{y:.1f}" for y in np.linspace(0, 1, 11)])
    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in x_points])

    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)

    from matplotlib.patches import Patch
    legend_elements = []
    for idx, name in enumerate(legend_names):
        color = colors[idx % len(colors)]
        hatch = hatches[idx % len(hatches)]
        # Create a Patch with both color and hatch
        legend_elements.append(
            Patch(facecolor=color, edgecolor='black', hatch=hatch, label=name)
        )

    ax.legend(
        handles=legend_elements,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.4),
        ncol=len(legend_names) // 2,
        frameon=True
    )

    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot a bar graph with 80% range bars and outliers.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="Input CSV files.")
    parser.add_argument('-y', '--y_columns', nargs='+', required=True, help="Y-axis column name(s).")
    parser.add_argument('-x', '--x_column', required=True, help="X-axis column name.")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the input files.")
    parser.add_argument('-ln', '--legend_names', nargs='+', required=True, help="Custom legend names for each combination of label and Y column.")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the plot.")
    parser.add_argument('-c', '--colors', nargs='+', help="Colors for the bars (optional).")
    parser.add_argument('-t', '--hatches', nargs='+', help="Hatch patterns for the bars (optional).")
    parser.add_argument('--x_label', required=False, help="Label for the X-axis (optional).")
    parser.add_argument('--y_label', required=False, help="Label for the Y-axis (optional).")
    parser.add_argument('--figsize', nargs=2, type=float, default=[10, 6], help="Figure size as width height (default: 10 6).")

    args = parser.parse_args()

    plot_percentile_bars(
        args.input_files,
        args.y_columns,
        args.x_column,
        args.labels,
        args.output_file,
        colors=args.colors,
        hatches=args.hatches,
        legend_names=args.legend_names,
        x_label=args.x_label,
        y_label=args.y_label
    )

if __name__ == "__main__":
    main()
