import random
import string
import time
import matplotlib.pyplot as plt
import json
import os

class TreapNode:
    """Represents a single node in the Treap (randomized BST with heap property)."""
    def __init__(self, key, priority=None):
        self.key = key
        # Priority is randomly assigned; if not provided, generate a random value
        # This ensures the tree maintains heap property with high probability
        self.priority = priority if priority is not None else random.random()
        self.left = None
        self.right = None

class Treap:
    """
    Treap (Tree + Heap) - A randomized self-balancing binary search tree.
    Combines properties of binary search trees (ordered by key) and binary heaps (ordered by priority).
    With high probability, achieves O(log n) operations for insert, delete, and search.
    """
    def __init__(self):
        self.root = None

    def rotate_right(self, y):
        """
        Perform a right rotation at node y.
        This moves y's left child up to take y's place, and y becomes the right child.
        Used to maintain the heap property (higher priority nodes move toward root).
        """
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def rotate_left(self, x):
        """
        Perform a left rotation at node x.
        This moves x's right child up to take x's place, and x becomes the left child.
        Used to maintain the heap property (higher priority nodes move toward root).
        """
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def insert(self, root, key):
        """
        Recursively insert a key into the treap.
        Maintains BST property by key and heap property by priority through rotations.
        If key already exists, it is not inserted (no duplicates).
        """
        if not root:
            # Base case: create a new node with random priority
            return TreapNode(key)
        
        if key < root.key:
            # Key is smaller, insert into left subtree
            root.left = self.insert(root.left, key)
            # Check heap property: if left child has higher priority, rotate right
            if root.left.priority > root.priority:
                root = self.rotate_right(root)
        elif key > root.key:
            # Key is larger, insert into right subtree
            root.right = self.insert(root.right, key)
            # Check heap property: if right child has higher priority, rotate left
            if root.right.priority > root.priority:
                root = self.rotate_left(root)
        # If key == root.key, do nothing (ignore duplicates)
        
        return root

    def search(self, root, key):
        """
        Recursively search for a key in the treap.
        Returns True if key exists, False otherwise.
        """
        if not root:
            # Base case: reached empty node, key not found
            return False
        
        if key == root.key:
            # Found the key
            return True
        elif key < root.key:
            # Key is smaller, search in left subtree
            return self.search(root.left, key)
        else:
            # Key is larger, search in right subtree
            return self.search(root.right, key)

    def delete(self, root, key):
        """
        Recursively delete a key from the treap.
        Uses rotations to move the target node to a leaf position before removal.
        Returns the modified subtree root.
        """
        if not root:
            # Base case: reached empty node, key not found
            return None
        
        if key < root.key:
            # Key is in left subtree, recursively delete
            root.left = self.delete(root.left, key)
        elif key > root.key:
            # Key is in right subtree, recursively delete
            root.right = self.delete(root.right, key)
        else:
            # Found the node to delete
            if not root.left:
                # Node has no left child, return right child (or None if no right child)
                return root.right
            elif not root.right:
                # Node has no right child, return left child
                return root.left
            
            # Node has two children: use rotations to bubble it down to a leaf
            # Compare priorities of left and right children
            if root.left.priority < root.right.priority:
                # Right child has higher priority, rotate left to move it up
                root = self.rotate_left(root)
                # Continue deleting from the left subtree
                root.left = self.delete(root.left, key)
            else:
                # Left child has higher priority (or equal), rotate right to move it up
                root = self.rotate_right(root)
                # Continue deleting from the right subtree
                root.right = self.delete(root.right, key)
        
        return root

    # ---- Wrapper methods for easy usage ----
    def insert_key(self, key):
        """Public method to insert a key into the treap."""
        self.root = self.insert(self.root, key)

    def search_key(self, key):
        """Public method to search for a key in the treap."""
        return self.search(self.root, key)

    def delete_key(self, key):
        """Public method to delete a key from the treap."""
        self.root = self.delete(self.root, key)

# ---- BENCHMARK FUNCTION ----
def benchmark_treap(n, number=1000):
    """
    Benchmark Treap performance:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half non-existent)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time) in seconds
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    # Generate n random usernames (string of 5 chars + index) for testing
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = Treap()

    # ---- Insertion Benchmark ----
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert_key(name)
    # Calculate average time per insertion in seconds
    t_insert_treap = (time.perf_counter_ns() - start) / n / 1e9

    # ---- Lookup Benchmark ----
    # Create a mix of existing and non-existing usernames for lookup
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search_key(name)
    # Calculate average time per lookup in seconds
    t_lookup_treap = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # ---- Deletion Benchmark ----
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete_key(name)
    # Calculate average time per deletion in seconds
    t_delete_treap = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    return t_insert_treap, t_lookup_treap, t_delete_treap

# ---- MAIN TEST / PERFORMANCE PLOT ----
if __name__ == "__main__":
    # Test the treap with different sizes to measure performance scaling
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7]
    t_insert_list_treap, t_lookup_list_treap, t_delete_list_treap = [], [], []

    # Run benchmarks for each size
    for n in n_values:
        t_insert_treap, t_lookup_treap, t_delete_treap = benchmark_treap(n)
        t_insert_list_treap.append(t_insert_treap)
        t_lookup_list_treap.append(t_lookup_treap)
        t_delete_list_treap.append(t_delete_treap)
        print(f"n={n}, insert={t_insert_treap:.9e}, lookup={t_lookup_treap:.9e}, delete={t_delete_treap:.9e}")

    # ---- Save benchmark results ----
    results = {
        "n_list": n_values,
        "insert_times": t_insert_list_treap,
        "lookup_times": t_lookup_list_treap,
        "delete_times": t_delete_list_treap
    }

    # Create Results folder if it doesn't exist
    os.makedirs("Results", exist_ok=True)

    # Save benchmark results to JSON file
    with open(os.path.join("Results", "results_treap.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results_treap.json")

    # ---- Create and save performance plot ----
    plt.figure(figsize=(8,6))
    plt.plot(n_values, t_insert_list_treap, 'o-', label="Insertion")
    plt.plot(n_values, t_lookup_list_treap, 's-', label="Lookup")
    plt.plot(n_values, t_delete_list_treap, '^-', label="Deletion")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of usernames (n)")
    plt.ylabel("Average time (s)")
    plt.title("Treap Performance")
    plt.legend()
    plt.grid(False)
    # Save plot to Plots folder
    plt.savefig(os.path.join("Plots", "Treap_Performance.png"), dpi=300, bbox_inches="tight")
    plt.close()