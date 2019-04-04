class Node:
    def __init__(self, position, listenRange):
        
        # User defined parameters
        self.position = position
        self.listenRange = listenRange

        # Default init parameters
        self.arrivalPacket = []
        self.arrivalTime = []
        self.arrivalSize = []
        self.state = -1
        
        

n = Node({2, 3}, 10)

print(n.position)
print(n.listenRange)