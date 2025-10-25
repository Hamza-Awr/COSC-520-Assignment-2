import random
import string
import time
import matplotlib.pyplot as plt
import json
import os

# ---- RED-BLACK TREE IMPLEMENTATION ----
# A Red-Black Tree is a self-balancing binary search tree where each node has a color (red or black)
# and maintains specific properties to ensure O(log n) operations for insert, delete, and search.

class RBNode:
    """Represents a single node in the Red-Black Tree."""
    def __init__(self, key):
        self.key = key
        self.color = 'red'  # new nodes start red
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    """Red-Black Tree implementation with insertion, deletion, search, and black-height validation."""
    def __init__(self):
        # NIL is a sentinel node representing empty children (all NIL nodes are black)
        self.NIL = RBNode(None)
        self.NIL.color = 'black'
        self.root = self.NIL

    # ---- Utility functions ----
    def left_rotate(self, x):
        """
        Rotate the subtree rooted at x to the left.
        Used during rebalancing to maintain tree structure.
        """
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """
        Rotate the subtree rooted at y to the right.
        Used during rebalancing to maintain tree structure.
        """
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    # ---- Insertion ----
    def insert(self, key):
        """
        Insert a new key into the Red-Black Tree.
        Ignores duplicate keys. Calls fix_insert to maintain RB properties.
        """
        node = RBNode(key)
        node.left = node.right = self.NIL

        # Find the correct position for the new node (standard BST insertion)
        parent = None
        current = self.root
        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            elif node.key > current.key:
                current = current.right
            else:
                return  # ignore duplicates

        # Insert the new node as a child of parent
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        # Fix any violations of Red-Black Tree properties
        self._fix_insert(node)

    def _fix_insert(self, z):
        """
        Rebalance the tree after insertion by recoloring and rotating nodes
        to maintain Red-Black Tree properties.
        """
        # Continue fixing while the parent of z is red (violates RB property)
        while z.parent and z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                # z's parent is a left child
                y = z.parent.parent.right  # uncle node
                if y.color == 'red':  # Case 1: uncle is red
                    # Recolor nodes
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    # Uncle is black
                    if z == z.parent.right:  # Case 2: z is a right child
                        # Rotate to make it a left child (Case 3)
                        z = z.parent
                        self.left_rotate(z)
                    # Case 3: z is a left child
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:  # mirror case: z's parent is a right child
                y = z.parent.parent.left  # uncle node
                if y.color == 'red':  # Case 1: uncle is red
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    # Uncle is black
                    if z == z.parent.left:  # Case 2: z is a left child
                        z = z.parent
                        self.right_rotate(z)
                    # Case 3: z is a right child
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        # Root must always be black
        self.root.color = 'black'

    # ---- Search ----
    def search(self, key):
        """
        Search for a key in the Red-Black Tree.
        Returns True if key exists, False otherwise.
        """
        node = self.root
        # Standard BST search
        while node != self.NIL and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node != self.NIL

    # ---- Deletion ----
    def _transplant(self, u, v):
        """
        Replace the subtree rooted at u with the subtree rooted at v.
        Helper function for deletion.
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """
        Find the node with minimum key in the subtree rooted at node.
        Returns the leftmost node.
        """
        while node.left != self.NIL:
            node = node.left
        return node

    def delete(self, key):
        """
        Delete a key from the Red-Black Tree.
        Calls fix_delete to maintain RB properties after deletion.
        """
        # Find the node to delete
        z = self.root
        while z != self.NIL and z.key != key:
            if key < z.key:
                z = z.left
            else:
                z = z.right
        if z == self.NIL:
            return  # key not found

        # Store information needed for fixing after deletion
        y = z
        y_original_color = y.color
        
        # Case 1: z has no left child
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        # Case 2: z has no right child
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        # Case 3: z has two children
        else:
            # Find successor (minimum in right subtree)
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        # Fix any violations if a black node was deleted
        if y_original_color == 'black':
            self._fix_delete(x)

    def _fix_delete(self, x):
        """
        Rebalance the tree after deletion by recoloring and rotating nodes
        to maintain Red-Black Tree properties.
        """
        # Continue fixing while x is not root and is black
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                # x is a left child
                w = x.parent.right  # sibling
                if w.color == 'red':
                    # Case 1: sibling is red
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == w.right.color == 'black':
                    # Case 2: sibling and its children are black
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        # Case 3: sibling's right child is black
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    # Case 4: sibling's right child is red
                    w.color = x.parent.color
                    x.parent.color = w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:  # mirror case: x is a right child
                w = x.parent.left  # sibling
                if w.color == 'red':
                    # Case 1: sibling is red
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == w.right.color == 'black':
                    # Case 2: sibling and its children are black
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        # Case 3: sibling's left child is black
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    # Case 4: sibling's left child is red
                    w.color = x.parent.color
                    x.parent.color = w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    # ---- Validation ----
    def validate_black_height(self):
        """
        Validate the Red-Black Tree property that all root-to-leaf paths
        contain the same number of black nodes.
        Returns True if valid, False otherwise.
        """
        def dfs(node):
            # Base case: NIL node counts as a black leaf
            if node == self.NIL:
                return 1
            # Recursively check left and right subtrees
            left = dfs(node.left)
            right = dfs(node.right)
            # If subtrees have different black heights or are invalid, return 0
            if left == 0 or right == 0 or left != right:
                return 0
            # Return the black height including current node if it's black
            return left + (1 if node.color == 'black' else 0)
        return dfs(self.root) > 0

# ---- BENCHMARK FUNCTION ----
def benchmark_rbt(n, number=1000):
    """
    Benchmark Red-Black Tree performance:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half non-existent)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time) in seconds
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    # Generate n random usernames for testing
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = RBTree()

    # ---- Insertion Benchmark ----
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert(name)
    # Calculate average time per insertion in seconds
    t_insert_rbt = (time.perf_counter_ns() - start) / n / 1e9

    # ---- Lookup Benchmark ----
    # Create a mix of existing and non-existing usernames for lookup
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search(name)
    # Calculate average time per lookup in seconds
    t_lookup_rbt = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # ---- Deletion Benchmark ----
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete(name)
    # Calculate average time per deletion in seconds
    t_delete_rbt = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    # ---- Validation ----
    # Verify that RB Tree properties are maintained after all operations
    assert tree.validate_black_height(), "Black-height property violated!"

    return t_insert_rbt, t_lookup_rbt, t_delete_rbt

# ---- MAIN TEST / PERFORMANCE PLOT ----
if __name__ == "__main__":
    # Test the tree with different sizes to measure performance scaling
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7]
    t_insert_list_rbt, t_lookup_list_rbt, t_delete_list_rbt = [], [], []

    # Run benchmarks for each size
    for n in n_values:
        t_insert_rbt, t_lookup_rbt, t_delete_rbt = benchmark_rbt(n)
        t_insert_list_rbt.append(t_insert_rbt)
        t_lookup_list_rbt.append(t_lookup_rbt)
        t_delete_list_rbt.append(t_delete_rbt)
        print(f"n={n}, insert={t_insert_rbt:.9e}, lookup={t_lookup_rbt:.9e}, delete={t_delete_rbt:.9e}")

    # ---- Save benchmark results ----
    results = {
        "n_list": n_values,
        "insert_times": t_insert_list_rbt,
        "lookup_times": t_lookup_list_rbt,
        "delete_times": t_delete_list_rbt
    }

    # Create Results folder if it doesn't exist
    os.makedirs("Results", exist_ok=True)

    # Save benchmark results to JSON file
    with open(os.path.join("Results", "results_rbtree.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results_rbtree.json")

    # ---- Create and save performance plot ----
    plt.figure(figsize=(8,6))
    plt.plot(n_values, t_insert_list_rbt, 'o-', label="Insertion")
    plt.plot(n_values, t_lookup_list_rbt, 's-', label="Lookup")
    plt.plot(n_values, t_delete_list_rbt, '^-', label="Deletion")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average time (s)")
    plt.title("Red-Black Tree Performance")
    plt.legend()
    plt.grid(False)
    # Save plot to Plots folder
    plt.savefig(os.path.join("Plots", "Red-Black_Tree_Performance.png"), dpi=300, bbox_inches="tight")
    plt.close()