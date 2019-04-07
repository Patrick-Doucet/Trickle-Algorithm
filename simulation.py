import classes.node as node
import classes.graph as graph

# Initting test graph
g = graph.Graph()
nA = node.Node(g, 'A', {'x': 0, 'y': 3}, 2)
nB = node.Node(g, 'B', {'x': 1, 'y': 6}, 1)
nC = node.Node(g, 'C', {'x': 2, 'y': 5}, 3)
nD = node.Node(g, 'D', {'x': 5, 'y': 10}, 10)
nE = node.Node(g, 'E', {'x': 0, 'y': 0}, 3)
nF = node.Node(g, 'F', {'x': 3, 'y': 8}, 3)
nG = node.Node(g, 'G', {'x': 4, 'y': 8}, 3)
nH = node.Node(g, 'H', {'x': 3, 'y': 7}, 4)
nI = node.Node(g, 'I', {'x': 2, 'y': 6}, 3)
nJ = node.Node(g, 'J', {'x': 3, 'y': 5}, 3)

# Adding nodes to graph
g.add_node(nA)
g.add_node(nB)
g.add_node(nC)
g.add_node(nD)
g.add_node(nE)
#g.add_node(nF)
#g.add_node(nG)
#g.add_node(nH)
#g.add_node(nI)
#g.add_node(nJ)

# Configure trickle params in nodes
# Setting Imax, Imin and redundancy k
for node in g.nodeList:
    node.configure_trickle_parameters(10, 100, 3)
    node.start_trickle_algorithm(0) # start trickle algorithm at time=0

# Debugging
for node in g.nodeList:
    outputstring = ''
    for adj_node in node.get_node_list():
        outputstring += ' ' + adj_node.nid + ' '
    print('I AM ' + node.nid + ' AND I CAN REACH: [' + outputstring + ']')

g.plot()

#for node in g.nodeList:
#    print('I AM ' + node.nid + ' AND MY STATE IS: ' + str(node.state) + ' --------------------------- ARRIVAL TIME OF: ' + str(node.arrivalPacket) + ' IS ' + str(node.arrivalTime))

g.window.getMouse() # pause before closing

g.run_simulation()
