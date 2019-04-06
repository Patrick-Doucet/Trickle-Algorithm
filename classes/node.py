import math
import numpy as np
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
        self.arrivalInfo = []
        self.state = -1
        self.isListening = True # FOR NOW IT WILL ALWAYS LISTEN
        self.packetSize = 10.

        # Trickle parameters
        self.Imin = -1 # Minimum length of interval
        self.Imax = -1 # Minimum length of interval
        self.k = -1 # Redundancy k
        self.I = -1 # Length of current interval
        self.t = -1 # Random time t inside [I/2, I]
        self.c = -1 # Consistant message counter

    ##########################################################
    #                    Simulation methods                  #
    ##########################################################

    def get_node_list(self):
        return self.nodeList

    # Iterate through all the nodes of the graph and add the ones in the node's range to its nodeList
    def update_node_list(self, allNodes):

        self.nodeList = [] # Clear node list

        # Repopulate node list
        for node in allNodes:

            # If the node is different than self and its position is in range, add it to self.nodeList
            if node.nid != self.nid:
                if(self.is_in_range(node)):
                    self.nodeList.append(node)

        return

    # Check if at a certain time, the node had received an update
    def has_node_updated_at_time(self, time):

        updateList = []

        if len(self.arrivalInfo) == 0:
            return updateList

        def sortFun(x):
            return x['time']

        self.arrivalInfo.sort(key=sortFun)

        timestamp = self.arrivalInfo[0]['time'] #for now
        stateAtTimestamp = self.arrivalInfo[0]['state']
        nodeF = self.arrivalInfo[0]['node']
        if time == timestamp:
            updateList.append({ 'timestamp': timestamp, 'state': stateAtTimestamp, 'node' : nodeF})

        return updateList


    # Return distance between 2 points
    def distance_between_2_points(self, point1, point2):
        return math.sqrt(math.pow(point2['x'] - point1['x'], 2) + math.pow(point2['y'] - point1['y'], 2))

    # Returns True or False, checking if the given node is in the range of this node
    def is_in_range(self, nextNode):
        return self.distance_between_2_points(self.position, nextNode.position) <= self.listenRange

    def calculate_propagation_time(self, point1, point2):
        distance = self.distance_between_2_points(point1, point2)
        bandwidth = 0.1
        transmissionPower = 1000
        alpha = 2
        noise = 1

        transmissionRate = bandwidth * math.log(1 + (transmissionPower / (math.pow(distance, alpha) * noise)))
        propagationTime = self.packetSize/transmissionRate
        # Normalize to integers
        normalizedPropagationTime = math.ceil(propagationTime)
        return normalizedPropagationTime


    ##########################################################
    #                    Trickle methods                     #
    ##########################################################

    def configure_trickle_parameters(self, Imin, Imax, k):
        self.Imin = Imin # Minimum length of interval
        self.Imax = Imax # Minimum length of interval
        self.k = k # Redundancy k

    def start_listen(self):
        # Listen period
        self.isListening = True
        return

    def stop_listen(self):
        # Stop listening
        self.isListening = False
        return

    def update_state(self, nodeF, state, time):
        # If this is a new state, update to the new state and transmit to other nodes

        self.arrivalInfo.append({'node':nodeF,'time':time,'state':state})

        if self.state != state:
            # Logical update
            self.state = state
            self.transmit_state_to_neighbors(time)
        else: return

    def transmit_state_to_neighbors(self, previousTime):
        for node in self.nodeList:

            # Calculate time for the next neighbor to update
            time = self.calculate_propagation_time(self.position, node.position)
            print('TIME ' + self.nid + ' ' + node.nid + ' '+ str(time) + ' ' + str(self.distance_between_2_points(self.position, node.position)))
            # Because this is precomputed, add the last iterations time to this one
            time += previousTime
            node.update_state(self, self.state, time)
        return
