import classes.node as node
import classes.graph as graph
import sys
import numpy as np

# Initting test graph
g = graph.Graph(True)

# Fetch filename from command line: Ex: python simulation.py <filename>
paramsPath = sys.argv[1]
graphPath = sys.argv[2]

params = np.loadtxt(paramsPath)
graph = np.loadtxt(graphPath, dtype='str')
Imin, Imax, k = params
for line in graph:
    temp = node.Node(g, line[0], {'x': int(line[1]), 'y' : int(line[2])}, int(line[3]))

    # Configure trickle params in nodes
    # Setting Imax, Imin and redundancy k
    temp.configure_trickle_parameters(Imin,Imax,k)
    temp.start_trickle_algorithm(0) # start trickle algorithm at time=0

    # Adding nodes to graph
    g.add_node(temp)

print([Imax,Imin,k])

# Debugging
for node in g.nodeList:
    outputstring = ''
    for adj_node in node.get_node_list():
        outputstring += ' ' + adj_node.nid + ' '
    print('I AM ' + node.nid + ' AND I CAN REACH: [' + outputstring + ']')

g.plot()

g.window.getMouse() # pause before closing

g.run_simulation(g.nodeList[2])
