"""
Unit tests for Red-Black Tree implementation.

This module provides comprehensive testing for the Red-Black Tree data structure,
focusing on the most important properties and edge cases.
"""

import unittest
import random
import sys
import os

# Add parent directory to path to import rbtree module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_structures.rbtree import RBTree, RBNode


class TestRBTreeBasicOperations(unittest.TestCase):
    """Test basic operations: insert, search, delete."""
    
    def setUp(self):
        """Initialize a fresh Red-Black tree before each test."""
        self.tree = RBTree()
    
    def test_empty_tree(self):
        """Test operations on an empty tree."""
        self.assertEqual(self.tree.root, self.tree.NIL)
        self.assertFalse(self.tree.search(1))
    
    def test_single_insertion(self):
        """Test inserting a single element."""
        self.tree.insert(10)
        self.assertNotEqual(self.tree.root, self.tree.NIL)
        self.assertEqual(self.tree.root.key, 10)
        self.assertEqual(self.tree.root.color, 'black')  # Root is always black
    
    def test_multiple_insertions_and_search(self):
        """Test inserting multiple elements and searching."""
        keys = [15, 10, 20, 5, 12, 18, 25]
        for key in keys:
            self.tree.insert(key)
        
        for key in keys:
            self.assertTrue(self.tree.search(key))
        
        # Non-existent keys
        self.assertFalse(self.tree.search(1))
        self.assertFalse(self.tree.search(30))
    
    def test_duplicate_insertion(self):
        """Test that duplicate keys are ignored."""
        self.tree.insert(10)
        self.tree.insert(10)
        
        # Count nodes manually (should be 1)
        count = 0
        def count_nodes(node):
            nonlocal count
            if node != self.tree.NIL:
                count += 1
                count_nodes(node.left)
                count_nodes(node.right)
        
        count_nodes(self.tree.root)
        self.assertEqual(count, 1)
    
    def test_delete_operations(self):
        """Test various deletion scenarios."""
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key)
        
        # Delete leaf node
        self.tree.delete(5)
        self.assertFalse(self.tree.search(5))
        
        # Delete node with two children
        self.tree.delete(20)
        self.assertFalse(self.tree.search(20))
        
        # Other keys should still be present
        for key in [10, 30, 15, 25, 35]:
            self.assertTrue(self.tree.search(key))
        
        self.assertTrue(self.tree.validate_black_height())
    
    def test_delete_all_nodes(self):
        """Test deleting all nodes from the tree."""
        keys = [10, 5, 15, 2, 7, 12, 20]
        
        for key in keys:
            self.tree.insert(key)
        
        for key in keys:
            self.tree.delete(key)
        
        self.assertEqual(self.tree.root, self.tree.NIL)


class TestRBTreeProperties(unittest.TestCase):
    """Test Red-Black tree properties."""
    
    def setUp(self):
        """Initialize a fresh Red-Black tree before each test."""
        self.tree = RBTree()
    
    def test_root_always_black(self):
        """Test that root is always black after any operations."""
        for i in range(1, 21):
            self.tree.insert(i)
            self.assertEqual(self.tree.root.color, 'black')
        
        # Delete some nodes
        for i in [5, 10, 15]:
            self.tree.delete(i)
            if self.tree.root != self.tree.NIL:
                self.assertEqual(self.tree.root.color, 'black')
    
    def test_red_nodes_have_black_children(self):
        """Test that red nodes have only black children (no consecutive reds)."""
        keys = list(range(1, 51))
        random.shuffle(keys)
        
        for key in keys:
            self.tree.insert(key)
        
        def check_red_property(node):
            if node == self.tree.NIL:
                return True
            
            if node.color == 'red':
                # Both children must be black
                self.assertEqual(node.left.color, 'black')
                self.assertEqual(node.right.color, 'black')
            
            return check_red_property(node.left) and check_red_property(node.right)
        
        self.assertTrue(check_red_property(self.tree.root))
    
    def test_black_height_consistency(self):
        """Test that all paths have the same black height."""
        keys = list(range(1, 101))
        random.shuffle(keys)
        
        for key in keys:
            self.tree.insert(key)
            self.assertTrue(self.tree.validate_black_height())
        
        # Delete half the keys and check again
        to_delete = random.sample(keys, 50)
        for key in to_delete:
            self.tree.delete(key)
            self.assertTrue(self.tree.validate_black_height())
    
    def test_bst_property_maintained(self):
        """Test that BST property is maintained (inorder gives sorted)."""
        keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
        for key in keys:
            self.tree.insert(key)
        
        # Collect keys via in-order traversal
        result = []
        def inorder(node):
            if node != self.tree.NIL:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(self.tree.root)
        self.assertEqual(result, sorted(keys))


class TestRBTreeLargeDatasets(unittest.TestCase):
    """Test with large datasets and various patterns."""
    
    def test_large_sequential_insertions(self):
        """Test inserting 10000 sequential values."""
        tree = RBTree()
        n = 10000
        
        for i in range(n):
            tree.insert(i)
        
        self.assertTrue(tree.validate_black_height())
        
        # Verify random samples
        for i in range(0, n, 1000):
            self.assertTrue(tree.search(i))
    
    def test_large_reverse_insertions(self):
        """Test inserting 10000 values in reverse order."""
        tree = RBTree()
        n = 10000
        
        for i in range(n, 0, -1):
            tree.insert(i)
        
        self.assertTrue(tree.validate_black_height())
        
        # Verify random samples
        for i in range(1, n, 1000):
            self.assertTrue(tree.search(i))
    
    def test_large_random_insertions(self):
        """Test inserting 10000 random values."""
        tree = RBTree()
        keys = list(range(10000))
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.validate_black_height())
        
        # Verify random samples
        for key in random.sample(keys, 100):
            self.assertTrue(tree.search(key))
    
    def test_large_scale_deletions(self):
        """Test large-scale insertions followed by deletions."""
        tree = RBTree()
        n = 5000
        
        # Insert
        for i in range(n):
            tree.insert(i)
        
        # Delete half
        for i in range(0, n, 2):
            tree.delete(i)
            if i % 100 == 0:  # Check periodically
                self.assertTrue(tree.validate_black_height())
        
        # Verify remaining keys
        for i in range(1, n, 2):
            self.assertTrue(tree.search(i))
        
        # Verify deleted keys
        for i in range(0, n, 2):
            self.assertFalse(tree.search(i))


class TestRBTreeStressTests(unittest.TestCase):
    """Stress tests for Red-Black tree."""
    
    def test_random_operations_sequence(self):
        """Test 5000 random operations maintaining all properties."""
        tree = RBTree()
        inserted_keys = set()
        
        random.seed(42)
        for _ in range(5000):
            operation = random.choice(['insert', 'delete', 'search'])
            key = random.randint(1, 500)
            
            if operation == 'insert':
                tree.insert(key)
                inserted_keys.add(key)
            elif operation == 'delete' and inserted_keys:
                tree.delete(key)
                inserted_keys.discard(key)
            elif operation == 'search':
                result = tree.search(key)
                if key in inserted_keys:
                    self.assertTrue(result)
            
            # Validate periodically
            if _ % 100 == 0:
                self.assertTrue(tree.validate_black_height())
    
    def test_insert_delete_cycle(self):
        """Test repeated insert and delete cycles."""
        tree = RBTree()
        keys = list(range(1, 101))
        
        for _ in range(20):
            # Insert all
            for key in keys:
                tree.insert(key)
            
            self.assertTrue(tree.validate_black_height())
            
            # Delete all
            random.shuffle(keys)
            for key in keys:
                tree.delete(key)
        
        self.assertEqual(tree.root, tree.NIL)
    
    def test_alternating_min_max_deletions(self):
        """Test deleting alternately from min and max."""
        tree = RBTree()
        keys = list(range(1, 101))
        
        for key in keys:
            tree.insert(key)
        
        # Alternately delete min and max
        count = 0
        while tree.root != tree.NIL:
            # Find and delete min
            node = tree.root
            while node.left != tree.NIL:
                node = node.left
            min_key = node.key
            tree.delete(min_key)
            
            count += 1
            if tree.root == tree.NIL:
                break
            
            # Find and delete max
            node = tree.root
            while node.right != tree.NIL:
                node = node.right
            max_key = node.key
            tree.delete(max_key)
            
            count += 1
            
            # Validate periodically
            if count % 10 == 0 and tree.root != tree.NIL:
                self.assertTrue(tree.validate_black_height())
        
        self.assertEqual(tree.root, tree.NIL)
    
    def test_delete_root_repeatedly(self):
        """Test repeatedly deleting the root node."""
        tree = RBTree()
        keys = list(range(1, 201))
        
        for key in keys:
            tree.insert(key)
        
        # Delete root 100 times
        for i in range(100):
            if tree.root != tree.NIL:
                root_key = tree.root.key
                tree.delete(root_key)
                self.assertFalse(tree.search(root_key))
                
                if i % 10 == 0 and tree.root != tree.NIL:
                    self.assertTrue(tree.validate_black_height())


class TestRBTreeEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_negative_and_positive_keys(self):
        """Test tree with mix of negative, zero, and positive keys."""
        tree = RBTree()
        keys = list(range(-500, 501))
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.validate_black_height())
        
        # Check BST property
        result = []
        def inorder(node):
            if node != tree.NIL:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        
        inorder(tree.root)
        self.assertEqual(result, sorted(keys))
    
    def test_string_keys(self):
        """Test tree with string keys."""
        tree = RBTree()
        keys = [f"key_{i:04d}" for i in range(1000)]
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.validate_black_height())
        
        # Verify random samples
        for key in random.sample(keys, 100):
            self.assertTrue(tree.search(key))
    
    def test_very_large_keys(self):
        """Test with very large key values."""
        tree = RBTree()
        keys = [10**9 + i for i in range(1000)]
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        self.assertTrue(tree.validate_black_height())
        
        for key in random.sample(keys, 100):
            self.assertTrue(tree.search(key))


class TestRBTreePerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_tree_height_logarithmic(self):
        """Test that tree height is O(log n)."""
        tree = RBTree()
        n = 10000
        
        for i in range(n):
            tree.insert(i)
        
        # Calculate actual height
        def height(node):
            if node == tree.NIL:
                return 0
            return 1 + max(height(node.left), height(node.right))
        
        h = height(tree.root)
        
        # Red-Black tree height should be at most 2*log2(n+1)
        import math
        max_height = 2 * math.log2(n + 1)
        
        self.assertLessEqual(h, max_height)
    
    def test_operations_complete_quickly(self):
        """Test that operations complete in reasonable time."""
        import time
        
        tree = RBTree()
        n = 10000
        
        # Time insertions
        start = time.time()
        for i in range(n):
            tree.insert(i)
        insert_time = time.time() - start
        
        # Time searches
        start = time.time()
        for i in range(0, n, 10):
            tree.search(i)
        search_time = time.time() - start
        
        # Time deletions
        start = time.time()
        for i in range(0, n, 10):
            tree.delete(i)
        delete_time = time.time() - start
        
        # Operations should complete in reasonable time
        self.assertLess(insert_time, 3.0, "Insertions took too long")
        self.assertLess(search_time, 0.5, "Searches took too long")
        self.assertLess(delete_time, 0.5, "Deletions took too long")


class TestRBTreeConsistency(unittest.TestCase):
    """Test internal consistency of the tree structure."""
    
    def test_parent_pointers_correct(self):
        """Test that parent pointers are correctly maintained."""
        tree = RBTree()
        keys = list(range(1, 101))
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        def check_parents(node):
            if node == tree.NIL:
                return True
            
            # Check left child's parent pointer
            if node.left != tree.NIL:
                self.assertEqual(node.left.parent, node)
            
            # Check right child's parent pointer
            if node.right != tree.NIL:
                self.assertEqual(node.right.parent, node)
            
            return check_parents(node.left) and check_parents(node.right)
        
        self.assertTrue(check_parents(tree.root))
    
    def test_no_cycles(self):
        """Test that there are no cycles in the tree structure."""
        tree = RBTree()
        keys = list(range(1, 201))
        random.shuffle(keys)
        
        for key in keys:
            tree.insert(key)
        
        visited = set()
        
        def check_no_cycles(node):
            if node == tree.NIL:
                return True
            
            # Check if we've seen this node before
            node_id = id(node)
            self.assertNotIn(node_id, visited)
            visited.add(node_id)
            
            return check_no_cycles(node.left) and check_no_cycles(node.right)
        
        self.assertTrue(check_no_cycles(tree.root))
    
    def test_node_count_consistency(self):
        """Test that node count is consistent after operations."""
        tree = RBTree()
        keys = list(range(1, 501))
        
        for key in keys:
            tree.insert(key)
        
        def count_nodes(node):
            if node == tree.NIL:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        self.assertEqual(count_nodes(tree.root), 500)
        
        # Delete 250 nodes
        to_delete = random.sample(keys, 250)
        for key in to_delete:
            tree.delete(key)
        
        self.assertEqual(count_nodes(tree.root), 250)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)