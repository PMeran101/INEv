import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create a dual Y-axis plot with a line graph and box plots.")
parser.add_argument('--input', required=True, help="Path to the input CSV file.")
parser.add_argument('--output', required=True, help="Path to save the output plot (e.g., output.pdf).")
parser.add_argument('--x', required=True, help="Column name for the X-axis.")
parser.add_argument('--y1', required=True, help="Column name for the first Y-axis (line graph).")
parser.add_argument('--y2', required=True, help="Column name for the second Y-axis (box plot).")
parser.add_argument('--xlabel', required=True, help="Label for the X-axis.")
parser.add_argument('--y1label', required=True, help="Label for the first Y-axis.")
parser.add_argument('--y2label', required=True, help="Label for the second Y-axis.")
parser.add_argument('--title', required=True, help="Title of the plot.")
args = parser.parse_args()

# Load the CSV file
data = pd.read_csv(args.input)

# Ensure columns exist
if args.x not in data.columns or args.y1 not in data.columns or args.y2 not in data.columns:
    raise ValueError(f"One or more specified columns ({args.x}, {args.y1}, {args.y2}) are not in the CSV file.")

# Group data by the X-axis for box plots
x_unique = sorted(data[args.x].unique())
grouped_data = [data.loc[data[args.x] == x_val, args.y2].to_numpy() for x_val in x_unique]

# Prepare Y1 values for the line graph
x_line = np.array(x_unique)  # Unique sorted X-axis values
y1_mean = data.groupby(args.x)[args.y1].mean().loc[x_line].to_numpy()  # Mean Y1 for line graph

# Create the plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot the line graph (Y1)
ax1.plot(x_line, y1_mean, color='blue', label=args.y1label, marker='o')
ax1.set_xlabel(args.xlabel)
ax1.set_ylabel(args.y1label, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')

# Plot the box plots (Y2)
ax2 = ax1.twinx()
ax2.boxplot(grouped_data, positions=x_unique, widths=0.4, patch_artist=True,
            boxprops=dict(facecolor="orange", alpha=0.6))
ax2.set_ylabel(args.y2label, color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Add title and grid
plt.title(args.title)
ax1.grid(True)

# Save and show the plot
plt.tight_layout()
plt.savefig(args.output, format='pdf')
plt.show()
