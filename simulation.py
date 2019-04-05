import classes.node as node
import classes.graph as graph

# Initting test graph
g = graph.Graph()
nA = node.Node('A', {'x': 0, 'y': 3}, 2)
nB = node.Node('B', {'x': 1, 'y': 4}, 1)
nC = node.Node('C', {'x': 2, 'y': 5}, 3)

# Debugging
print('A SHOULD SEE B? ' + str(nA.is_in_range(nB)))
print('A SHOULD SEE C? ' + str(nA.is_in_range(nC)))
print('B SHOULD SEE A? ' + str(nB.is_in_range(nA)))
print('B SHOULD SEE C? ' + str(nB.is_in_range(nC)))
print('C SHOULD SEE A? ' + str(nC.is_in_range(nA)))
print('C SHOULD SEE B? ' + str(nC.is_in_range(nB)))

# Adding nodes to graph
g.add_node(nA)
g.add_node(nB)
g.add_node(nC)

# Debugging
outputstring1 = ''
for node in nA.get_node_list():
    outputstring1 += ' ' + node.nid + ' '
print('I AM A AND I CAN REACH: [' + outputstring1 + ']')

outputstring1 = ''
for node in nB.get_node_list():
        outputstring1 += ' ' + node.nid + ' '
print('I AM B AND I CAN REACH: [' + outputstring1 + ']')

outputstring1 = ''
for node in nC.get_node_list():
        outputstring1 += ' ' + node.nid + ' '
print('I AM C AND I CAN REACH: [' + outputstring1 + ']')
