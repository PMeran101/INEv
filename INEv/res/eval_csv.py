import argparse
import pandas as pd

def evaluate_csv(csv_file):
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Ensure the columns exist
    if 'Total Transmissions' not in df.columns or 'Total Savings' not in df.columns:
        print("Error: CSV file must contain 'Total Transmissions' and 'Total Savings' columns.")
        return

    # Initialize a list to store savings percentages
    savings_percentages = []
    
    # Iterate over each row and calculate the savings percentage
    for index, row in df.iterrows():
        total_transmissions = row['Total Transmissions']  # Without optimization
        total_savings = row['Total Savings']  # With optimization
        
        # Avoid division by zero
        if total_transmissions == 0:
            savings_percentage = 0.0
        else:
            # Calculate savings percentage for this row
            savings_percentage = ((total_transmissions - total_savings) / total_transmissions) * 100
        
        # Store the percentage for later averaging
        savings_percentages.append(savings_percentage)
    
    # Calculate the average savings percentage
    if len(savings_percentages) > 0:
        average_savings_percentage = sum(savings_percentages) / len(savings_percentages)
    else:
        average_savings_percentage = 0.0

    # Print results
    print(f"Max Potential Savings: {max(savings_percentages):.2f}%")
    print(f"Average Saving Potential: {average_savings_percentage:.2f}%")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Evaluate the CSV file')
    parser.add_argument('--csv_file','-cf', type=str, help='The CSV file to evaluate', required=True)
    return parser.parse_args()

def main():
    args = parse_arguments()
    csv_file = args.csv_file
    evaluate_csv(csv_file)

if __name__ == '__main__':
    main()
