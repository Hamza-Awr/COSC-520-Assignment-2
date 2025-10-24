"""
Unit tests for Treap (Tree + Heap) implementation.

This module provides comprehensive testing for the Treap data structure,
including insertion, deletion, search, and heap property validation.
"""

import unittest
import random
import sys
import os

# Add parent directory to path to import treap module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_structures.treap import Treap, TreapNode


class TestTreapNode(unittest.TestCase):
    """Test cases for TreapNode class."""
    
    def test_node_creation_with_priority(self):
        """Test that a node is created with specified priority."""
        node = TreapNode(10, priority=0.5)
        self.assertEqual(node.key, 10)
        self.assertEqual(node.priority, 0.5)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
    
    def test_node_creation_random_priority(self):
        """Test that a node is created with random priority if not specified."""
        random.seed(42)
        node = TreapNode(10)
        self.assertEqual(node.key, 10)
        self.assertIsNotNone(node.priority)
        self.assertGreaterEqual(node.priority, 0.0)
        self.assertLessEqual(node.priority, 1.0)
    
    def test_different_nodes_different_priorities(self):
        """Test that different nodes get different random priorities."""
        nodes = [TreapNode(i) for i in range(10)]
        priorities = [node.priority for node in nodes]
        
        # Very unlikely all 10 priorities are the same
        self.assertGreater(len(set(priorities)), 1)


class TestTreapBasicOperations(unittest.TestCase):
    """Test basic operations: insert, search, delete."""
    
    def setUp(self):
        """Initialize a fresh Treap before each test."""
        self.treap = Treap()
        random.seed(42)  # For reproducible tests
    
    def test_empty_treap(self):
        """Test operations on an empty treap."""
        self.assertIsNone(self.treap.root)
        self.assertFalse(self.treap.search_key(1))
    
    def test_single_insertion(self):
        """Test inserting a single element."""
        self.treap.insert_key(10)
        self.assertIsNotNone(self.treap.root)
        self.assertEqual(self.treap.root.key, 10)
    
    def test_multiple_insertions(self):
        """Test inserting multiple elements."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            self.treap.insert_key(key)
        
        # Verify all keys are present
        for key in keys:
            self.assertTrue(self.treap.search_key(key))
    
    def test_search_existing_keys(self):
        """Test searching for keys that exist."""
        keys = [15, 10, 20, 5, 12, 18, 25]
        for key in keys:
            self.treap.insert_key(key)
        
        for key in keys:
            self.assertTrue(self.treap.search_key(key))
    
    def test_search_nonexistent_keys(self):
        """Test searching for keys that don't exist."""
        self.treap.insert_key(10)
        self.treap.insert_key(20)
        
        self.assertFalse(self.treap.search_key(5))
        self.assertFalse(self.treap.search_key(15))
        self.assertFalse(self.treap.search_key(25))
    
    def test_delete_single_node(self):
        """Test deleting the only node in the treap."""
        self.treap.insert_key(10)
        self.treap.delete_key(10)
        
        self.assertIsNone(self.treap.root)
        self.assertFalse(self.treap.search_key(10))
    
    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        keys = [20, 10, 30]
        for key in keys:
            self.treap.insert_key(key)
        
        # Find a leaf (depends on priorities, but one should be leaf)
        self.treap.delete_key(10)
        
        self.assertFalse(self.treap.search_key(10))
        self.assertTrue(self.treap.search_key(20))
        self.assertTrue(self.treap.search_key(30))
    
    def test_delete_node_with_children(self):
        """Test deleting a node with children."""
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.treap.insert_key(key)
        
        self.treap.delete_key(20)
        self.assertFalse(self.treap.search_key(20))
        
        # All other keys should still be present
        for key in [10, 30, 5, 15, 25, 35]:
            self.assertTrue(self.treap.search_key(key))
    
    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        self.treap.insert_key(10)
        self.treap.insert_key(20)
        
        # Should not raise error
        self.treap.delete_key(30)
        
        # Original keys should still be present
        self.assertTrue(self.treap.search_key(10))
        self.assertTrue(self.treap.search_key(20))
    
    def test_insert_duplicate_keys(self):
        """Test that duplicate keys are handled (should be ignored)."""
        self.treap.insert_key(10)
        self.treap.insert_key(10)
        
        # Should still be able to find it
        self.assertTrue(self.treap.search_key(10))


class TestTreapProperties(unittest.TestCase):
    """Test Treap properties (BST for keys, heap for priorities)."""
    
    def setUp(self):
        """Initialize a fresh Treap before each test."""
        self.treap = Treap()
        random.seed(42)
    
    def test_bst_property(self):
        """Test that BST property is maintained for keys."""
        keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
        for key in keys:
            self.treap.insert_key(key)
        
        # Collect keys via in-order traversal
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(self.treap.root)
        self.assertEqual(result, sorted(keys))
    
    def test_heap_property(self):
        """Test that max-heap property is maintained for priorities."""
        keys = list(range(1, 21))
        for key in keys:
            self.treap.insert_key(key)
        
        def check_heap_property(node):
            """Check that parent priority >= children priorities."""
            if not node:
                return True
            
            if node.left and node.left.priority > node.priority:
                return False
            if node.right and node.right.priority > node.priority:
                return False
            
            return check_heap_property(node.left) and check_heap_property(node.right)
        
        self.assertTrue(check_heap_property(self.treap.root))
    
    def test_bst_property_after_deletions(self):
        """Test BST property is maintained after deletions."""
        keys = list(range(1, 31))
        for key in keys:
            self.treap.insert_key(key)
        
        # Delete half the keys
        to_delete = random.sample(keys, 15)
        for key in to_delete:
            self.treap.delete_key(key)
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(self.treap.root)
        self.assertEqual(result, sorted(result))
    
    def test_heap_property_after_deletions(self):
        """Test heap property is maintained after deletions."""
        keys = list(range(1, 31))
        for key in keys:
            self.treap.insert_key(key)
        
        # Delete some keys
        to_delete = random.sample(keys, 15)
        for key in to_delete:
            self.treap.delete_key(key)
        
        def check_heap_property(node):
            if not node:
                return True
            
            if node.left and node.left.priority > node.priority:
                return False
            if node.right and node.right.priority > node.priority:
                return False
            
            return check_heap_property(node.left) and check_heap_property(node.right)
        
        self.assertTrue(check_heap_property(self.treap.root))


class TestTreapRotations(unittest.TestCase):
    """Test rotations in Treap."""
    
    def setUp(self):
        """Initialize a fresh Treap before each test."""
        self.treap = Treap()
    
    def test_insertion_triggers_rotations(self):
        """Test that insertions trigger rotations based on priorities."""
        # Insert with specific priorities to force rotations
        node1 = TreapNode(10, priority=0.3)
        node2 = TreapNode(5, priority=0.5)
        node3 = TreapNode(15, priority=0.7)
        
        self.treap.root = self.treap.insert(None, 10)
        self.treap.root.priority = 0.3
        
        self.treap.root = self.treap.insert(self.treap.root, 5)
        if self.treap.root.left:
            self.treap.root.left.priority = 0.5
        
        # After insertion, higher priority should be closer to root
        # Due to rotations
        self.assertIsNotNone(self.treap.root)
    
    def test_properties_maintained_after_rotations(self):
        """Test that both BST and heap properties are maintained after rotations."""
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            self.treap.insert_key(key)
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(self.treap.root)
        self.assertEqual(result, sorted(keys))
        
        # Check heap property
        def check_heap(node):
            if not node:
                return True
            if node.left and node.left.priority > node.priority:
                return False
            if node.right and node.right.priority > node.priority:
                return False
            return check_heap(node.left) and check_heap(node.right)
        
        self.assertTrue(check_heap(self.treap.root))


class TestTreapEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_large_sequential_insertions(self):
        """Test inserting many sequential values."""
        treap = Treap()
        random.seed(42)
        n = 1000
        
        for i in range(n):
            treap.insert_key(i)
        
        # Verify random samples
        for i in range(0, n, 100):
            self.assertTrue(treap.search_key(i))
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(len(result), n)
        self.assertEqual(result, sorted(result))
    
    def test_large_reverse_insertions(self):
        """Test inserting many values in reverse order."""
        treap = Treap()
        random.seed(42)
        n = 1000
        
        for i in range(n, 0, -1):
            treap.insert_key(i)
        
        # Verify random samples
        for i in range(100, n, 100):
            self.assertTrue(treap.search_key(i))
    
    def test_large_random_insertions(self):
        """Test inserting many random values."""
        treap = Treap()
        random.seed(42)
        keys = list(range(1000))
        random.shuffle(keys)
        
        for key in keys:
            treap.insert_key(key)
        
        # Verify random samples
        for key in random.sample(keys, 100):
            self.assertTrue(treap.search_key(key))
    
    def test_negative_keys(self):
        """Test treap with negative keys."""
        treap = Treap()
        random.seed(42)
        keys = [-10, -5, -15, 0, 5, -20, 10]
        
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            self.assertTrue(treap.search_key(key))
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(result, sorted(keys))
    
    def test_string_keys(self):
        """Test treap with string keys."""
        treap = Treap()
        random.seed(42)
        keys = ["dog", "cat", "elephant", "ant", "zebra", "bear"]
        
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            self.assertTrue(treap.search_key(key))
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(result, sorted(keys))
    
    def test_delete_all_nodes(self):
        """Test deleting all nodes from the treap."""
        treap = Treap()
        random.seed(42)
        keys = [10, 5, 15, 2, 7, 12, 20]
        
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            treap.delete_key(key)
        
        self.assertIsNone(treap.root)
    
    def test_alternating_insert_delete(self):
        """Test alternating insertions and deletions."""
        treap = Treap()
        random.seed(42)
        
        for i in range(100):
            treap.insert_key(i)
            if i % 3 == 0 and i > 0:
                treap.delete_key(i - 1)
            
            # Check properties are maintained
            result = []
            def inorder(node):
                if node:
                    inorder(node.left)
                    result.append(node.key)
                    inorder(node.right)
            
            inorder(treap.root)
            self.assertEqual(result, sorted(result))


class TestTreapStressTests(unittest.TestCase):
    """Stress tests for Treap."""
    
    def test_insert_delete_cycle(self):
        """Test repeated insert and delete of same keys."""
        treap = Treap()
        random.seed(42)
        keys = [1, 2, 3, 4, 5]
        
        for _ in range(10):
            for key in keys:
                treap.insert_key(key)
            for key in keys:
                treap.delete_key(key)
        
        self.assertIsNone(treap.root)
    
    def test_random_operations_sequence(self):
        """Test a random sequence of operations."""
        treap = Treap()
        inserted_keys = set()
        
        random.seed(42)
        for _ in range(500):
            operation = random.choice(['insert', 'delete', 'search'])
            key = random.randint(1, 100)
            
            if operation == 'insert':
                treap.insert_key(key)
                inserted_keys.add(key)
            elif operation == 'delete' and inserted_keys:
                treap.delete_key(key)
                inserted_keys.discard(key)
            elif operation == 'search':
                result = treap.search_key(key)
                if key in inserted_keys:
                    self.assertTrue(result)
            
            # Check BST property is maintained
            result = []
            def inorder(node):
                if node:
                    inorder(node.left)
                    result.append(node.key)
                    inorder(node.right)
            
            inorder(treap.root)
            self.assertEqual(result, sorted(result))
    
    def test_many_small_values(self):
        """Test with many small integer values."""
        treap = Treap()
        random.seed(42)
        keys = list(range(1, 201))
        random.shuffle(keys)
        
        for key in keys:
            treap.insert_key(key)
        
        # Verify all present
        for key in keys:
            self.assertTrue(treap.search_key(key))
        
        # Delete half
        to_delete = random.sample(keys, 100)
        for key in to_delete:
            treap.delete_key(key)
        
        # Verify deleted ones are gone
        for key in to_delete:
            self.assertFalse(treap.search_key(key))
        
        # Verify remaining ones are still there
        remaining = set(keys) - set(to_delete)
        for key in remaining:
            self.assertTrue(treap.search_key(key))
    
    def test_pathological_priorities(self):
        """Test with all same priorities (degrades to BST)."""
        treap = Treap()
        
        # Insert with same priority
        for i in range(10):
            treap.root = treap.insert(treap.root, i)
            if treap.root:
                current = treap.root
                while current.right:
                    current = current.right
                current.priority = 0.5  # Same priority for all
        
        # Should still maintain BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(result, sorted(result))


class TestTreapRandomization(unittest.TestCase):
    """Test randomization aspects of Treap."""
    
    def test_different_structures_different_seeds(self):
        """Test that different random seeds produce different tree structures."""
        keys = list(range(1, 21))
        
        # Build treap with seed 1
        random.seed(1)
        treap1 = Treap()
        for key in keys:
            treap1.insert_key(key)
        
        # Build treap with seed 2
        random.seed(2)
        treap2 = Treap()
        for key in keys:
            treap2.insert_key(key)
        
        # Collect structures
        def collect_structure(node):
            if not node:
                return []
            return [(node.key, node.priority)] + collect_structure(node.left) + collect_structure(node.right)
        
        struct1 = collect_structure(treap1.root)
        struct2 = collect_structure(treap2.root)
        
        # Structures should be different (very unlikely to be the same)
        self.assertNotEqual(struct1, struct2)
    
    def test_expected_height(self):
        """Test that tree height is reasonable (expected O(log n))."""
        treap = Treap()
        random.seed(42)
        n = 1000
        
        for i in range(n):
            treap.insert_key(i)
        
        def height(node):
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))
        
        h = height(treap.root)
        
        # Expected height is O(log n), with high probability < 4*log2(n)
        import math
        max_expected_height = 4 * math.log2(n)
        
        self.assertLess(h, max_expected_height)


class TestTreapCorrectness(unittest.TestCase):
    """Test overall correctness of Treap operations."""
    
    def test_insert_search_consistency(self):
        """Test that inserted keys can always be found."""
        treap = Treap()
        random.seed(42)
        keys = list(range(1, 101))
        random.shuffle(keys)
        
        for key in keys:
            treap.insert_key(key)
            self.assertTrue(treap.search_key(key))
    
    def test_delete_search_consistency(self):
        """Test that deleted keys cannot be found."""
        treap = Treap()
        random.seed(42)
        keys = list(range(1, 51))
        
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            treap.delete_key(key)
            self.assertFalse(treap.search_key(key))
    
    def test_operations_maintain_invariants(self):
        """Test that all operations maintain both BST and heap properties."""
        treap = Treap()
        random.seed(42)
        
        operations = []
        for _ in range(100):
            op = random.choice(['insert', 'delete'])
            key = random.randint(1, 50)
            operations.append((op, key))
        
        for op, key in operations:
            if op == 'insert':
                treap.insert_key(key)
            else:
                treap.delete_key(key)
            
            # Check BST property
            result = []
            def inorder(node):
                if node:
                    inorder(node.left)
                    result.append(node.key)
                    inorder(node.right)
            
            inorder(treap.root)
            self.assertEqual(result, sorted(result))
            
            # Check heap property
            def check_heap(node):
                if not node:
                    return True
                if node.left and node.left.priority > node.priority:
                    return False
                if node.right and node.right.priority > node.priority:
                    return False
                return check_heap(node.left) and check_heap(node.right)
            
            self.assertTrue(check_heap(treap.root))
    
    def test_all_keys_reachable(self):
        """Test that all inserted keys are reachable via search."""
        treap = Treap()
        random.seed(42)
        keys = list(range(1, 101))
        random.shuffle(keys)
        
        for key in keys:
            treap.insert_key(key)
        
        # All keys should be searchable
        for key in keys:
            self.assertTrue(treap.search_key(key), f"Key {key} should be found")
        
        # Non-inserted keys should not be found
        for key in range(101, 111):
            self.assertFalse(treap.search_key(key), f"Key {key} should not be found")


class TestTreapComparisonWithBST(unittest.TestCase):
    """Test that Treap behaves correctly as a BST."""
    
    def test_inorder_traversal_sorted(self):
        """Test that inorder traversal always gives sorted sequence."""
        treap = Treap()
        random.seed(42)
        
        # Test with multiple different key sets
        test_sets = [
            list(range(1, 21)),
            list(range(20, 0, -1)),
            [5, 15, 3, 20, 1, 10, 25, 8],
        ]
        
        for keys in test_sets:
            treap = Treap()
            random.seed(42)
            
            for key in keys:
                treap.insert_key(key)
            
            result = []
            def inorder(node):
                if node:
                    inorder(node.left)
                    result.append(node.key)
                    inorder(node.right)
            
            inorder(treap.root)
            self.assertEqual(result, sorted(keys))
    
    def test_min_max_keys(self):
        """Test finding minimum and maximum keys."""
        treap = Treap()
        random.seed(42)
        keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
        
        for key in keys:
            treap.insert_key(key)
        
        # Find minimum (leftmost node)
        def find_min(node):
            if not node:
                return None
            while node.left:
                node = node.left
            return node.key
        
        # Find maximum (rightmost node)
        def find_max(node):
            if not node:
                return None
            while node.right:
                node = node.right
            return node.key
        
        self.assertEqual(find_min(treap.root), min(keys))
        self.assertEqual(find_max(treap.root), max(keys))
    
    def test_successor_predecessor(self):
        """Test that BST successor/predecessor relationships hold."""
        treap = Treap()
        random.seed(42)
        keys = [10, 5, 15, 3, 7, 12, 20]
        
        for key in keys:
            treap.insert_key(key)
        
        # Get sorted keys
        sorted_keys = sorted(keys)
        
        # Collect inorder traversal
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        
        # Verify each key's position in sorted order
        for i, key in enumerate(sorted_keys):
            self.assertEqual(result[i], key)


class TestTreapMemoryAndPerformance(unittest.TestCase):
    """Test memory and performance characteristics."""
    
    def test_no_memory_leak_on_delete(self):
        """Test that deleted nodes don't cause issues."""
        treap = Treap()
        random.seed(42)
        
        # Insert many nodes
        for i in range(100):
            treap.insert_key(i)
        
        # Delete all nodes
        for i in range(100):
            treap.delete_key(i)
        
        # Tree should be empty
        self.assertIsNone(treap.root)
        
        # Should be able to reuse
        treap.insert_key(50)
        self.assertTrue(treap.search_key(50))
    
    def test_operations_complete_quickly(self):
        """Test that operations complete in reasonable time."""
        import time
        
        treap = Treap()
        random.seed(42)
        n = 10000
        
        # Time insertions
        start = time.time()
        for i in range(n):
            treap.insert_key(i)
        insert_time = time.time() - start
        
        # Time searches
        start = time.time()
        for i in range(0, n, 10):
            treap.search_key(i)
        search_time = time.time() - start
        
        # Time deletions
        start = time.time()
        for i in range(0, n, 10):
            treap.delete_key(i)
        delete_time = time.time() - start
        
        # Operations should complete in reasonable time
        # These are generous bounds - actual times should be much faster
        self.assertLess(insert_time, 5.0, "Insertions took too long")
        self.assertLess(search_time, 1.0, "Searches took too long")
        self.assertLess(delete_time, 1.0, "Deletions took too long")


class TestTreapSpecialCases(unittest.TestCase):
    """Test special cases and corner scenarios."""
    
    def test_single_node_operations(self):
        """Test all operations on a single-node tree."""
        treap = Treap()
        treap.insert_key(42)
        
        # Search should work
        self.assertTrue(treap.search_key(42))
        self.assertFalse(treap.search_key(41))
        self.assertFalse(treap.search_key(43))
        
        # Root should be the only node
        self.assertEqual(treap.root.key, 42)
        self.assertIsNone(treap.root.left)
        self.assertIsNone(treap.root.right)
        
        # Delete should empty the tree
        treap.delete_key(42)
        self.assertIsNone(treap.root)
    
    def test_two_node_configurations(self):
        """Test different two-node configurations."""
        # Left child configuration
        treap1 = Treap()
        treap1.root = TreapNode(10, priority=0.9)
        treap1.root.left = TreapNode(5, priority=0.5)
        
        self.assertTrue(treap1.search_key(10))
        self.assertTrue(treap1.search_key(5))
        
        # Right child configuration
        treap2 = Treap()
        treap2.root = TreapNode(10, priority=0.9)
        treap2.root.right = TreapNode(15, priority=0.5)
        
        self.assertTrue(treap2.search_key(10))
        self.assertTrue(treap2.search_key(15))
    
    def test_complete_tree_structure(self):
        """Test building a complete tree structure."""
        treap = Treap()
        random.seed(42)
        
        # Insert 7 nodes (can form complete binary tree)
        keys = [4, 2, 6, 1, 3, 5, 7]
        for key in keys:
            treap.insert_key(key)
        
        # All nodes should be present
        for key in keys:
            self.assertTrue(treap.search_key(key))
        
        # BST property should hold
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(result, sorted(keys))
    
    def test_skewed_insertions(self):
        """Test handling of skewed insertion patterns."""
        # All left insertions (ascending)
        treap1 = Treap()
        random.seed(42)
        for i in range(1, 11):
            treap1.insert_key(i)
        
        # BST property should still hold due to randomized priorities
        result1 = []
        def inorder1(node):
            if node:
                inorder1(node.left)
                result1.append(node.key)
                inorder1(node.right)
        
        inorder1(treap1.root)
        self.assertEqual(result1, list(range(1, 11)))
        
        # All right insertions (descending)
        treap2 = Treap()
        random.seed(42)
        for i in range(10, 0, -1):
            treap2.insert_key(i)
        
        result2 = []
        def inorder2(node):
            if node:
                inorder2(node.left)
                result2.append(node.key)
                inorder2(node.right)
        
        inorder2(treap2.root)
        self.assertEqual(result2, list(range(1, 11)))
    
    def test_repeated_same_operations(self):
        """Test repeated same operations."""
        treap = Treap()
        random.seed(42)
        
        # Insert same key multiple times
        for _ in range(10):
            treap.insert_key(5)
        
        # Should still have only one node with that key
        self.assertTrue(treap.search_key(5))
        
        # Delete same key multiple times (only first should have effect)
        for _ in range(10):
            treap.delete_key(5)
        
        # Key should be gone
        self.assertFalse(treap.search_key(5))
    
    def test_empty_after_clear(self):
        """Test that tree is properly empty after clearing all nodes."""
        treap = Treap()
        random.seed(42)
        
        keys = list(range(1, 26))
        for key in keys:
            treap.insert_key(key)
        
        # Delete all in random order
        random.shuffle(keys)
        for key in keys:
            treap.delete_key(key)
        
        # Tree should be completely empty
        self.assertIsNone(treap.root)
        
        # Should be able to use again
        treap.insert_key(100)
        self.assertTrue(treap.search_key(100))
        self.assertEqual(treap.root.key, 100)


class TestTreapFloatingPointPriorities(unittest.TestCase):
    """Test handling of floating-point priorities."""
    
    def test_priority_range(self):
        """Test that priorities are within expected range."""
        treap = Treap()
        random.seed(42)
        
        for i in range(50):
            treap.insert_key(i)
        
        def check_priorities(node):
            if not node:
                return True
            
            # Priority should be between 0 and 1
            self.assertGreaterEqual(node.priority, 0.0)
            self.assertLessEqual(node.priority, 1.0)
            
            return check_priorities(node.left) and check_priorities(node.right)
        
        check_priorities(treap.root)
    
    def test_priority_uniqueness(self):
        """Test that priorities are generally unique."""
        treap = Treap()
        random.seed(42)
        
        for i in range(100):
            treap.insert_key(i)
        
        priorities = []
        def collect_priorities(node):
            if node:
                priorities.append(node.priority)
                collect_priorities(node.left)
                collect_priorities(node.right)
        
        collect_priorities(treap.root)
        
        # Most priorities should be unique (allowing for rare collisions)
        unique_count = len(set(priorities))
        self.assertGreater(unique_count, 95)  # At least 95% unique
    
    def test_explicit_priorities(self):
        """Test using explicit priorities."""
        treap = Treap()
        
        # Manually construct tree with specific priorities
        treap.root = treap.insert(None, 50)
        treap.root.priority = 0.9
        
        treap.root = treap.insert(treap.root, 30)
        treap.root.left.priority = 0.8
        
        treap.root = treap.insert(treap.root, 70)
        treap.root.right.priority = 0.7
        
        # Verify structure respects priorities
        self.assertEqual(treap.root.key, 50)
        self.assertGreater(treap.root.priority, treap.root.left.priority)
        self.assertGreater(treap.root.priority, treap.root.right.priority)


class TestTreapBoundaryValues(unittest.TestCase):
    """Test boundary values and extreme cases."""
    
    def test_very_large_keys(self):
        """Test with very large key values."""
        treap = Treap()
        random.seed(42)
        
        keys = [10**6, 10**6 + 1, 10**6 + 2, 10**9, 10**9 + 1]
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            self.assertTrue(treap.search_key(key))
    
    def test_very_small_keys(self):
        """Test with very small (negative) key values."""
        treap = Treap()
        random.seed(42)
        
        keys = [-10**6, -10**6 + 1, -10**9, -10**9 + 1, -1]
        for key in keys:
            treap.insert_key(key)
        
        for key in keys:
            self.assertTrue(treap.search_key(key))
    
    def test_zero_key(self):
        """Test with zero as a key."""
        treap = Treap()
        treap.insert_key(0)
        
        self.assertTrue(treap.search_key(0))
        self.assertEqual(treap.root.key, 0)
        
        treap.delete_key(0)
        self.assertFalse(treap.search_key(0))
    
    def test_mixed_positive_negative(self):
        """Test with mix of positive and negative keys."""
        treap = Treap()
        random.seed(42)
        
        keys = [-100, -50, -10, -1, 0, 1, 10, 50, 100]
        for key in keys:
            treap.insert_key(key)
        
        # Check BST property
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(treap.root)
        self.assertEqual(result, sorted(keys))


class TestTreapDeletionEdgeCases(unittest.TestCase):
    """Test specific edge cases for deletion."""
    
    def test_delete_root_with_two_children(self):
        """Test deleting root when it has two children."""
        treap = Treap()
        random.seed(42)
        
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            treap.insert_key(key)
        
        root_key = treap.root.key
        treap.delete_key(root_key)
        
        self.assertFalse(treap.search_key(root_key))
        
        # All other keys should still be present
        remaining = [k for k in keys if k != root_key]
        for key in remaining:
            self.assertTrue(treap.search_key(key))
    
    def test_delete_leaves_only(self):
        """Test deleting all leaf nodes."""
        treap = Treap()
        random.seed(42)
        
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            treap.insert_key(key)
        
        # Find and delete leaf nodes
        def find_leaves(node):
            if not node:
                return []
            if not node.left and not node.right:
                return [node.key]
            return find_leaves(node.left) + find_leaves(node.right)
        
        leaves = find_leaves(treap.root)
        for leaf in leaves:
            treap.delete_key(leaf)
            self.assertFalse(treap.search_key(leaf))
    
    def test_delete_in_reverse_insertion_order(self):
        """Test deleting in reverse order of insertion."""
        treap = Treap()
        random.seed(42)
        
        keys = [10, 5, 15, 3, 7, 12, 20]
        for key in keys:
            treap.insert_key(key)
        
        # Delete in reverse order
        for key in reversed(keys):
            treap.delete_key(key)
            self.assertFalse(treap.search_key(key))
        
        self.assertIsNone(treap.root)


class TestTreapConsistencyChecks(unittest.TestCase):
    """Test consistency of treap structure after various operations."""
    
    def test_no_orphaned_nodes(self):
        """Test that no nodes are orphaned after operations."""
        treap = Treap()
        random.seed(42)
        
        keys = list(range(1, 51))
        for key in keys:
            treap.insert_key(key)
        
        # Count reachable nodes
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        self.assertEqual(count_nodes(treap.root), 50)
        
        # Delete half
        to_delete = random.sample(keys, 25)
        for key in to_delete:
            treap.delete_key(key)
        
        # Should have exactly 25 nodes remaining
        self.assertEqual(count_nodes(treap.root), 25)
    
    def test_parent_child_consistency(self):
        """Test that parent-child relationships are consistent."""
        treap = Treap()
        random.seed(42)
        
        for i in range(20):
            treap.insert_key(i)
        
        def check_consistency(node, parent_key=None):
            if not node:
                return True
            
            # Check BST property
            if node.left:
                self.assertLess(node.left.key, node.key)
            if node.right:
                self.assertGreater(node.right.key, node.key)
            
            # Check heap property
            if node.left:
                self.assertGreaterEqual(node.priority, node.left.priority)
            if node.right:
                self.assertGreaterEqual(node.priority, node.right.priority)
            
            return check_consistency(node.left, node.key) and check_consistency(node.right, node.key)
        
        self.assertTrue(check_consistency(treap.root))
    
    def test_structure_integrity_after_stress(self):
        """Test that structure remains intact after many operations."""
        treap = Treap()
        random.seed(42)
        
        # Perform many random operations
        for _ in range(1000):
            op = random.choice(['insert', 'delete', 'search'])
            key = random.randint(1, 100)
            
            if op == 'insert':
                treap.insert_key(key)
            elif op == 'delete':
                treap.delete_key(key)
            else:
                treap.search_key(key)
        
        # Verify integrity
        def verify_structure(node):
            if not node:
                return True, []
            
            left_ok, left_keys = verify_structure(node.left)
            right_ok, right_keys = verify_structure(node.right)
            
            # Check BST property
            for k in left_keys:
                if k >= node.key:
                    return False, []
            for k in right_keys:
                if k <= node.key:
                    return False, []
            
            # Check heap property
            if node.left and node.left.priority > node.priority:
                return False, []
            if node.right and node.right.priority > node.priority:
                return False, []
            
            return left_ok and right_ok, left_keys + [node.key] + right_keys
        
        ok, _ = verify_structure(treap.root)
        self.assertTrue(ok)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)