#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 23:21:43 2022

@author: samira
"""

from tree import *
import random as rd
import sys
import pickle
from binary_helper import save_file, load_file


def main():
    
    nw = load_file('original_network')

    wl_windows = load_file('wl_windows')

    wl = load_file('original_wl')
        
        
    query_index = 1

    if len(sys.argv) > 1: 
      query_index = int(sys.argv[1])      
    
    # overwrite current rates + current query workload  
    myquery_window = wl_windows[query_index][1]
    for i in range(len(nw)):  
        for rate in range(len(nw[i])):
            nw[i][rate] = myquery_window * nw[i][rate]
            
    wl = [wl[query_index]] # original_wl
        
    print(wl)
    
    save_file('network', nw)

    save_file('current_wl',wl) 


if __name__ == "__main__":
    main()        