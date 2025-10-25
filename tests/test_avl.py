"""
Unit tests for AVL Tree implementation.

This module provides comprehensive testing for the AVL Tree data structure,
including insertion, deletion, search, traversals, and balance validation.
"""

import unittest
import random
import sys
import os

# Add parent directory to path to import avl module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_structures.avl import AVLTree, AVLNode


class TestAVLNode(unittest.TestCase):
    """Test cases for AVLNode class."""
    
    def test_node_creation(self):
        """Test that a node is created with correct initial values."""
        node = AVLNode(10, "value10")
        self.assertEqual(node.key, 10)
        self.assertEqual(node.value, "value10")
        # Child pointers should be None initially
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        # Height of a new node is always 1 (leaf node)
        self.assertEqual(node.height, 1)
    
    def test_node_creation_without_value(self):
        """Test node creation with only a key."""
        node = AVLNode(5)
        self.assertEqual(node.key, 5)
        # Value should be None if not provided
        self.assertIsNone(node.value)


class TestAVLTreeBasicOperations(unittest.TestCase):
    """Test basic operations: insert, search, delete."""
    
    def setUp(self):
        """Initialize a fresh AVL tree before each test."""
        self.tree = AVLTree()
    
    def test_empty_tree(self):
        """Test operations on an empty tree."""
        # Empty tree should have no root
        self.assertIsNone(self.tree.root)
        # Searching in empty tree should return None
        self.assertIsNone(self.tree.search(1))
        # In-order traversal of empty tree should be empty list
        self.assertEqual(self.tree.inorder(), [])
    
    def test_single_insertion(self):
        """Test inserting a single element."""
        self.tree.insert(10)
        # Root should now exist
        self.assertIsNotNone(self.tree.root)
        # Root key should be 10
        self.assertEqual(self.tree.root.key, 10)
        # Root height should be 1 (single node)
        self.assertEqual(self.tree.root.height, 1)
    
    def test_multiple_insertions(self):
        """Test inserting multiple elements."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            self.tree.insert(key)
        
        # Verify all keys can be found
        for key in keys:
            self.assertIsNotNone(self.tree.search(key))
    
    def test_insertion_with_values(self):
        """Test inserting key-value pairs."""
        self.tree.insert(1, "one")
        self.tree.insert(2, "two")
        self.tree.insert(3, "three")
        
        # Values should be stored and retrievable
        self.assertEqual(self.tree.search(1), "one")
        self.assertEqual(self.tree.search(2), "two")
        self.assertEqual(self.tree.search(3), "three")
    
    def test_duplicate_insertion(self):
        """Test that duplicate keys update the value."""
        self.tree.insert(10, "first")
        self.tree.insert(10, "second")
        
        # Value should be updated to "second"
        self.assertEqual(self.tree.search(10), "second")
        # Tree should still have only one node with key 10 (no duplicates)
        inorder = self.tree.inorder()
        self.assertEqual(len(inorder), 1)
    
    def test_search_nonexistent(self):
        """Test searching for keys that don't exist."""
        self.tree.insert(10)
        self.tree.insert(20)
        
        # Non-existent keys should return None
        self.assertIsNone(self.tree.search(5))
        self.assertIsNone(self.tree.search(15))
        self.assertIsNone(self.tree.search(25))
    
    def test_delete_single_node(self):
        """Test deleting the only node in the tree."""
        self.tree.insert(10)
        self.tree.delete(10)
        
        # After deletion, tree should be empty
        self.assertIsNone(self.tree.root)
        # Key should no longer be searchable
        self.assertIsNone(self.tree.search(10))
    
    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        self.tree.insert(20)
        self.tree.insert(10)
        self.tree.insert(30)
        self.tree.delete(10)
        
        # Deleted key should not be found
        self.assertIsNone(self.tree.search(10))
        # Other keys should still exist
        self.assertIsNotNone(self.tree.search(20))
        self.assertIsNotNone(self.tree.search(30))
    
    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        self.tree.insert(20)
        self.tree.insert(10)
        self.tree.insert(5)
        self.tree.delete(10)
        
        # Deleted node should not be found
        self.assertIsNone(self.tree.search(10))
        # Remaining nodes should still be accessible
        self.assertIsNotNone(self.tree.search(20))
        self.assertIsNotNone(self.tree.search(5))
    
    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        keys = [20, 10, 30, 5, 15, 25, 35]
        for key in keys:
            self.tree.insert(key)
        
        self.tree.delete(20)
        # Node should be deleted
        self.assertIsNone(self.tree.search(20))
        
        # All other keys should still be present
        for key in [10, 30, 5, 15, 25, 35]:
            self.assertIsNotNone(self.tree.search(key))
    
    def test_delete_nonexistent(self):
        """Test deleting a key that doesn't exist."""
        self.tree.insert(10)
        self.tree.insert(20)
        
        # Should not raise error when deleting non-existent key
        self.tree.delete(30)
        
        # Original keys should still be present
        self.assertIsNotNone(self.tree.search(10))
        self.assertIsNotNone(self.tree.search(20))


class TestAVLTreeRotations(unittest.TestCase):
    """Test AVL tree rotations and balancing."""
    
    def setUp(self):
        """Initialize a fresh AVL tree before each test."""
        self.tree = AVLTree()
    
    def test_right_rotation(self):
        """Test right rotation (Left-Left case)."""
        # Insert in descending order to trigger left-left imbalance
        self.tree.insert(30)
        self.tree.insert(20)
        self.tree.insert(10)
        
        # After right rotation, root should be middle element
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)
        # Tree should be balanced after rotation
        self.assertTrue(self.tree.is_balanced())
    
    def test_left_rotation(self):
        """Test left rotation (Right-Right case)."""
        # Insert in ascending order to trigger right-right imbalance
        self.tree.insert(10)
        self.tree.insert(20)
        self.tree.insert(30)
        
        # After left rotation, root should be middle element
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)
        # Tree should be balanced after rotation
        self.assertTrue(self.tree.is_balanced())
    
    def test_left_right_rotation(self):
        """Test left-right rotation (Left-Right case)."""
        # Insert in order that causes left-right imbalance
        self.tree.insert(30)
        self.tree.insert(10)
        self.tree.insert(20)
        
        # After rotations, root should be middle element
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)
        # Tree should be balanced
        self.assertTrue(self.tree.is_balanced())
    
    def test_right_left_rotation(self):
        """Test right-left rotation (Right-Left case)."""
        # Insert in order that causes right-left imbalance
        self.tree.insert(10)
        self.tree.insert(30)
        self.tree.insert(20)
        
        # After rotations, root should be middle element
        self.assertEqual(self.tree.root.key, 20)
        self.assertEqual(self.tree.root.left.key, 10)
        self.assertEqual(self.tree.root.right.key, 30)
        # Tree should be balanced
        self.assertTrue(self.tree.is_balanced())
    
    def test_balance_after_deletion(self):
        """Test that tree rebalances after deletion."""
        keys = [10, 5, 15, 2, 7, 12, 20, 1]
        for key in keys:
            self.tree.insert(key)
        
        # Tree should be balanced after insertions
        self.assertTrue(self.tree.is_balanced())
        
        # Delete nodes and verify tree remains balanced
        self.tree.delete(1)
        self.assertTrue(self.tree.is_balanced())
        
        self.tree.delete(7)
        self.assertTrue(self.tree.is_balanced())


class TestAVLTreeTraversals(unittest.TestCase):
    """Test tree traversal methods."""
    
    def setUp(self):
        """Initialize a tree with sample data."""
        self.tree = AVLTree()
        # Insert keys: 10, 5, 15, 2, 7, 12, 20
        keys = [10, 5, 15, 2, 7, 12, 20]
        for key in keys:
            self.tree.insert(key, f"val{key}")
    
    def test_inorder_traversal(self):
        """Test in-order traversal returns sorted keys."""
        result = self.tree.inorder()
        # Extract just the keys from (key, value) tuples
        keys = [item[0] for item in result]
        
        # In-order traversal should give sorted order
        self.assertEqual(keys, sorted(keys))
        # Verify all keys are present
        self.assertEqual(keys, [2, 5, 7, 10, 12, 15, 20])
    
    def test_preorder_traversal(self):
        """Test pre-order traversal."""
        result = self.tree.preorder()
        
        # Pre-order visits root first
        self.assertEqual(result[0][0], self.tree.root.key)
        
        # Should have all 7 elements
        self.assertEqual(len(result), 7)
    
    def test_postorder_traversal(self):
        """Test post-order traversal."""
        result = self.tree.postorder()
        
        # Post-order visits root last
        self.assertEqual(result[-1][0], self.tree.root.key)
        
        # Should have all 7 elements
        self.assertEqual(len(result), 7)
    
    def test_empty_tree_traversals(self):
        """Test traversals on an empty tree."""
        empty_tree = AVLTree()
        
        # All traversals on empty tree should return empty list
        self.assertEqual(empty_tree.inorder(), [])
        self.assertEqual(empty_tree.preorder(), [])
        self.assertEqual(empty_tree.postorder(), [])


class TestAVLTreeProperties(unittest.TestCase):
    """Test AVL tree properties and invariants."""
    
    def test_height_property(self):
        """Test that node heights are correctly maintained."""
        tree = AVLTree()
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        
        # Root with 2 levels should have height 2
        self.assertEqual(tree.root.height, 2)
        
        # Leaf nodes should have height 1
        self.assertEqual(tree.root.left.height, 1)
        self.assertEqual(tree.root.right.height, 1)
    
    def test_balance_factor_bounds(self):
        """Test that balance factors stay within [-1, 1]."""
        tree = AVLTree()
        keys = list(range(1, 101))
        random.shuffle(keys)
        
        # Insert keys and verify balance after each insertion
        for key in keys:
            tree.insert(key)
            # Tree must remain balanced at all times
            self.assertTrue(tree.is_balanced())
    
    def test_bst_property(self):
        """Test that BST property is maintained (in-order is sorted)."""
        tree = AVLTree()
        keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
        
        for key in keys:
            tree.insert(key)
        
        # In-order traversal should be sorted
        inorder = [item[0] for item in tree.inorder()]
        self.assertEqual(inorder, sorted(keys))
    
    def test_balance_after_random_operations(self):
        """Test balance is maintained after random insert/delete operations."""
        tree = AVLTree()
        keys = list(range(1, 51))
        random.shuffle(keys)
        
        # Random insertions
        for key in keys[:30]:
            tree.insert(key)
            # Tree must be balanced after every insertion
            self.assertTrue(tree.is_balanced())
        
        # Random deletions
        to_delete = random.sample(keys[:30], 10)
        for key in to_delete:
            tree.delete(key)
            # Tree must be balanced after every deletion
            self.assertTrue(tree.is_balanced())


class TestAVLTreeEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_large_sequential_insertions(self):
        """Test inserting many sequential values."""
        tree = AVLTree()
        n = 1000
        
        # Insert 1000 sequential values
        for i in range(n):
            tree.insert(i)
        
        # Tree should be balanced despite sequential insertions
        self.assertTrue(tree.is_balanced())
        # All values should be present
        self.assertEqual(len(tree.inorder()), n)
    
    def test_large_reverse_insertions(self):
        """Test inserting many values in reverse order."""
        tree = AVLTree()
        n = 1000
        
        # Insert 1000 values in reverse order
        for i in range(n, 0, -1):
            tree.insert(i)
        
        # Tree should be balanced despite reverse sequential insertions
        self.assertTrue(tree.is_balanced())
        # All values should be present
        self.assertEqual(len(tree.inorder()), n)
    
    def test_large_random_insertions(self):
        """Test inserting many random values."""
        tree = AVLTree()
        keys = list(range(1000))
        random.shuffle(keys)
        
        # Insert 1000 random values
        for key in keys:
            tree.insert(key)
        
        # Tree should be balanced
        self.assertTrue(tree.is_balanced())
        # All values should be present
        self.assertEqual(len(tree.inorder()), 1000)
    
    def test_negative_keys(self):
        """Test tree with negative keys."""
        tree = AVLTree()
        keys = [-10, -5, -15, 0, 5, -20, 10]
        
        for key in keys:
            tree.insert(key)
        
        # All keys should be findable
        for key in keys:
            self.assertIsNotNone(tree.search(key))
        
        # In-order should be sorted (including negatives)
        inorder = [item[0] for item in tree.inorder()]
        self.assertEqual(inorder, sorted(keys))
    
    def test_string_keys(self):
        """Test tree with string keys."""
        tree = AVLTree()
        keys = ["dog", "cat", "elephant", "ant", "zebra"]
        
        for key in keys:
            tree.insert(key, key.upper())
        
        # Values should be associated correctly
        for key in keys:
            self.assertEqual(tree.search(key), key.upper())
        
        # In-order should be alphabetically sorted
        inorder = [item[0] for item in tree.inorder()]
        self.assertEqual(inorder, sorted(keys))
    
    def test_delete_all_nodes(self):
        """Test deleting all nodes from the tree."""
        tree = AVLTree()
        keys = [10, 5, 15, 2, 7, 12, 20]
        
        for key in keys:
            tree.insert(key)
        
        # Delete all nodes one by one
        for key in keys:
            tree.delete(key)
        
        # Tree should be completely empty
        self.assertIsNone(tree.root)
        self.assertEqual(tree.inorder(), [])
    
    def test_alternating_insert_delete(self):
        """Test alternating insertions and deletions."""
        tree = AVLTree()
        
        for i in range(100):
            tree.insert(i)
            # Periodically delete to maintain alternating pattern
            if i % 3 == 0 and i > 0:
                tree.delete(i - 1)
            # Tree must remain balanced after every operation
            self.assertTrue(tree.is_balanced())


class TestAVLTreeStressTests(unittest.TestCase):
    """Stress tests for AVL tree."""
    
    def test_many_duplicates(self):
        """Test handling many duplicate insertions."""
        tree = AVLTree()
        
        # Insert same key 100 times
        for _ in range(100):
            tree.insert(5, "value")
        
        # Should still have only one node with that key
        self.assertEqual(len(tree.inorder()), 1)
        # Value should be accessible
        self.assertEqual(tree.search(5), "value")
    
    def test_insert_delete_cycle(self):
        """Test repeated insert and delete of same keys."""
        tree = AVLTree()
        keys = [1, 2, 3, 4, 5]
        
        # Repeat insert/delete cycle 10 times
        for _ in range(10):
            for key in keys:
                tree.insert(key)
            for key in keys:
                tree.delete(key)
        
        # After all cycles, tree should be empty
        self.assertIsNone(tree.root)
    
    def test_random_operations_sequence(self):
        """Test a random sequence of operations."""
        tree = AVLTree()
        inserted_keys = set()
        
        random.seed(42)
        for _ in range(500):
            # Randomly choose an operation
            operation = random.choice(['insert', 'delete', 'search'])
            key = random.randint(1, 100)
            
            if operation == 'insert':
                tree.insert(key)
                inserted_keys.add(key)
            elif operation == 'delete' and inserted_keys:
                tree.delete(key)
                inserted_keys.discard(key)
            elif operation == 'search':
                result = tree.search(key)
                # Verify search consistency
                if key in inserted_keys:
                    self.assertIsNotNone(result)
            
            # Tree must always be balanced
            self.assertTrue(tree.is_balanced())


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)