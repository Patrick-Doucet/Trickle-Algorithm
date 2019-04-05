import classes.node as node
import classes.graph as graph

# Initting test graph
g = graph.Graph()
nA = node.Node(g, 'A', {'x': 0, 'y': 3}, 2)
nB = node.Node(g, 'B', {'x': 1, 'y': 6}, 1)
nC = node.Node(g, 'C', {'x': 2, 'y': 5}, 3)
nD = node.Node(g, 'D', {'x': 5, 'y': 10}, 4)
nE = node.Node(g, 'E', {'x': 0, 'y': 0}, 3)
nF = node.Node(g, 'F', {'x': 3, 'y': 8}, 3)

# Adding nodes to graph
g.add_node(nA)
g.add_node(nB)
g.add_node(nC)
g.add_node(nD)
g.add_node(nE)
g.add_node(nF)

# Debugging
for node in g.nodeList:
    outputstring = ''
    for adj_node in node.get_node_list():
        outputstring += ' ' + adj_node.nid + ' '
    print('I AM ' + node.nid + ' AND I CAN REACH: [' + outputstring + ']')

g.plot()

nC.transmit(nC.nodeList)
