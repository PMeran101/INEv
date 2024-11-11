#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:43:03 2021

@author: samira
"""
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import argparse

# input should contain name of -i files, -box showBoxes as boolean, -x -y x and y axis, -l labels, -o outputname
# read schema from first line of input files and throw exception if input files don't have the same schema

def main():
    parser = argparse.ArgumentParser(description='Generate Plots')
    myargs = myparse_args(parser)
    mydata = []
    
    if len(myargs.labels) != len(myargs.inputs):
        print("Number of input paths and labels must be the same.")
        return 
    
    if myargs.colors and len(myargs.colors) != len(myargs.labels):
        print("Number of colors must match number of labels.")
        return
    
    if myargs.styles and len(myargs.styles) != len(myargs.labels):
        print("Number of styles must match number of labels.")
        return

    if myargs.legend_labels and len(myargs.legend_labels) != len(myargs.inputs):
        print("Number of legend labels must match the number of input files.")
        return

    
    labels = myargs.labels
    colors = myargs.colors if myargs.colors else ['b'] * len(labels)
    styles = myargs.styles if myargs.styles else ['-'] * len(labels)
    legend_labels = myargs.legend_labels if myargs.legend_labels else [f"{labels[i]} - {y_col}" for i in range(len(labels)) for y_col in myargs.yC]
    
    mycolumns = list(pd.read_csv(myargs.inputs[0]).columns)
    
    for path in myargs.inputs: # schemas are equal or overlap
        df = pd.read_csv(path)
        mycolumns = list(set(mycolumns).intersection(set(list(df.columns))))
        mydata.append(df)
        
    df1 = mydata[0]
    
    # Use specified column names for x and y axis
    if not mycolumns:
        print("Mismatch of schemas")
        return
    
    if myargs.xC in list(mycolumns):
        X_Column = myargs.xC
    else: 
        print("Wrong Column Name")
        print("Schema " + str(mycolumns))
        return
        
    if myargs.yC in list(mycolumns):
        Y_Column = myargs.yC
    else: 
        print("Wrong Column Name")
        print("Schema " + str(mycolumns))
        return
    
    plt.figure(figsize=(12, 6))
    plt.rcParams.update({'font.size':17})
    plt.xlabel(myargs.x_label)
    plt.ylabel(myargs.y_label)
    plt.ylim(0, 1.05)
    plt.yticks(np.linspace(0, 1, 11))

    # Arrange x-ticks
    myX_o = sorted(list(set(df1[X_Column].tolist()))) 
    myX = range(0, len(myX_o)) # counting of x ticks
    legend_index = 0
    for i in range(len(mydata)):
        y_data = mydata[i].groupby(X_Column)[Y_Column].median().to_numpy()
        myX = myX[:len(y_data)]
        plt.plot(myX, y_data, marker="x", label=legend_labels[legend_index], color=colors[i], linestyle=styles[i])
        legend_index += 1

    plt.legend()
    
    if myargs.boxplot:
        # Group values by x value to get list of values for each box plot
        for i in mydata:
            listT = i.groupby(X_Column)[Y_Column].apply(list)
            dfBox = listT.reset_index(name="Lists")
            myLists = list(dfBox["Lists"])
            plt.boxplot(myLists, positions=myX, manage_ticks=False)
    
    plt.xticks(myX, myX_o)    
    plt.savefig("figs/" + str(myargs.outname), format='pdf', bbox_inches='tight')

def myparse_args(parser):
    parser.add_argument('-i', '--inputs', nargs='+', help='input files', required=True)
    parser.add_argument('-l', '--labels', nargs='+', required=True, help='Labels for each line')
    parser.add_argument('-c', '--colors', nargs='+', required=False, help='Colors for each label')
    parser.add_argument('-s', '--styles', nargs='+', required=False, help='Line styles for each label (e.g., "-", "--", "-.", ":")')
    parser.add_argument('-x', '--xC', help='x axis identifier', required=True)
    parser.add_argument('-y', '--yC', help='y axis identifier', required=True)
    parser.add_argument('-legend_labels', nargs='+', required=False, help='Custom labels for each line in the legend')
    parser.add_argument('-box', '--boxplot', action='store_true', required=False, default=False,
                        help='Include boxplots in the graph')
    parser.add_argument('-o', '--outname', required=False, default="plot", help='Output file name')
    parser.add_argument('--x_label', required=False, help='Custom label for the X-axis')
    parser.add_argument('--y_label', required=False, help='Custom label for the Y-axis')
    return parser.parse_args()
    
if __name__ == "__main__":
    main()
