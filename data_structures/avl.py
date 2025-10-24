import random
import string
import time
import matplotlib.pyplot as plt

# AVLTree implementation
class AVLNode:
    """Node of an AVL Tree"""
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Height of a leaf node is 1

class AVLTree:
    """AVL Tree implementation with insert, delete, search, and traversals."""
    def __init__(self):
        self.root = None

    # Utility functions
    def _height(self, node):
        """Return the height of a node."""
        return node.height if node else 0

    def _update_height(self, node):
        """Recalculate height based on children."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """Compute the balance factor = left_height - right_height."""
        return self._height(node.left) - self._height(node.right) if node else 0

    def _min_node(self, node):
        """Return node with smallest key (used in deletion)."""
        while node.left:
            node = node.left
        return node

    # Rotations (O(1))
    def _right_rotate(self, y):
        """
        Perform a right rotation around node y.
                y                x
               / \              / \
              x   T3   -->     T1  y
             / \                  / \
            T1  T2               T2  T3
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self._update_height(y)
        self._update_height(x)

        return x  # New root of subtree

    def _left_rotate(self, x):
        """
        Perform a left rotation around node x.
            x                     y
           / \                   / \
          T1  y      -->        x  T3
             / \               / \
            T2  T3            T1  T2
        """
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self._update_height(x)
        self._update_height(y)

        return y  # New root of subtree

    # Rebalancing
    def _rebalance(self, node):
        """Rebalance a node if it's unbalanced (balance factor < -1 or > 1)."""
        self._update_height(node)
        bf = self._balance_factor(node)

        # Left heavy
        if bf > 1:
            # Left-Right case
            if self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left)
            # Left-Left case
            return self._right_rotate(node)

        # Right heavy
        if bf < -1:
            # Right-Left case
            if self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right)
            # Right-Right case
            return self._left_rotate(node)

        return node  # No imbalance

    # Insert (O(log n))
    def _insert(self, node, key, value=None):
        """Recursive helper to insert a key and rebalance."""
        if not node:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Duplicate key — update value (with new one)
            node.value = value
            return node

        return self._rebalance(node)

    def insert(self, key, value=None): # recursive
        """Public method to insert a key-value pair."""
        self.root = self._insert(self.root, key, value)

    # Search (O(log n))
    def search(self, key):
        """Return the value for the given key, or None if not found."""
        node = self.root
        while node:
            if key == node.key:
                return node.value if node.value is not None else node.key
            node = node.left if key < node.key else node.right
        return None

    # Delete (O(log n))
    def _delete(self, node, key):
        """Recursive helper to delete a key and rebalance."""
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node to delete found
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Node has two children: find inorder successor
                succ = self._min_node(node.right)
                node.key, node.value = succ.key, succ.value
                node.right = self._delete(node.right, succ.key)

        return self._rebalance(node) if node else None

    def delete(self, key):
        """Public method to delete a key."""
        self.root = self._delete(self.root, key)

    # Some extra functions not necessary for the main operations but may be useful
    # Traversals (O(n))
    def inorder(self):
        """Return in-order traversal as a list of (key, value)."""
        res = []
        def _in(node):
            if not node:
                return
            _in(node.left)
            res.append((node.key, node.value))
            _in(node.right)
        _in(self.root)
        return res

    def preorder(self):
        """Return pre-order traversal as a list of (key, value)."""
        res = []
        def _pre(node):
            if not node:
                return
            res.append((node.key, node.value))
            _pre(node.left)
            _pre(node.right)
        _pre(self.root)
        return res

    def postorder(self):
        """Return post-order traversal as a list of (key, value)."""
        res = []
        def _post(node):
            if not node:
                return
            _post(node.left)
            _post(node.right)
            res.append((node.key, node.value))
        _post(self.root)
        return res
    
    def is_balanced(self):
        """Check if the AVL tree is balanced (balance factor <= 1 for all nodes)."""
        def _check(node):
            if not node:
                return True, 0  # balanced, height 0
            left_bal, left_h = _check(node.left)
            right_bal, right_h = _check(node.right)
            node_balanced = left_bal and right_bal and abs(left_h - right_h) <= 1
            node_height = 1 + max(left_h, right_h)
            return node_balanced, node_height
        balanced, _ = _check(self.root)
        return balanced
    
    # Pretty-print (for debugging small trees)
    def _str(self, node, level=0, pref="Root: "):
        """Helper to print the tree structure."""
        if not node:
            return ""
        s = " " * (level * 4) + f"{pref}{node.key}(h={node.height})\n"
        s += self._str(node.left, level+1, "L--- ")
        s += self._str(node.right, level+1, "R--- ")
        return s

    def __str__(self):
        """String representation of the entire tree."""
        return self._str(self.root) or "<empty tree>"

# BENCHMARK FUNCTION
def benchmark_avl(n, number=1000):
    """
    Benchmark AVL Tree:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half random)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time)
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = AVLTree()

    # insertion
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert(name)
    t_insert_avl = (time.perf_counter_ns() - start) / n / 1e9

    # lookup
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search(name)
    t_lookup_avl = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # deletion
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete(name)
    t_delete_avl = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    return t_insert_avl, t_lookup_avl, t_delete_avl

# MAIN TEST

if __name__ == "__main__":
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7] # Values of n (size of dataset)
    t_insert_list_avl, t_lookup_list_avl, t_delete_list_avl = [], [], []

    for n in n_values:
        t_insert_avl, t_lookup_avl, t_delete_avl = benchmark_avl(n)
        t_insert_list_avl.append(t_insert_avl)
        t_lookup_list_avl.append(t_lookup_avl)
        t_delete_list_avl.append(t_delete_avl)
        print(f"n={n}, insert={t_insert_avl:.9e}, lookup={t_lookup_avl:.9e}, delete={t_delete_avl:.9e}")

    plt.figure(figsize=(8,6))
    plt.plot(n_values, t_insert_list_avl, 'o-', label="Insertion")
    plt.plot(n_values, t_lookup_list_avl, 's-', label="Lookup")
    plt.plot(n_values, t_delete_list_avl, '^-', label="Deletion")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average time (s)")
    plt.title("AVL Tree Performance")
    plt.legend()
    plt.grid(False)
    plt.show()