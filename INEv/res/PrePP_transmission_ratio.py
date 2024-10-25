"""
Script to add a Transmission Ratio for the PrePP compared to the INEv and Compared to Central Fog
"""

import pandas as pd
import argparse

def load_args():
    parser = argparse.ArgumentParser(description='Calculate Transmission Ratios and update CSV file.')
    parser.add_argument('--input_file', help='Path to the input CSV file')
    return parser.parse_args()

def main():
    args = load_args()
    input_file = args.input_file

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_file}' is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: The file '{input_file}' is not a valid CSV.")
        return

    # Ensure required columns are present
    required_columns = ['Transmission', 'INEvTransmission', 'exact_costs']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
        return

    # Convert relevant columns to numeric, coerce errors to NaN
    for col in required_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate TransmissionRatioINEv (exact_costs / INEvTransmission)
    df['TransmissionRatioINEv'] = df['exact_costs'] / df['INEvTransmission']

    # Calculate TransmissionRatioCentral (exact_costs / Transmission)
    df['TransmissionRatioCentral'] = df['exact_costs'] / df['Transmission']

    # Handle division by zero or infinite values by replacing them with NaN
    df.replace([float('inf'), -float('inf')], pd.NA, inplace=True)

    # Append the new columns to the DataFrame
    # (They are already appended by the assignment operations above)

    # Save the updated DataFrame back to the same CSV file
    try:
        df.to_csv(input_file, index=False)
        print(f"Updated file saved successfully: {input_file}")
    except Exception as e:
        print(f"Error: Could not write to file '{input_file}'. {e}")

if __name__ == '__main__':
    main()
