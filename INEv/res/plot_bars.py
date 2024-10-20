import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to generate bar plot
def plot_bar(files, y_column, labels, output_file):
    # Initialize data for the bar plot
    transmission_ratios = []
    
    # Collect the transmission ratio from each file
    for file in files:
        data = pd.read_csv(file)
        transmission_ratio_mean = data[y_column].mean()  # Calculate the mean of TransmissionRatio
        transmission_ratios.append(transmission_ratio_mean)

    # Create bar plot
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size': 17})
    # Create positions for the bars
    # Create positions for the bars (sequential integers starting from 2)
    positions = np.arange(2, len(labels) + 2)
    labels = [int(label.split('_')[1]) for label in labels]
    # Plot bars with the positions aligned with labels
    plt.bar(positions, transmission_ratios, align='center')
    # Plot the trend line connecting the tops of the bars
    plt.plot(positions, transmission_ratios, marker='o', linestyle='-', color='red', label='Trend')

    plt.xlabel('MaxParents')
    plt.ylabel(y_column)
    plt.title(f'{y_column} for Different MaxParents')
    
    # Set x-axis labels and ensure alignment
    plt.xticks(positions, labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.rcParams.update({'font.size':17})
    # Save the figure to a file
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Plot bar graph from CSV files.")
    parser.add_argument('-i', '--input_files', nargs='+', required=True, help="List of input CSV files.")
    parser.add_argument('-y', '--y_column', required=True, help="Column name for y-axis (e.g., TransmissionRatio)")
    parser.add_argument('-l', '--labels', nargs='+', required=True, help="Labels for the files (e.g., MaxParents_2 MaxParents_3)")
    parser.add_argument('-o', '--output_file', required=True, help="Output file for the bar plot")

    args = parser.parse_args()

    # Call the plotting function
    plot_bar(args.input_files, args.y_column, args.labels, args.output_file)

if __name__ == "__main__":
    main()
