import math

class Node:

    def __init__(self, position, listenRange):
        
        # User defined parameters
        self.position = position
        self.listenRange = listenRange

        # Default init parameters
        self.nodeList = []
        self.arrivalPacket = []
        self.arrivalTime = []
        self.arrivalSize = []
        self.state = -1

        # Trickle parameters
        self.Imin = -1 # Minimum length of interval
        self.Imax = -1 # Minimum length of interval
        self.k = -1 # Redundancy k
        self.I = -1 # Length of current interval
        self.t = -1 # Random time t inside [I/2, I]
        self.c = -1 # Consistant message counter

    # Simulation methods
    def get_node_list(self):
        return nodeList
    
    def update_node_list(self):
        return

    def distance_between_2_points(self, point1, point2):
        return math.sqrt(math.pow(point2['x'] - point1['x'], 2) + math.pow(point2['y'] - point1['y'], 2))

    def is_in_range(self, point1, point2):
        return self.distance_between_2_points(point1, point2) < self.listenRange

    # Trickle methods
    def listen(self):
        return

    def update(self, state):
        return

    def transmit(self, nodeList):
        return
    