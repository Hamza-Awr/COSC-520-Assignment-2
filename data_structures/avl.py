import random
import string
import time
import matplotlib.pyplot as plt
import json
import os

# ---- AVL TREE IMPLEMENTATION ----
# An AVL Tree is a self-balancing binary search tree where the balance factor
# (left_height - right_height) of every node is in the range [-1, 1].
# This guarantees O(log n) time complexity for insert, delete, and search operations.

class AVLNode:
    """Node of an AVL Tree."""
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

    # ---- Utility functions ----
    def _height(self, node):
        """Return the height of a node. Returns 0 if node is None."""
        return node.height if node else 0

    def _update_height(self, node):
        """Recalculate and update the height of a node based on its children."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """
        Compute the balance factor of a node.
        balance_factor = height(left_subtree) - height(right_subtree)
        In a balanced AVL tree, this value should be in [-1, 0, 1].
        """
        return self._height(node.left) - self._height(node.right) if node else 0

    def _min_node(self, node):
        """
        Return the node with the smallest key in the subtree rooted at node.
        Used during deletion to find the in-order successor.
        """
        while node.left:
            node = node.left
        return node

    # ---- Rotations (O(1)) ----
    def _right_rotate(self, y):
        """
        Perform a right rotation around node y.
        This balances a left-heavy subtree by moving the left child up.
        
        Before:          After:
            y                x
           / \              / \
          x   T3   -->     T1  y
         / \                  / \
        T1  T2               T2  T3
        """
        x = y.left
        T2 = x.right

        # Perform rotation: rearrange pointers
        x.right = y
        y.left = T2

        # Update heights of affected nodes (bottom-up)
        self._update_height(y)
        self._update_height(x)

        # Return new root of subtree
        return x

    def _left_rotate(self, x):
        """
        Perform a left rotation around node x.
        This balances a right-heavy subtree by moving the right child up.
        
        Before:          After:
            x                y
           / \              / \
          T1  y   -->      x  T3
             / \           / \
            T2  T3        T1  T2
        """
        y = x.right
        T2 = y.left

        # Perform rotation: rearrange pointers
        y.left = x
        x.right = T2

        # Update heights of affected nodes (bottom-up)
        self._update_height(x)
        self._update_height(y)

        # Return new root of subtree
        return y

    # ---- Rebalancing ----
    def _rebalance(self, node):
        """
        Rebalance a node if it becomes unbalanced (balance factor < -1 or > 1).
        Handles four cases: Left-Left, Left-Right, Right-Left, Right-Right.
        """
        # Update height after modification
        self._update_height(node)
        bf = self._balance_factor(node)

        # ---- Left-heavy cases (balance factor > 1) ----
        if bf > 1:
            # Check if left child is right-heavy (Left-Right case)
            if self._balance_factor(node.left) < 0:
                # First, left rotate the left child to make it left-heavy
                node.left = self._left_rotate(node.left)
            # Left-Left case: perform right rotation on current node
            return self._right_rotate(node)

        # ---- Right-heavy cases (balance factor < -1) ----
        if bf < -1:
            # Check if right child is left-heavy (Right-Left case)
            if self._balance_factor(node.right) > 0:
                # First, right rotate the right child to make it right-heavy
                node.right = self._right_rotate(node.right)
            # Right-Right case: perform left rotation on current node
            return self._left_rotate(node)

        # Node is balanced or within acceptable range, no rebalancing needed
        return node

    # ---- Insertion (O(log n)) ----
    def _insert(self, node, key, value=None):
        """Recursive helper to insert a key-value pair and rebalance the tree."""
        if not node:
            # Base case: create and return a new node
            return AVLNode(key, value)

        if key < node.key:
            # Key is smaller, insert into left subtree
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            # Key is larger, insert into right subtree
            node.right = self._insert(node.right, key, value)
        else:
            # Duplicate key: update the value and return without rebalancing
            node.value = value
            return node

        # After insertion, rebalance the tree to maintain AVL properties
        return self._rebalance(node)

    def insert(self, key, value=None):
        """Public method to insert a key-value pair into the AVL tree."""
        self.root = self._insert(self.root, key, value)

    # ---- Search (O(log n)) ----
    def search(self, key):
        """
        Search for a key in the AVL tree.
        Returns the value associated with the key, or None if not found.
        """
        node = self.root
        # Standard BST search (AVL property ensures log n traversal)
        while node:
            if key == node.key:
                # Found the key, return value (or key if value is None)
                return node.value if node.value is not None else node.key
            # Navigate left or right based on key comparison
            node = node.left if key < node.key else node.right
        # Key not found
        return None

    # ---- Deletion (O(log n)) ----
    def _delete(self, node, key):
        """Recursive helper to delete a key and rebalance the tree."""
        if not node:
            # Base case: reached empty subtree, key not found
            return None

        if key < node.key:
            # Key is in left subtree, recursively delete
            node.left = self._delete(node.left, key)
        elif key > node.key:
            # Key is in right subtree, recursively delete
            node.right = self._delete(node.right, key)
        else:
            # Found the node to delete
            if not node.left:
                # Node has no left child: replace with right child (or None)
                return node.right
            elif not node.right:
                # Node has no right child: replace with left child
                return node.left
            else:
                # Node has two children: use in-order successor strategy
                # Find the successor (smallest key in right subtree)
                succ = self._min_node(node.right)
                # Copy successor's key and value to current node
                node.key, node.value = succ.key, succ.value
                # Delete the successor from right subtree
                node.right = self._delete(node.right, succ.key)

        # After deletion, rebalance the tree to maintain AVL properties
        return self._rebalance(node) if node else None

    def delete(self, key):
        """Public method to delete a key from the AVL tree."""
        self.root = self._delete(self.root, key)

    # ---- Tree Traversals (O(n)) ----
    # These functions visit all nodes in different orders; useful for debugging and analysis
    
    def inorder(self):
        """
        Return in-order traversal as a list of (key, value) pairs.
        In-order traversal visits nodes in sorted order (ascending by key).
        """
        res = []
        def _in(node):
            if not node:
                return
            _in(node.left)              # Visit left subtree
            res.append((node.key, node.value))  # Visit node
            _in(node.right)             # Visit right subtree
        _in(self.root)
        return res

    def preorder(self):
        """
        Return pre-order traversal as a list of (key, value) pairs.
        Pre-order traversal visits node before its children.
        """
        res = []
        def _pre(node):
            if not node:
                return
            res.append((node.key, node.value))  # Visit node first
            _pre(node.left)              # Visit left subtree
            _pre(node.right)             # Visit right subtree
        _pre(self.root)
        return res

    def postorder(self):
        """
        Return post-order traversal as a list of (key, value) pairs.
        Post-order traversal visits children before their parent node.
        """
        res = []
        def _post(node):
            if not node:
                return
            _post(node.left)             # Visit left subtree
            _post(node.right)            # Visit right subtree
            res.append((node.key, node.value))  # Visit node last
        _post(self.root)
        return res
    
    # ---- Tree Validation ----
    def is_balanced(self):
        """
        Check if the entire AVL tree maintains the balance property.
        Returns True if the balance factor of every node is in [-1, 0, 1].
        """
        def _check(node):
            if not node:
                # Empty subtree is balanced with height 0
                return True, 0
            # Recursively check left and right subtrees
            left_bal, left_h = _check(node.left)
            right_bal, right_h = _check(node.right)
            # Current node is balanced if both subtrees are balanced and their heights differ by at most 1
            node_balanced = left_bal and right_bal and abs(left_h - right_h) <= 1
            # Height of current node is 1 plus the maximum height of its children
            node_height = 1 + max(left_h, right_h)
            return node_balanced, node_height
        balanced, _ = _check(self.root)
        return balanced
    
    # ---- Pretty-Print (for debugging small trees) ----
    def _str(self, node, level=0, pref="Root: "):
        """Helper to print the tree structure with indentation for visual representation."""
        if not node:
            return ""
        # Build string representation of current node with height info
        s = " " * (level * 4) + f"{pref}{node.key}(h={node.height})\n"
        # Recursively add left and right subtrees with indentation
        s += self._str(node.left, level+1, "L--- ")
        s += self._str(node.right, level+1, "R--- ")
        return s

    def __str__(self):
        """String representation of the entire tree for debugging."""
        return self._str(self.root) or "<empty tree>"

# ---- BENCHMARK FUNCTION ----
def benchmark_avl(n, number=1000):
    """
    Benchmark AVL Tree performance:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half non-existent)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time) in seconds
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    # Generate n random usernames (string of 5 chars + index) for testing
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = AVLTree()

    # ---- Insertion Benchmark ----
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert(name)
    # Calculate average time per insertion in seconds
    t_insert_avl = (time.perf_counter_ns() - start) / n / 1e9

    # ---- Lookup Benchmark ----
    # Create a mix of existing and non-existing usernames for lookup
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search(name)
    # Calculate average time per lookup in seconds
    t_lookup_avl = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # ---- Deletion Benchmark ----
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete(name)
    # Calculate average time per deletion in seconds
    t_delete_avl = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    return t_insert_avl, t_lookup_avl, t_delete_avl

# ---- MAIN TEST ----
if __name__ == "__main__":
    # Test the tree with different sizes to measure performance scaling
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7]  # Values of n (size of dataset)
    t_insert_list_avl, t_lookup_list_avl, t_delete_list_avl = [], [], []

    # Run benchmarks for each size
    for n in n_values:
        t_insert_avl, t_lookup_avl, t_delete_avl = benchmark_avl(n)
        t_insert_list_avl.append(t_insert_avl)
        t_lookup_list_avl.append(t_lookup_avl)
        t_delete_list_avl.append(t_delete_avl)
        print(f"n={n}, insert={t_insert_avl:.9e}, lookup={t_lookup_avl:.9e}, delete={t_delete_avl:.9e}")

    # ---- Save benchmark results ----
    results = {
        "n_list": n_values,
        "insert_times": t_insert_list_avl,
        "lookup_times": t_lookup_list_avl,
        "delete_times": t_delete_list_avl
    }

    # Create Results folder if it doesn't exist
    os.makedirs("Results", exist_ok=True)

    # Save benchmark results to JSON file
    with open(os.path.join("Results", "results_avl.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results_avl.json")

    # ---- Create and save performance plot ----
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
    # Save plot to Plots folder
    plt.savefig(os.path.join("Plots", "AVL_Tree_Performance.png"), dpi=300, bbox_inches="tight")
    plt.close()
    plt.show()