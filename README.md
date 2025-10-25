# Balanced Binary Search Trees

A comprehensive implementation and testing suite for three self-balancing binary search tree data structures: **AVL Tree**, **Red-Black Tree**, and **Treap**.

## Repository Structure

```
├── data_structures/
│   ├── avl.py          # AVL Tree implementation
│   ├── rbtree.py       # Red-Black Tree implementation
│   └── treap.py        # Treap implementation
├── tests/
│   ├── test_avl.py     # AVL Tree unit tests
│   ├── test_rbtree.py  # Red-Black Tree unit tests
│   └── test_treap.py   # Treap unit tests
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Data Structures

### AVL Tree
- **Self-balancing** binary search tree
- Maintains height balance: |height(left) - height(right)| ≤ 1
- Operations: O(log n) insert, delete, search
- Includes: rotations (LL, RR, LR, RL), traversals, balance validation

### Red-Black Tree
- **Self-balancing** binary search tree with color properties
- Ensures no path is more than twice as long as any other
- Operations: O(log n) insert, delete, search
- Includes: rotations, recoloring, black-height validation

### Treap
- **Randomized** binary search tree (Tree + Heap)
- BST property for keys, max-heap property for priorities
- Expected O(log n) operations
- Includes: priority-based rotations, randomization

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run All Tests
```bash
# Run all test files automatically
python -m unittest discover tests/ -v
```

### Run Individual Test Files
```bash
# AVL Tree tests
python -m unittest tests.test_avl -v

# Red-Black Tree tests
python -m unittest tests.test_rbtree -v

# Treap tests
python -m unittest tests.test_treap -v

```

### Run Specific Test Classes
```bash
# Run only AVL rotation tests
python -m unittest tests.test_avl.TestAVLTreeRotations -v

# Run only Red-Black tree properties tests
python -m unittest tests.test_rbtree.TestRBTreeProperties -v
```

## Test Coverage

### AVL Tree Tests (50+ tests)
- Basic operations (insert, search, delete)
- All rotation cases (LL, RR, LR, RL)
- Balance factor validation
- Traversals (inorder, preorder, postorder)
- Edge cases (1000+ elements, negative/string keys)
- Stress tests with random operations

### Red-Black Tree Tests (40+ tests)
- All 5 Red-Black properties
- Large-scale operations (10,000+ elements)
- Random operation sequences (5,000+ ops)
- Stress tests (repeated cycles, min/max deletions)
- Consistency checks (parent pointers, no cycles)
- Performance validation (logarithmic height)

### Treap Tests (60+ tests)
- BST and max-heap property validation
- Randomization testing
- Priority-based rotations
- Large datasets (10,000+ elements)
- Floating-point priority handling
- Boundary value tests

## Usage Examples

### AVL Tree
```python
from data_structures.avl import AVLTree

# Create tree
tree = AVLTree()

# Insert values
tree.insert(10, "value10")
tree.insert(20, "value20")
tree.insert(5, "value5")

# Search
result = tree.search(10)  # Returns "value10"

# Delete
tree.delete(20)

# Check if balanced
print(tree.is_balanced())  # True

# Traversals
print(tree.inorder())   # Returns sorted list of (key, value) tuples
```

### Red-Black Tree
```python
from data_structures.rbtree import RBTree

# Create tree
tree = RBTree()

# Insert values
tree.insert(10)
tree.insert(20)
tree.insert(5)

# Search
found = tree.search(10)  # Returns True

# Delete
tree.delete(20)

# Validate black-height property
print(tree.validate_black_height())  # True
```

### Treap
```python
from data_structures.treap import Treap

# Create treap
treap = Treap()

# Insert values (priorities assigned randomly)
treap.insert_key(10)
treap.insert_key(20)
treap.insert_key(5)

# Search
found = treap.search_key(10)  # Returns True

# Delete
treap.delete_key(20)
```

## Running Benchmarks

Each data structure file includes a benchmark section that tests performance with datasets of varying sizes (10³ to 10⁷ elements):

```bash
# Run AVL Tree benchmark
python data_structures/avl.py

# Run Red-Black Tree benchmark
python data_structures/rbtree.py

# Run Treap benchmark
python data_structures/treap.py
```

This will output timing data and generate a performance plot showing:
- Average insertion time
- Average lookup time
- Average deletion time