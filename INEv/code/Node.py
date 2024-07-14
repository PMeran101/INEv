


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
        
    
    def __str__(self):
        return (f"Node {self.id}\n"
                f"Computational Power: {self.computational_power}\n"
                f"Memory: {self.memory}\n"
                f"Eventrates: {self.eventrates}")
        
        