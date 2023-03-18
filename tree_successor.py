#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, do nothing.
        """
        if self.root is None:
            self.root = Node(key)
            return

        node = self.root
        while node.key != key:
            if key < node.key:
                if node.left is None:
                    node.left = Node(key, parent=node)
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(key, parent=node)
                node = node.right

    def successor(self, node=None):
        nodey = self.root
        if node is None:
            while nodey.left is not None:
                nodey = nodey.left
            return nodey

        if node.right is not None:
            nodey = node.right
            while nodey.left:
                nodey = nodey.left
            return nodey
        else:
            parent = node.parent
            while parent is not None:
                if parent.left == node:
                    break
                node = parent
                parent = node.parent
        return parent