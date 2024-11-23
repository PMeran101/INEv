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
    
    labels = myargs.labels
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
    
    plt.rcParams.update({'font.size': 18})
    plt.xlabel(myargs.x_label if myargs.x_label else X_Column,fontsize=25)  # Use custom or default X-axis label
    plt.ylabel(myargs.y_label if myargs.y_label else "Transmission Ratio",fontsize=25)  # Use custom or default Y-axis label

    # Arrange X-ticks
    df1 = mydata[0]
    myX_o = sorted(list(set(df1[X_Column].tolist())))
    myX = range(len(myX_o))  # Positions for X-ticks
    
    # Check for custom legend labels
    legend_labels = myargs.legend_labels if myargs.legend_labels else [f"{label} - {y_col}" for label in labels for y_col in Y_Columns]
    
    if len(legend_labels) != len(labels) * len(Y_Columns):
        print("The number of legend labels must match the total number of input files and Y columns.")
        return

    all_y_data = []
    # Plot data
    legend_index = 0
    for i in range(len(mydata)):
        df = mydata[i]
        for y_col in Y_Columns:
            y_data = df.groupby(X_Column)[y_col].median().reindex(myX_o).to_numpy()
            plt.plot(myX, y_data, marker="x", label=legend_labels[legend_index])
            all_y_data.extend(y_data)
            legend_index += 1
    
    # Place the legend on top of the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.250), ncol=len(labels), borderaxespad=0., frameon=True)

    max_y = max(all_y_data)
    # Rotate X-axis labels to avoid overlap
    plt.xticks(myX, myX_o, rotation=45, ha='right',fontsize=23)
    plt.yticks(np.arange(0, max_y, 250),fontsize=23)
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
    
    plt.savefig("figs/" + str(myargs.outname), format='pdf', bbox_inches='tight')
    # plt.show()

def myparse_args(parser):
    parser.add_argument('-i', '--inputs', nargs='+', help='Input CSV file paths', required=True)
    parser.add_argument('-l', '--labels', nargs='+', help='Labels for input files', required=True)
    parser.add_argument('-x', '--xC', help='X-axis column name', required=True)
    parser.add_argument('-y', '--yC', nargs='+', help='Y-axis column name(s)', required=True)
    parser.add_argument('-box', '--boxplot', action='store_true', required=False, default=False, help='Include boxplots in the graph')
    parser.add_argument('-o', '--outname', required=False, default="plot", help='Output file name')
    parser.add_argument('--x_label', help="Custom label for the x-axis")
    parser.add_argument('--y_label', help="Custom label for the y-axis")
    parser.add_argument('--legend_labels', nargs='+', help="Custom labels for the legend")
    args = parser.parse_args()
    return args
         
if __name__ == "__main__":
    main()
