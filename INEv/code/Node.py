


class Node():
    
    id = 0
    computational_power = 0
    memory = 0
    eventrates = [] 
    
    
    def __init__(self, id:int ,compute_power: int, memore: int, eventrate: list):
        self.id = id
        self.computational_power = compute_power
        self.memory = memore
        self.eventrates = eventrate
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
        
    # def print_tree(self,root):
    #     stack = [(root, 0)]  # Stack to hold nodes along with their level
    #     while stack:
    #         node, level = stack.pop()
    #         if node is not None:
    #             print(' ' * level * 4 + str(node))
    #             # Push siblings first so that children are processed first
    #             if node.Sibling is not None:
    #                 stack.append((node.Sibling, level))
    #             if node.Child is not None:
    #                 stack.append((node.Child, level + 1))
        
        