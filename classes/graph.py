from .graphics import *
import math

class Graph:

    def __init__(self):

        # Default init parameters
        self.nodeList = []
        self.window = GraphWin(width = 1000, height = 1000) # create a window
        self.window.setCoords(-5, -5, 15, 15) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
        self.radius = 0.2


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



        for node in self.nodeList:
            circle = Circle(Point(node.position['x'], node.position['y']),self.radius)
            #circle.setFill('black')
            circle.draw(self.window)
            circle = Circle(Point(node.position['x'],node.position['y']), node.listenRange)
            circle.setOutline('silver')
            circle.draw(self.window)
            text = Text(Point(node.position['x'] + 0*self.radius, node.position['y']+ 0*self.radius), node.nid)
            text.draw(self.window)
            for adj_node in node.get_node_list():
                self.draw_line(node, adj_node, 'silver')

        self.window.getMouse() # pause before closing
