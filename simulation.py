import classes.node as node
import classes.graph as graph

# Initting test graph
g = graph.Graph()
nA = node.Node('A', {'x': 0, 'y': 3}, 2)
nB = node.Node('B', {'x': 1, 'y': 6}, 1)
nC = node.Node('C', {'x': 2, 'y': 5}, 3)
nD = node.Node('D', {'x': 5, 'y': 10}, 4)
nE = node.Node('E', {'x': 0, 'y': 0}, 3)
nF = node.Node('F', {'x': 3, 'y': 8}, 3)

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

nD.update_state(1)

for node in g.nodeList:
    print('I AM ' + node.nid + ' AND MY STATE IS: ' + str(node.state))

g.plot()