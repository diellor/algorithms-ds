#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        if left is not None: left.parent = self
        if right is not None: right.parent = self

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def rotate(self, node):
        """ Rotate the given `node` up.

        Performs a single rotation of the edge between the given node
        and its parent, choosing left or right rotation appropriately.
        """
        if node.parent is not None:
            if node.parent.left == node:
                if node.right is not None: node.right.parent = node.parent
                node.parent.left = node.right
                node.right = node.parent
            else:
                if node.left is not None: node.left.parent = node.parent
                node.parent.right = node.left
                node.left = node.parent
            if node.parent.parent is not None:
                if node.parent.parent.left == node.parent:
                    node.parent.parent.left = node
                else:
                    node.parent.parent.right = node
            else:
                self.root = node
            node.parent.parent, node.parent = node, node.parent.parent

    def lookup(self, key):
        """Look up the given key in the tree.

        Returns the node with the requested key or `None`.
        """
        # TODO: Utilize splay suitably.
        node = self.root
        while node is not None:
            isSplayed = node
            if node.key == key:
                self.splay(node)
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if(isSplayed is not None):
            self.splay(isSplayed)
        return None

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, nothing happens.
        """
        # TODO: Utilize splay suitably.
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

        self.splay(node)

    def remove(self, key):

        """Remove given key from the tree.

        It the key is not present, nothing happens.
        """
        # TODO: Utilize splay suitably.
        node = self.root
        while node is not None and node.key != key:
            isSplayed=node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is not None:
            if node.left is not None and node.right is not None:
                replacement = node.right
                while replacement.left is not None:
                    replacement = replacement.left
                node.key = replacement.key
                node = replacement

            replacement = node.left if node.left is not None else node.right
            if node.parent is not None:
                if node.parent.left == node: node.parent.left = replacement
                else: node.parent.right = replacement
            else:
                self.root = replacement
            if replacement is not None:
                replacement.parent = node.parent
            isSplayed = node.parent
            node = None

        if(isSplayed):
            self.splay(isSplayed)

    def splay(self, node):
        while node.parent != None:
            if node.parent == self.root:
                if node == node.parent.right:
                    self.leftRotate(node.parent) # only one rotation
                else:
                    self.rightRotate(node.parent) #only one rotation
            else:
                parent = node.parent
                parentParent = parent.parent
                if node.parent.left == node and parent.parent.left == parent:  # RR
                    self.rightRotate(parentParent)
                    self.rightRotate(parent)
                elif node.parent.right == node and parent.parent.right == parent: # LL
                    self.leftRotate(parentParent)
                    self.leftRotate(parent)
                elif node.parent.left == node and parent.parent.right == parent:  # RL
                    self.rightRotate(parent)
                    self.leftRotate(parentParent)
                elif node.parent.right == node and parent.parent.left == parent: # LR
                    self.leftRotate(parent)
                    self.rightRotate(parentParent)

    def leftRotate(self, node):
        child = node.right
        node.right = child.left
        if child.left != None:
            child.left.parent = node

        child.parent = node.parent
        if node.parent == None:
            self.root = child

        elif node == node.parent.left:
            node.parent.left = child

        else:
            node.parent.right = child
        child.left = node
        node.parent = child

    def rightRotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != None:
            y.right.parent = node

        y.parent = node.parent
        if node.parent == None:
            self.root = y

        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.right = node
        node.parent = y