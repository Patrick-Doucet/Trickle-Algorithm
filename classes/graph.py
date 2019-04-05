class Graph:

    def __init__(self):
        
        # Default init parameters
        self.nodeList = []
        
    # Add new node to network graph
    # Force all nodes (including the newly added node) to update their nodeList
    def add_node(self, node):
        self.nodeList.append(node)
        for node in self.nodeList:
            node.update_node_list(self.nodeList)
