
from graphviz import Digraph

class Node():
    
    id = 0
    computational_power = 0
    memory = 0
    eventrates = [] 
    
    
    def __init__(self, id:int ,compute_power: int, memore: int):
        self.id = id
        self.computational_power = compute_power
        self.memory = memore
        self.eventrates = []
        self.Parent = None
        self.Child = None
        self.Sibling = None
        
    

    def __str__(self):
        parent_id = self.Parent.id if self.Parent else None
        child_id = self.Child.id if self.Child else None
        sibling_id = self.Sibling.id if self.Sibling else None
        return (f"Node {self.id}\n"
                f"Computational Power: {self.computational_power}\n"
                f"Memory: {self.memory}\n"
                f"Eventrates: {self.eventrates}\n"
                f"Parent: {parent_id}\n"
                f"Child: {child_id}\n"
                f"Sibling: {sibling_id}\n")

    def add_nodes_edges(self,node, dot=None, nodes=set(), edges=set()):
        if dot is None:
            dot = Digraph()

        if node.id not in nodes:
            dot.node(name=str(node.id), label=str(node.id))
            nodes.add(node.id)

        if node.Child is not None:
            if (node.id, node.Child.id) not in edges:
                dot.node(name=str(node.Child.id), label=str(node.Child.id))
                dot.edge(str(node.id), str(node.Child.id))
                edges.add((node.id, node.Child.id))
            self.add_nodes_edges(node.Child, dot, nodes, edges)
        
        sibling = node.Sibling
        while sibling is not None:
            if sibling.id not in nodes:
                dot.node(name=str(sibling.id), label=str(sibling.id))
                nodes.add(sibling.id)
            if (node.Parent.id, sibling.id) not in edges:
                dot.edge(str(node.Parent.id), str(sibling.id))
                edges.add((node.Parent.id, sibling.id))
            self.add_nodes_edges(sibling, dot, nodes, edges)
            sibling = sibling.Sibling

        return dot

    def visualize_tree(self,root):
        dot = self.add_nodes_edges(root)
        dot.render('tree', format='png', view=False)  # Save and view the tree as a PNG image
        
        