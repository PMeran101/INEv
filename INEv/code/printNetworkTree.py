import Node
import pickle
from binary_helper import load_file
def print_network_tree():
    nw = load_file('network')        
    root = nw[0]
    
    print(root)
    
    root.visualize_tree(root)
    
    

print_network_tree()