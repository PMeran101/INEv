
from graphviz import Graph

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
        self.Parent = []
        self.Child = []
        self.Sibling = []
        
    

    def __str__(self):
        parent_ids = [parent.id for parent in self.Parent] if self.Parent else None
        child_ids = [child.id for child in self.Child] if self.Child else None
        sibling_ids = [sibling.id for sibling in self.Sibling] if self.Sibling else None

        return (f"Node {self.id}\n"
                f"Computational Power: {self.computational_power}\n"
                f"Memory: {self.memory}\n"
                f"Eventrates: {self.eventrates}\n"
                f"Parents: {parent_ids}\n"
                f"Child: {child_ids}\n"
                f"Siblings: {sibling_ids}\n")
    def add_nodes_edges(self, node, dot=None, nodes=set(), edges=set()):
        if dot is None:
            dot = Graph()

        # Add the current node if not already added
        if node.id not in nodes:
            dot.node(name=str(node.id), label=str(node.id))
            nodes.add(node.id)

        # Process each child node
        for child in node.Child:
            if child.id not in nodes:
                dot.node(name=str(child.id), label=str(child.id))
                nodes.add(child.id)

            # Add an edge between the current node and its child
            if (node.id, child.id) not in edges:
                dot.edge(str(node.id), str(child.id))
                edges.add((node.id, child.id))

            # Recursively add nodes and edges for the child
            self.add_nodes_edges(child, dot, nodes, edges)

        # Process each sibling node
        for sibling in node.Sibling:
            if sibling.id not in nodes:
                dot.node(name=str(sibling.id), label=str(sibling.id))
                nodes.add(sibling.id)

            # Add an edge between the parent and the sibling
            for parent in node.Parent:
                if (parent.id, sibling.id) not in edges:
                    dot.edge(str(parent.id), str(sibling.id))
                    edges.add((parent.id, sibling.id))

            # Recursively add nodes and edges for the sibling
            self.add_nodes_edges(sibling, dot, nodes, edges)

        return dot

    def visualize_tree(self,root):
        dot = self.add_nodes_edges(root)
        dot.render('tree', format='png', view=False)  # Save and view the tree as a PNG image
        
        