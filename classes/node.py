import math

class Node:

    def __init__(self, nid, position, listenRange):
        
        # User defined parameters
        self.nid = nid # node id
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
        return self.nodeList
    
    def update_node_list(self, allNodes):

        self.nodeList = [] # Clear node list

        # Repopulate node list
        for node in allNodes:

            # If the node is different than self and its position is in range, add it to self.nodeList
            if node.nid != self.nid:
                if(self.is_in_range(node)):
                    self.nodeList.append(node)

        return

    # Return distance between 2 points
    def distance_between_2_points(self, point1, point2):
        return math.sqrt(math.pow(point2['x'] - point1['x'], 2) + math.pow(point2['y'] - point1['y'], 2))

    # Returns True or False, checking if the given node is in the range of this node
    def is_in_range(self, nextNode):
        return self.distance_between_2_points(self.position, nextNode.position) <= self.listenRange

    # Trickle methods
    def listen(self):
        return

    def update(self, state):
        return

    def transmit(self, nodeList):
        return
    