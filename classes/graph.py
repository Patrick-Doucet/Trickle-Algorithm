from .graphics import *
import math
import numpy as np
from time import sleep

class Graph:

    def __init__(self, show_range = False):
        self.show_range = show_range
        # Default init parameters
        self.nodeList = []
        self.simulationStartTime = 0
        self.simulationEndTime = 2000
        self.simulationCurrentTime = -1

    # Iterate through the simulation time to graphically show all node updates
    def run_simulation(self, startingNode):

        if(self.simulationCurrentTime < self.simulationStartTime):
            self.simulationCurrentTime = self.simulationStartTime

        max_x = np.max(list(map(lambda x : x.position['x'], self.nodeList))) - self.radius/2
        max_y = np.max(list(map(lambda x : x.position['y'], self.nodeList))) - self.radius/2
        max_total = np.max([max_x, max_y])

        timer = Text(Point(max_total, max_total), 'Time : ' + str(self.simulationCurrentTime))
        timer.draw(self.window)

        # Inject state change to node in graph
        startingNode.queue_received_state(startingNode, 1, 1)

        while self.simulationCurrentTime < self.simulationEndTime:

            updatesToProcess = {}
            for node in self.nodeList:
                # Get list of node update
                nodeUpdates = node.has_node_updated_at_time(self.simulationCurrentTime)
                updatesToProcess[node.nid] = {'node': node, 'updates' : nodeUpdates}

                # Update node if needed
                node.update_state(self.simulationCurrentTime)

                # Attempt to transmit to other nodes
                node.does_node_need_to_transmit(self.simulationCurrentTime)

                # Has the interval I expired?
                node.has_interval_expired(self.simulationCurrentTime)

            for struct in updatesToProcess.values():# Graphical update
                if struct['updates'] != []:
                    node = struct['node']
                    nodeF = struct['updates'][0]['node']
                    arc = Arc(Point(node.position['x'], node.position['y']),node.graph.radius,)
                    arc.setFill('medium sea green')
                    arc.setStart('90')
                    arc.setExtent('180')
                    arc.draw(node.graph.window)
                    if node!=nodeF:
                        self.draw_line(nodeF, node)
                    text = Text(Point(node.position['x'] + 0*node.graph.radius, node.position['y']+ 0*node.graph.radius), node.nid)
                    text.draw(node.graph.window)
                    #sleep(0.25)

            timer.undraw()
            self.window.update()
            timer = Text(Point(max_total, max_total), 'Time : ' + str(self.simulationCurrentTime))
            timer.draw(self.window)

            self.simulationCurrentTime += 1

        self.window.getMouse()

    # Add new node to network graph
    # Force all nodes (including the newly added node) to update their nodeList
    def add_node(self, node):
        self.nodeList.append(node)
        for node in self.nodeList:
            node.update_node_list(self.nodeList)

    def draw_line(self, node, adj_node, color='black'):
        def get_angle(node1, node2):
            return math.atan2(node1.position['y']-node2.position['y'],node1.position['x']-node2.position['x'])

        line = Line(Point(node.position['x'] - self.radius*math.cos(get_angle(node,adj_node)),node.position['y'] - self.radius*math.sin(get_angle(node,adj_node))),Point(adj_node.position['x'] + self.radius*math.cos(get_angle(node,adj_node)),adj_node.position['y'] + self.radius*math.sin(get_angle(node,adj_node))))
        line.setArrow("last")
        line.setFill(color)
        line.draw(self.window)


    def plot(self):
        min_x = np.min(list(map(lambda x : x.position['x'], self.nodeList))) - 5
        max_x = np.max(list(map(lambda x : x.position['x'], self.nodeList))) + 5
        min_y = np.min(list(map(lambda x : x.position['y'], self.nodeList))) - 5
        max_y = np.max(list(map(lambda x : x.position['y'], self.nodeList))) + 5

        range = max(max_x-min_x,max_y-min_y)
        self.radius = range/80

        self.window = GraphWin(width = 1000, height = 1000)
        self.window.setCoords(min_x, min_y, min_x+range, min_y+range)

        for node in self.nodeList:
            circle = Circle(Point(node.position['x'], node.position['y']),self.radius)
            #circle.setFill('black')
            circle.draw(self.window)
            if self.show_range:
                circle = Circle(Point(node.position['x'],node.position['y']), node.listenRange)
                circle.setOutline('silver')
                circle.draw(self.window)
            for adj_node in node.get_node_list():
                self.draw_line(node, adj_node, 'silver')
            text = Text(Point(node.position['x'] + 0*self.radius, node.position['y']+ 0*self.radius), node.nid)
            text.draw(self.window)
        self.window.getMouse() # pause before closing
