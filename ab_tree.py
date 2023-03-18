#!/usr/bin/env python3

class ABNode:
    """Single node in an ABTree.

    Each node contains keys and children
    (with one more children than there are keys).
    We also store a pointer to node's parent (None for root).
    """
    def __init__(self, keys = None, children = None, parent = None):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.parent = parent

    def find_branch(self, key):
        """ Try finding given key in this node.

        If this node contains the given key, returns (True, key_position).
        If not, returns (False, first_position_with_key_greater_than_the_given).
        """
        i = 0
        while (i < len(self.keys) and self.keys[i] < key):
            i += 1

        return (i < len(self.keys) and self.keys[i] == key, i)

    def insert_branch(self, i, key, child):
        """ Insert a new key and a given child between keys i and i+1."""
        self.keys.insert(i, key)
        self.children.insert(i + 1, child)


class ABTree:
    """A class representing the whole ABTree."""

    def __init__(self, a, b):
        assert a >= 2 and b >= 2 * a - 1, "Invalid values of a, b: {}, {}".format(a, b)
        self.a = a
        self.b = b
        self.root = ABNode(children=[None])

    def find(self, key):
        """Find a key in the tree.

        Returns True if the key is present, False otherwise.
        """
        node = self.root
        while node:
            found, i = node.find_branch(key)
            if found: return True
            node = node.children[i]
        return False

    def split_node(self, node, size):
        """Helper function for insert

        Split node into two nodes such that original node contains first _size_ children.
        Return new node and the key separating nodes.
        """
        newNode = ABNode()
        key = node.keys[size]
        newNode.children = node.children[size + 1:]
        node.children = node.children[:size + 1]
        newNode.keys = node.keys[size + 1:]
        node.keys = node.keys[:size]

        for child in newNode.children:
            if child is not None:
                child.parent = newNode

        return newNode, key

        # TODO: Implement and use in insert method

    # Insert node
    def insert(self, k):
        parents = []
        node = self.root

        if (node == None):
            self.root = ABNode(k)
            return

        if(self.find(k)):
            return

        elif node.find_branch(k) is not True:
            while True:
                position = node.find_branch(k)[1]
                parents.append((node,position))
                if (node.children[position] is None):
                    break

                node = node.children[position]
            node.insert_branch(position, k, None)

            while len(node.keys) >= self.b:
                # newNode = ABNode()
                middleKeyIndex = len(node.keys)//2

                newNode, key = self.split_node(node, middleKeyIndex)

                if node == self.root:
                    self.root = ABNode()
                    self.root.children.append(node)
                    self.root.children.append(newNode)
                    self.root.keys.append(key)
                    self.root.parent = None
                    node.parent = self.root
                    newNode.parent = self.root
                    return
                else:
                    pos = node.parent.find_branch(key)[1]
                    node.parent.insert_branch(pos, key, newNode)
                    newNode.parent = node.parent
                    node = node.parent
