import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_percentile_bars(input_files, y_column, x_column, labels, output_file, colors=None, x_label=None, y_label=None, legend_title="Data Sets"):
    """
    Generates a bar graph where for each unique x-axis point, the bar represents the range
    from the 10th percentile to the 90th percentile of the y_column values.
    Whiskers show the outliers (minimum to 10th percentile and 90th percentile to maximum).
    Allows customization of figure size, axis labels, and legend title.

    Parameters:
    - input_files: List of CSV file paths.
    - y_column: Name of the y-axis column in the CSV files.
    - x_column: Name of the x-axis column in the CSV files.
    - labels: List of labels corresponding to each CSV file.
    - output_file: Path to save the output plot.
    - colors: List of colors for the bars (optional).
    - x_label: Custom x-axis label (optional).
    - y_label: Custom y-axis label (optional).
    - legend_title: Custom title for the legend (optional).
    """
    # Check that the number of input files and labels match
    if len(input_files) != len(labels):
        raise ValueError("The number of input files and labels must be the same.")
    if colors and len(colors) != len(labels):
        raise ValueError("The number of colors must match the number of input files and labels.")

    # Set default colors if not provided
    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Dictionary to hold data for each (x_point, label)
    data_dict = {}

    # Collect data from each file
    for idx, file in enumerate(input_files):
        label = labels[idx]
        df = pd.read_csv(file)

        # Group data by x_column
        grouped = df.groupby(x_column)[y_column]

        for x_point, group in grouped:
            key = (x_point, label)
            # Calculate percentiles and min/max
            p10 = np.percentile(group, 10)
            p90 = np.percentile(group, 90)
            min_value = group.min()
            max_value = group.max()
            data_dict[key] = {'p10': p10, 'p90': p90, 'min': min_value, 'max': max_value}

    # Get sorted unique x-axis points
    x_points = sorted(set([key[0] for key in data_dict.keys()]))
    n_labels = len(labels)

    # Prepare data for plotting
    bar_positions = []
    bar_heights = []
    bar_bottoms = []
    lower_whisker = []
    upper_whisker = []
    bar_labels = []

    # Width of each bar group and individual bars
    total_width = 0.8
    bar_width = total_width / n_labels

    # Positions for each group of bars
    positions = np.arange(len(x_points))

    # Adjust font size for consistency
    plt.rcParams.update({'font.size': 17})

    for i, label in enumerate(labels):
        positions_i = positions - total_width/2 + bar_width/2 + i*bar_width
        bar_positions.extend(positions_i)
        bar_labels.extend([str(x) for x in x_points])

        heights = []
        bottoms = []
        err_lower = []
        err_upper = []

        for x_point in x_points:
            key = (x_point, label)
            if key in data_dict:
                p10 = data_dict[key]['p10']
                p90 = data_dict[key]['p90']
                min_value = data_dict[key]['min']
                max_value = data_dict[key]['max']
                bar_height = p90 - p10

                # Handle zero bar height
                if round(bar_height,2) == 0.0:
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
    for i in range(n_labels):
        idx_start = 0
        idx_end = len(x_points)

        x_pos = bar_positions[i*len(x_points):(i+1)*len(x_points)]
        heights = bar_heights[i]
        bottoms = bar_bottoms[i]
        lower_whiskers = lower_whisker[i]
        upper_whiskers = upper_whisker[i]

        # Plot bars
        ax.bar(
            x_pos,
            heights,
            width=bar_width,
            bottom=bottoms,
            label=labels[i],
            align='center',
            zorder=2,
            color=colors[i % len(colors)]
        )

        # Plot whiskers
        for j in range(len(x_pos)):
            if not np.isnan(bottoms[j]):
                # Lower whisker
                if lower_whiskers[j] is not None:
                    ax.vlines(
                        x_pos[j],
                        bottoms[j] - lower_whiskers[j],
                        bottoms[j],
                        color='black',
                        linestyle='-',
                        zorder=3
                    )
                    # Add cap
                    ax.hlines(
                        bottoms[j] - lower_whiskers[j],
                        x_pos[j] - capwidth / 2,
                        x_pos[j] + capwidth / 2,
                        color='black',
                        zorder=3
                    )
                # Upper whisker
                if upper_whiskers[j] is not None:
                    ax.vlines(
                        x_pos[j],
                        bottoms[j] + heights[j],
                        bottoms[j] + heights[j] + upper_whiskers[j],
                        color='black',
                        linestyle='-',
                        zorder=3
                    )
                    # Add cap
                    ax.hlines(
                        bottoms[j] + heights[j] + upper_whiskers[j],
                        x_pos[j] - capwidth / 2,
                        x_pos[j] + capwidth / 2,
                        color='black',
                        zorder=3
                    )
                # If both whiskers are None and bar height is minimal, plot a marker
                if lower_whiskers[j] is None and upper_whiskers[j] is None and heights[j] == minimal_height:
                    ax.plot(
                        x_pos[j],
                        bottoms[j] + heights[j] / 2,
                        marker='o',
                        color='black',
                        zorder=4
                    )

    # Set y-axis range from 0 to 1 with appropriate steps
    ax.set_ylim(0, 1.05)
    ax.set_yticks(np.linspace(0, 1, 11))  # Set ticks at intervals of 0.1
    ax.set_yticklabels([f"{y:.1f}" for y in np.linspace(0, 1, 11)], fontsize=23)

    # Set x-axis labels
    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in x_points],fontsize=23)

    plt.xlabel(x_label if x_label else x_column, fontsize=25)
    plt.ylabel(y_label if y_label else y_column,fontsize=25)
    # plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_file, format='svg', bbox_inches='tight')
    plt.close()
    print(f"Plot saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot a bar graph with 80% range bars and outliers.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="Input CSV files.")
    parser.add_argument('-y', '--y_column', required=True, help="Y-axis column name.")
    parser.add_argument('-x', '--x_column', required=True, help="X-axis column name.")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the input files.")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the plot.")
    parser.add_argument('-c', '--colors', nargs='+', help="Colors for the bars (optional).")
    parser.add_argument('--x_label', help="Custom x-axis label (optional).")
    parser.add_argument('--y_label', help="Custom y-axis label (optional).")
    parser.add_argument('--legend_title', default="Legend", help="Title for the legend (optional).")

    args = parser.parse_args()

    # Call the plotting function
    plot_percentile_bars(
        args.input_files,
        args.y_column,
        args.x_column,
        args.labels,
        args.output_file,
        colors=args.colors,
        x_label=args.x_label,
        y_label=args.y_label,
        legend_title=args.legend_title
    )

if __name__ == "__main__":
    main()
