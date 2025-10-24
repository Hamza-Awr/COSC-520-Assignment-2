import random
import string
import time
import matplotlib.pyplot as plt

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left = None
        self.right = None

class Treap:
    """Treap (Tree + Heap) with insert, search, delete, and rotations."""
    def __init__(self):
        self.root = None

    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def insert(self, root, key):
        if not root:
            return TreapNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
            if root.left.priority > root.priority:
                root = self.rotate_right(root)
        elif key > root.key:
            root.right = self.insert(root.right, key)
            if root.right.priority > root.priority:
                root = self.rotate_left(root)
        return root

    def search(self, root, key):
        if not root:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def delete(self, root, key):
        if not root:
            return None
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            if root.left.priority < root.right.priority:
                root = self.rotate_left(root)
                root.left = self.delete(root.left, key)
            else:
                root = self.rotate_right(root)
                root.right = self.delete(root.right, key)
        return root

    # Wrapper methods for easy usage like other trees
    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def search_key(self, key):
        return self.search(self.root, key)

    def delete_key(self, key):
        self.root = self.delete(self.root, key)

# ---- BENCHMARK FUNCTION ----
def benchmark_treap(n, number=1000):
    """
    Benchmark Treap:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half random)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time)
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = Treap()

    # ---- Insertion ----
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert_key(name)
    t_insert_treap = (time.perf_counter_ns() - start) / n / 1e9

    # ---- Lookup ----
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search_key(name)
    t_lookup_treap = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # ---- Deletion ----
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete_key(name)
    t_delete_treap = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    return t_insert_treap, t_lookup_treap, t_delete_treap

# ---- MAIN TEST / PERFORMANCE PLOT ----
if __name__ == "__main__":
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7]
    t_insert_list_treap, t_lookup_list_treap, t_delete_list_treap = [], [], []

    for n in n_values:
        t_insert_treap, t_lookup_treap, t_delete_treap = benchmark_treap(n)
        t_insert_list_treap.append(t_insert_treap)
        t_lookup_list_treap.append(t_lookup_treap)
        t_delete_list_treap.append(t_delete_treap)
        print(f"n={n}, insert={t_insert_treap:.9e}, lookup={t_lookup_treap:.9e}, delete={t_delete_treap:.9e}")

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
    plt.show()
