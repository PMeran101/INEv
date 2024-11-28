import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create a 2D scatter plot from a CSV file with dynamic inputs.")
parser.add_argument('--input', required=True, help="Path to the input CSV file.")
parser.add_argument('--output', required=True, help="Path to save the output plot (e.g., output.pdf).")
parser.add_argument('--x', required=True, help="Column name for the X-axis.")
parser.add_argument('--y', required=True, help="Column name for the Y-axis.")
parser.add_argument('--color', required=True, help="Column name for color encoding.")
parser.add_argument('--xlabel', required=True, help="Label for the X-axis.")
parser.add_argument('--ylabel', required=True, help="Label for the Y-axis.")
parser.add_argument('--colorlabel', required=True, help="Label for the color bar.")
args = parser.parse_args()

# Load the CSV file
data = pd.read_csv(args.input)

# Extract the relevant columns
x = data[args.x]
y = data[args.y]
color = data[args.color]

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y, c=color, cmap='viridis', s=50, alpha=0.8)

# Add color bar
plt.colorbar(label=args.colorlabel)

# Add labels
plt.xlabel(args.xlabel)
plt.ylabel(args.ylabel)

# Save the plot
plt.tight_layout()
plt.savefig(args.output, format='pdf')
# plt.show()
