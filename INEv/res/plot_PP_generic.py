#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:43:03 2021

@author: samira
Modified by Assistant on [Current Date]
"""

import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Generate Plots')
    myargs = myparse_args(parser)
    mydata = []
    
    if len(myargs.labels) != len(myargs.inputs):
        print("Number of input paths and labels must be the same.")
        return
    
    if myargs.colors and len(myargs.colors) != len(myargs.inputs) * len(myargs.yC):
        print("Number of colors must match the total number of input file and Y column combinations.")
        return
    
    if myargs.styles and len(myargs.styles) != len(myargs.inputs) * len(myargs.yC):
        print("Number of styles must match the total number of input file and Y column combinations.")
        return
    
    if myargs.legend_labels and len(myargs.legend_labels) != len(myargs.inputs) * len(myargs.yC):
        print("Number of legend labels must match the total number of input file and Y column combinations.")
        return
    
    labels = myargs.labels
    colors = myargs.colors if myargs.colors else ['b'] * (len(labels) * len(myargs.yC))
    styles = myargs.styles if myargs.styles else ['-'] * (len(labels) * len(myargs.yC))
    legend_labels = myargs.legend_labels if myargs.legend_labels else [f"{labels[i]} - {y_col}" for i in range(len(labels)) for y_col in myargs.yC]
    Y_Columns = myargs.yC  # Accept multiple Y columns

    # Read the data and find common columns across all files
    mycolumns = list(pd.read_csv(myargs.inputs[0]).columns)
    for path in myargs.inputs:
        df = pd.read_csv(path)
        mycolumns = list(set(mycolumns).intersection(set(df.columns)))
        mydata.append(df)
        
    if not mycolumns:
        print("Mismatch of schemas among input files.")
        return
    
    # Validate X_Column
    if myargs.xC in mycolumns:
        X_Column = myargs.xC
    else: 
        print(f"X-axis column '{myargs.xC}' not found in the data.")
        print("Available columns: " + ", ".join(mycolumns))
        return
    
    # Validate Y_Columns
    for y_col in Y_Columns:
        if y_col not in mycolumns:
            print(f"Y-axis column '{y_col}' not found in the data.")
            print("Available columns: " + ", ".join(mycolumns))
            return
    
    plt.rcParams.update({'font.size': 17})
    
        # Create the figure with scaled size
    fig, ax = plt.subplots(figsize=(12,6))

    # Update font size globally
    plt.rcParams.update({'font.size': 20})
    
    plt.xlabel(myargs.x_label if myargs.x_label else X_Column, fontsize=25)  # Use custom x-axis label if provided
    plt.ylabel(myargs.y_label if myargs.y_label else "Transmission Ratio",fontsize=25)  # Use custom y-axis label if provided

    # Arrange X-ticks
    df1 = mydata[0]
    myX_o = sorted(list(set(df1[X_Column].tolist())))
    myX = range(len(myX_o))  # Positions for X-ticks
    
    # Plot data with specific colors, styles, and legend labels
    legend_index = 0
    for i in range(len(mydata)):
        df = mydata[i]
        for j, y_col in enumerate(Y_Columns):
            y_data = df.groupby(X_Column)[y_col].median().reindex(myX_o).to_numpy()
            color = colors[i * len(Y_Columns) + j]
            style = styles[i * len(Y_Columns) + j]
            label = legend_labels[legend_index]
            legend_index += 1
            
            # Plot each line
            line, = plt.plot(myX, y_data, marker='x',label=label, color=color, linestyle='-' if style == 'loosely dashed' else style)
            
            # Apply custom dashes if 'loosely dashed'
            if style == 'loosely dashed':
                line.set_dashes([10, 5])  # 10 points on, 5 points off for loosely dashed
    
    # Place the legend on top of the plot
    plt.legend(
         loc='upper center', 
         bbox_to_anchor=(0.5, 1.32), 
         ncol=len(labels), 
         borderaxespad=0., 
         frameon=True
     )
    #plt.legend()

    # Rotate X-axis labels to avoid overlap
    plt.xticks(myX, myX_o, ha='right',fontsize=23)
    plt.yticks(np.arange(0, 1.1, 0.1),fontsize=23)
    
    if myargs.boxplot:
        # Add boxplots for each Y column
        for y_col in Y_Columns:
            list_of_lists = []
            for x_value in myX_o:
                data_at_x = []
                for df in mydata:
                    data_at_x.extend(df[df[X_Column] == x_value][y_col].tolist())
                list_of_lists.append(data_at_x)
            plt.boxplot(list_of_lists, positions=myX, manage_ticks=False)
    
    plt.savefig(str(myargs.outname), format='svg', bbox_inches='tight')

def myparse_args(parser):
    parser.add_argument('-i', '--inputs', nargs='+', help='Input CSV file paths', required=True)
    parser.add_argument('-l', '--labels', nargs='+', help='Labels for input files', required=True)
    parser.add_argument('-x', '--xC', help='X-axis column name', required=True)
    parser.add_argument('-y', '--yC', nargs='+', help='Y-axis column name(s)', required=True)
    parser.add_argument('-c', '--colors', nargs='+', required=False, help='Colors for each (input file, Y column) combination')
    parser.add_argument('-s', '--styles', nargs='+', required=False, help='Line styles for each (input file, Y column) combination (e.g., "-", "--", "-.", ":", "loosely dashed")')
    parser.add_argument('-legend_labels', nargs='+', required=False, help='Custom labels for each line in the legend')
    parser.add_argument('-box', '--boxplot', action='store_true', required=False, default=False,
                        help='Include boxplots in the graph')
    parser.add_argument('-o', '--outname', required=False, default="plot", help='Output file name')
    parser.add_argument('--x_label', required=False, help='Custom label for the X-axis')
    parser.add_argument('--y_label', required=False, help='Custom label for the Y-axis')
    return parser.parse_args()
         
if __name__ == "__main__":
    main()
