import random
import string
import time
import matplotlib.pyplot as plt

# ---- RED-BLACK TREE IMPLEMENTATION ----
class RBNode:
    def __init__(self, key):
        self.key = key
        self.color = 'red'  # new nodes start red
        self.left = None
        self.right = None
        self.parent = None

class RBTree:
    """Red-Black Tree implementation with insertion, deletion, search, and black-height validation."""
    def __init__(self):
        self.NIL = RBNode(None)
        self.NIL.color = 'black'
        self.root = self.NIL

    # ---- Utility functions ----
    def left_rotate(self, x):
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
        node = RBNode(key)
        node.left = node.right = self.NIL

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

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self._fix_insert(node)

    def _fix_insert(self, z):
        while z.parent and z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':  # Case 1
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:  # Case 2
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'  # Case 3
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:  # mirror case
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'black'

    # ---- Search ----
    def search(self, key):
        node = self.root
        while node != self.NIL and node.key != key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node != self.NIL

    # ---- Deletion ----
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def delete(self, key):
        z = self.root
        while z != self.NIL and z.key != key:
            if key < z.key:
                z = z.left
            else:
                z = z.right
        if z == self.NIL:
            return  # not found

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
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
        if y_original_color == 'black':
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:  # mirror case
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    # ---- Validation ----
    def validate_black_height(self):
        """Returns True if all root-to-leaf paths have same number of black nodes."""
        def dfs(node):
            if node == self.NIL:
                return 1  # count NIL as black leaf
            left = dfs(node.left)
            right = dfs(node.right)
            if left == 0 or right == 0 or left != right:
                return 0
            return left + (1 if node.color == 'black' else 0)
        return dfs(self.root) > 0

# ---- BENCHMARK FUNCTION ----
def benchmark_rbt(n, number=1000):
    """
    Benchmark Red-Black Tree:
      - Insert 'n' random usernames
      - Perform 'number' lookups (half existing, half random)
      - Perform 'number' deletions
    Returns: (avg_insert_time, avg_lookup_time, avg_delete_time)
    """
    chars = string.ascii_lowercase + string.digits
    random.seed(42)
    usernames = [''.join(random.choice(chars) for _ in range(5)) + str(i) for i in range(n)]

    tree = RBTree()

    # ---- Insertion ----
    start = time.perf_counter_ns()
    for name in usernames:
        tree.insert(name)
    t_insert_rbt = (time.perf_counter_ns() - start) / n / 1e9

    # ---- Lookup ----
    lookup_names = random.sample(usernames, min(number // 2, n))
    lookup_names += [''.join(random.choice(chars) for _ in range(5)) for _ in range(number - len(lookup_names))]
    start = time.perf_counter_ns()
    for name in lookup_names:
        tree.search(name)
    t_lookup_rbt = (time.perf_counter_ns() - start) / len(lookup_names) / 1e9

    # ---- Deletion ----
    delete_names = random.sample(usernames, min(number, n))
    start = time.perf_counter_ns()
    for name in delete_names:
        tree.delete(name)
    t_delete_rbt = (time.perf_counter_ns() - start) / len(delete_names) / 1e9

    # ---- Validation ----
    assert tree.validate_black_height(), "Black-height property violated!"

    return t_insert_rbt, t_lookup_rbt, t_delete_rbt

# ---- MAIN TEST / PERFORMANCE PLOT ----
if __name__ == "__main__":
    n_values = [10**3, 10**4, 10**5, 10**6, 10**7]
    t_insert_list_rbt, t_lookup_list_rbt, t_delete_list_rbt = [], [], []

    for n in n_values:
        t_insert_rbt, t_lookup_rbt, t_delete_rbt = benchmark_rbt(n)
        t_insert_list_rbt.append(t_insert_rbt)
        t_lookup_list_rbt.append(t_lookup_rbt)
        t_delete_list_rbt.append(t_delete_rbt)
        print(f"n={n}, insert={t_insert_rbt:.9e}, lookup={t_lookup_rbt:.9e}, delete={t_delete_rbt:.9e}")

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
    plt.show()
