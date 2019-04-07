import math
import random
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
        self.totalMessagesReceived = []
        self.arrivalInfo = []
        self.state = -1
        self.isListening = True # FOR NOW IT WILL ALWAYS LISTEN
        self.packetSize = 10.
        self.simCycleTime = 0 # offset for simulation time, self.t is bound by [I/2, I], but the simulation time always increases

        # Trickle parameters
        self.Imin = -1 # Minimum length of interval
        self.Imax = -1 # Maximum length of interval
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

    # Check if when we are at time t, the node has an update to transmit
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

    # Trickle step 4
    def does_node_need_to_transmit(self, time):

        if len(self.arrivalInfo) == 0: return

        if self.arrivalInfo[0]['time'] > time: return # The node cannot transmit until it has received the update first

        # if the time is not t, do not transmit
        if time != (self.t + self.simCycleTime): return

        # clear current messages
        # TODO: WE CANNOT CLEAR THIS HERE BECAUSE WE WILL LOSE TRANSMISSIONS
        self.arrivalInfo = []
        print(str(time) + ' = ' + str(self.t) + ' + ' + str(self.simCycleTime))
       
        # if c is not lesser than k, do not transmit    
        if self.c >= self.k: return

        # Else transmit
        self.transmit_state_to_neighbors(time)

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
    
    """
            The Trickle algorithm has six rules:

    1.  When the algorithm starts execution, it sets I to a value in the
        range of [Imin, Imax] -- that is, greater than or equal to Imin
        and less than or equal to Imax.  The algorithm then begins the
        first interval.

    2.  When an interval begins, Trickle resets c to 0 and sets t to a
        random point in the interval, taken from the range [I/2, I), that
        is, values greater than or equal to I/2 and less than I.  The
        interval ends at I.

    3.  Whenever Trickle hears a transmission that is "consistent", it
        increments the counter c.

    4.  At time t, Trickle transmits if and only if the counter c is less
        than the redundancy constant k.

    5.  When the interval I expires, Trickle doubles the interval length.
        If this new interval length would be longer than the time
        specified by Imax, Trickle sets the interval length I to be the
        time specified by Imax.

    6.  If Trickle hears a transmission that is "inconsistent" and I is
        greater than Imin, it resets the Trickle timer.  To reset the
        timer, Trickle sets I to Imin and starts a new interval as in
        step 2.  If I is equal to Imin when Trickle hears an
        "inconsistent" transmission, Trickle does nothing.  Trickle can
        also reset its timer in response to external "events".
    """

    def configure_trickle_parameters(self, Imin, Imax, k):

        self.Imin = Imin # Minimum length of interval

        """
        Taken from: https://tools.ietf.org/html/rfc6206#section-3
            The maximum interval size, Imax, is described as a number of
            doublings of the minimum interval size (the base-2 log(max/min)).
            For example, a protocol might define Imax as 16.  If the minimum
            interval is 100 ms, then the amount of time specified by Imax is
            100 ms * 65,536, i.e., 6,553.6 seconds or approximately
            109 minutes.
        """

        # TODO: Double check validity of this
        self.Imax = Imax#math.log(2, Imax/Imin) # Maximum length of interval

        self.k = k # Redundancy k

    def start_listen(self):
        # Listen period
        self.isListening = True
        return

    def stop_listen(self):
        # Stop listening
        self.isListening = False
        return

    # Trickle step 1
    def start_trickle_algorithm(self, currentSimTime):

        # Set I to a value in the range of Imin, Imax
        # Usually on first iteration, I is set to Imin
        if self.I == -1:
            self.I = self.Imin

        self.begin_new_interval(currentSimTime)

    # Trickle step 2
    def begin_new_interval(self, currentSimTime):

        # Reset counter to 0
        self.c = 0

        # Set t to a random point in the interval [I/2, I)
        self.t = random.randint(self.I // 2, self.I) # randint picks values from lowerbound to upperbound - 1

        self.simCycleTime = currentSimTime # offset for the simulation time

    def queue_received_state(self, nodeF, state, time):
        # If this is a new state, update to the new state and possibly transmit to other nodes
        self.totalMessagesReceived.append({ 'node': nodeF, 'time': time, 'state': state })
        self.arrivalInfo.append({ 'node': nodeF, 'time': time, 'state': state })

    def update_state(self, time):
        
        for arrival in self.arrivalInfo:
            if arrival['time'] == time:

                # Trickle step 3
                if self.state == arrival['state']:
                    self.c += 1 # if a "consistent" transmission is heard, increment the counter
                    print('Incremented counter for ' + str(self.nid) + ' To: ' + str(self.c))
                    return

                # Trickle step 6
                elif self.state != arrival['state']:    

                    # Update state
                    self.state = arrival['state']

                    if self.I > self.Imin:
                        # Reset the trickle timer and start a new interval
                        self.reset_trickle_timer(time)
                        print(str(self.nid) + ' reset timer')

    # Trickle step 4
    def transmit_state_to_neighbors(self, previousTime):
        
        for node in self.nodeList:

            # Calculate time for the next neighbor to update
            time = self.calculate_propagation_time(self.position, node.position)
            # Because this is precomputed, add the last iterations time to this one
            time += previousTime
            print('TIME ' + self.nid + ' ' + node.nid + ' '+ str(time) + ' ' + str(self.distance_between_2_points(self.position, node.position)))
            
            node.queue_received_state(self, self.state, time)
        return


    def has_interval_expired(self, simTime):
        if (self.I + self.simCycleTime) <= simTime:
            self.handle_interval_expired(simTime)
        return    

    # Trickle step 5
    def handle_interval_expired(self, simTime):

            # Update simulation time
            self.simCycleTime = simTime

            # The interval I has expired, double the interval
            self.I *= 2

            # If I exceeds Imax, set it to Imax
            if self.I > self.Imax:
                self.I = self.Imax

    def reset_trickle_timer(self, currentSimTime):

        self.I = self.Imin
        self.begin_new_interval(currentSimTime)

        