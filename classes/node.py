import math
from .graphics import *
from time import sleep

class Node:

    def __init__(self, source, nid, position, listenRange):

        # User defined parameters
        self.nid = nid # node id
        self.position = position
        self.listenRange = listenRange
        self.graph = source

        # Default init parameters
        self.nodeList = []
        self.arrivalPacket = []
        self.arrivalTime = []
        self.arrivalSize = []
        self.state = -1
        self.isListening = True # FOR NOW IT WILL ALWAYS LISTEN

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
    def start_listen(self):
        # Listen period
        self.isListening = True
        return

    def stop_listen(self):
        # Stop listening
        self.isListening = False
        return    

    def update_state(self, state):
        
        # If this is a new state, update to the new state and transmit to other nodes
        if self.state != state:
            self.state = state
            self.transmit_state_to_neighbors()
        else: return

    def transmit_state_to_neighbors(self):
        for node in self.nodeList:
            node.update_state(self.state)
        for thing in self.nodeList:
            circle = Circle(Point(thing.position['x'], thing.position['y']),self.graph.radius)
            circle.draw(self.graph.window)
            circle.setFill('green')
            self.graph.draw_line(self, thing)
            sleep(1)
        return