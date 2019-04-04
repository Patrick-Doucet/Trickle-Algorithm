import classes.node as node
import classes.graph as graph

g = graph.Graph()
n1 = node.Node({'x': 0, 'y': 3}, 2)
n2 = node.Node({'x': 1, 'y': 4}, 1)

print(n1.distance_between_2_points({'x': 0, 'y': 3}, {'x': 1, 'y': 4}))
print(n1.is_in_range({'x': 0, 'y': 3}, {'x': 1, 'y': 4}))
print(n2.is_in_range({'x': 0, 'y': 3}, {'x': 1, 'y': 4}))
print(g.nodeList)

g.add_node(n1)
g.add_node(n2)
for node in g.nodeList:
    print(node.position)