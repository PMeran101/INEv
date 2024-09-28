import Node
import pickle

def print_network_tree():
    
    with open('network', 'rb') as nw_file:
        nw = pickle.load(nw_file)
        
        root = nw[0]
    
    print(root)
    
    root.visualize_tree(root)
    
    

print_network_tree()