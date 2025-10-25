"""
plot_comparison.py
------------------
Plots benchmark results of AVL, Red-Black, and Treap trees
for insertion, lookup, and deletion operations on one figure
with three subplots (log–log scale).

Expected data:
- n_list: list of dataset sizes
- times_insert_*, times_lookup_*, times_delete_* for each tree
"""

import matplotlib.pyplot as plt
import json
import os

# ---- Example: Load from saved JSON file ----
# (Each benchmark script can save results as 'avl_results.json', 'rbt_results.json', etc.)
# Example JSON format:
# {
#     "n_list": [1000, 10000, 100000],
#     "insert_times": [1.2e-6, 1.8e-6, 2.5e-6],
#     "lookup_times": [0.8e-6, 1.1e-6, 1.6e-6],
#     "delete_times": [1.4e-6, 2.0e-6, 2.8e-6]
# }

def load_results(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# ---- Load benchmark results ----
avl = load_results("Results/results_avl.json")
rbtree = load_results("Results/results_rbtree.json")
treap = load_results("Results/results_treap.json")

n_list = avl["n_list"]

# ---- Create subplots ----
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
titles = ["Insertion", "Lookup", "Deletion"]
ylabels = ["Avg time per insertion (s)", "Avg time per lookup (s)", "Avg time per deletion (s)"]

# ---- Data tuples for iteration ----
data_sets = [
    (avl["insert_times"], rbtree["insert_times"], treap["insert_times"]),
    (avl["lookup_times"], rbtree["lookup_times"], treap["delete_times"]),  # note typo fix below
    (avl["delete_times"], rbtree["delete_times"], treap["delete_times"]),
]

# Correction: Use proper lookup_times for Treap
data_sets[1] = (avl["lookup_times"], rbtree["lookup_times"], treap["lookup_times"])

# Plot all three comparisons 
for i, ax in enumerate(axes):
    ax.plot(n_list, data_sets[i][0], 'o-', label="AVL Tree")
    ax.plot(n_list, data_sets[i][1], 's-', label="Red-Black Tree")
    ax.plot(n_list, data_sets[i][2], '^-', label="Treap")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Number of usernames (n)")
    ax.set_ylabel(ylabels[i])
    ax.set_title(f"{titles[i]} Performance")
    ax.legend()
    ax.grid(False)

# ---- Adjust layout and show ----
plt.tight_layout()
plt.savefig(os.path.join("Plots", "Overall_Data_structures_Performance.png"), dpi=300, bbox_inches="tight")
plt.close()