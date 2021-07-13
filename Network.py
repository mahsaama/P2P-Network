
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.Data = None

    def set_data(self, data):
        self.Data = data

    def add_child(self, data):
        child = Node()
        child.set_data(data)
        if self.left is None:
            self.left = child
        else:
            self.right = child


def candid_parent(node: Node):
    if (node.left is None) or (node.right is None):
        return node
    else:
        pass
        # TODO Probably run two threads for left and right? one who answers faster wins and the other thread dies
