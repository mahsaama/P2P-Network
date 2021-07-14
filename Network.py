class Network:
    def __init__(self):
        self.root = None

    def insert_node(self, root, data):
        if self.root is None:
            self.root = Node(data)
            return None
        else:
            if root.right is None:
                root.right = Node(data, root)
                return root.right.parent.data
            elif root.left is None:
                root.left = Node(data, root)
                return root.left.parent.data
            else:
                height_left = self.get_height(root.left)
                height_right = self.get_height(root.right)
                if height_left >= height_right:
                    return self.insert_node(root.right, data)
                else:
                    return self.insert_node(root.left, data)

    def get_height(self, root):
        if root is None:
            return -1
        height_left = self.get_height(root.left)
        height_right = self.get_height(root.right)
        if height_left > height_right:
            return height_left + 1
        else:
            return height_right + 1

    def print_network(self, node, level=0):
        if node is not None:
            self.print_network(node.left, level + 1)
            print(' ' * 4 * level + '->', node.data)
            self.print_network(node.right, level + 1)

    def __str__(self, root):
        root.__str__()
        if root.right is not None:
            self.__str__(root.right)
        if root.left is not None:
            self.__str__(root.left)


class Node:
    def __init__(self, data, par=None):
        self.parent = par
        self.left = None
        self.right = None
        self.data = data

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
        print("Data: {}, Left Child: {}, Right Child: {}, Parent: {}".format(self.data, left, right, parent))
