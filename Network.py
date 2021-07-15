
class Network:
    ''' Each node has an id that starts from 1. Network structure will look like this:
                        1
                    /       \
                2               3
              / |               | \
            4   5               6   7
          / |   | \           / |   |  \
        8   9   10  11      12  13  14 ...
        
        So we can find ones parent simply by dividing it's number by 2. And node i children will be i*2 and i*2+1.
    '''
    def __init__(self):
        self.root = None
        self.nodes_number = 1
        self.nodes = {}

    def insert_new_node(self, data):
        node_id = self.nodes_number
        self.nodes_number += 1

        if self.root == None:
            parent_node = None
        else:
            parent_id = node_id // 2
            parent_node = self.nodes[parent_id]

        new_node = Node(node_id, data, parent=parent_node)
        self.nodes[node_id] = new_node
        
        if self.root == None:
            self.root = new_node
        else:
            parent_node.add_child(new_node)

    def _str_network(self, node, level=0):
        if node is None:
            return ''

        return self._str_network(node.left, level + 1) + \
            f"{' ' * 5 * level} -> {node.data}\n" + \
            self._str_network(node.right, level + 1)
 
    def __str__(self):
        return self._str_network(self.root)


class Node:
    def __init__(self, id_, data, parent=None):
        self.id = id_
        self.parent = parent
        self.left = None
        self.right = None
        self.data = data

    def add_child(self, new_node):
        if new_node.id == self.id * 2:
            self.left = new_node
        else:
            self.right = new_node

    def __str__(self):
        if self.left is None:
            left = None
        else:
            left = self.left.data
        if self.right is None:
            right = None
        else:
            right = self.right.data
        if self.parent is None:
            parent = None
        else:
            parent = self.parent.data
        return "Data: {}, Left Child: {}, Right Child: {}, Parent: {}".format(self.data, left, right, parent)


# n = Network()
# for i in range(20):
#     n.insert_new_node(i)
# print(n)
