import sys
import random
BLACK = "black"
RED = "red"

class RBTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = BLACK

    def get_color(self):
        return self.color

    def print_info(self):
        print(f"Key: {self.key}, Color: {self.color}, Parent-key: {self.parent.key if self.parent else None}, \
        Left-key: {self.left.key if self.left else None}, Right-key: {self.right.key if self.right else None}")

class RedBlackTree:
    def __init__(self):
        self.nil = RBTNode(None)
        self.root = self.nil
        self.nil.color = BLACK
        self.nil.parent = None

    # left rotate like in AvlTree
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # right rotate like in AvlTree
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # insert node to tree
    def insert(self, z):
        z = RBTNode(z)
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.nil
        z.right = self.nil
        z.color = RED
        self.insert_fixup(z)

    # insert fixup for RB-Tree 3cases
    def insert_fixup(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
                if z == self.root:
                    break
        self.root.color = BLACK

    def delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def tree_minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def search(self, key):
        x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def delete(self, z):
        z = self.search(z)
        if z == self.nil:
            exit("node not found")
        y = z
        y_original_color = y.color # y_original_color is used to store the original color of y
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self.delete_fixup(x)

    def __print_helper(self, node, indent, last):
        if node != self.nil:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = node.color
            val = str(node.key)
            if s_color == RED:
                val = "\033[91m" + val + "\033[0m"
                print(val)
            else:
                print(val)
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def print_tree(self):
        self.__print_helper(self.root, "", True)

def rbt_test():
    bst = RedBlackTree()
    node = [5,3,8,1,4,6,9,7,10]
    for i in node:
        bst.insert(i)
    bst.print_tree()
    print("\nAfter deleting an element")
    bst.delete(5)
    bst.print_tree()

def rbt_random_test():
    bst = RedBlackTree()
    keys = [random.randint(0,100) for i in range(10)] # fill the list with random numbers
    for i in keys:
        print("Inserting: ", i)
        bst.insert(i)
    bst.print_tree()
    delete = keys[random.randint(0,9)] # pick a random number to delete
    print("\nAfter deleting an element ", delete)
    bst.delete(delete)
    bst.print_tree()

rbt_test()