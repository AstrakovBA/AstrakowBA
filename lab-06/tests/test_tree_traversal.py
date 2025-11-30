"""
Unit-тесты для методов обхода дерева.
"""

import unittest
from src.modules.binary_search_tree import BinarySearchTree
from src.modules.tree_traversal import (
    in_order_recursive,
    pre_order_recursive,
    post_order_recursive,
    in_order_iterative,
    pre_order_iterative,
    post_order_iterative
)


class TestTreeTraversal(unittest.TestCase):
    """Тесты для методов обхода дерева."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.tree = BinarySearchTree()
        # Создаем дерево:     5
        #                   /   \
        #                  3     7
        #                 / \   / \
        #                2   4 6   8
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
    
    def test_in_order_recursive(self):
        """Тест рекурсивного in-order обхода."""
        result = in_order_recursive(self.tree.root)
        expected = [2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(result, expected)
    
    def test_pre_order_recursive(self):
        """Тест рекурсивного pre-order обхода."""
        result = pre_order_recursive(self.tree.root)
        expected = [5, 3, 2, 4, 7, 6, 8]
        self.assertEqual(result, expected)
    
    def test_post_order_recursive(self):
        """Тест рекурсивного post-order обхода."""
        result = post_order_recursive(self.tree.root)
        expected = [2, 4, 3, 6, 8, 7, 5]
        self.assertEqual(result, expected)
    
    def test_in_order_iterative(self):
        """Тест итеративного in-order обхода."""
        result = in_order_iterative(self.tree.root)
        expected = [2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(result, expected)
    
    def test_pre_order_iterative(self):
        """Тест итеративного pre-order обхода."""
        result = pre_order_iterative(self.tree.root)
        expected = [5, 3, 2, 4, 7, 6, 8]
        self.assertEqual(result, expected)
    
    def test_post_order_iterative(self):
        """Тест итеративного post-order обхода."""
        result = post_order_iterative(self.tree.root)
        expected = [2, 4, 3, 6, 8, 7, 5]
        self.assertEqual(result, expected)
    
    def test_recursive_vs_iterative_in_order(self):
        """Сравнение рекурсивного и итеративного in-order обходов."""
        recursive_result = in_order_recursive(self.tree.root)
        iterative_result = in_order_iterative(self.tree.root)
        self.assertEqual(recursive_result, iterative_result)
    
    def test_recursive_vs_iterative_pre_order(self):
        """Сравнение рекурсивного и итеративного pre-order обходов."""
        recursive_result = pre_order_recursive(self.tree.root)
        iterative_result = pre_order_iterative(self.tree.root)
        self.assertEqual(recursive_result, iterative_result)
    
    def test_recursive_vs_iterative_post_order(self):
        """Сравнение рекурсивного и итеративного post-order обходов."""
        recursive_result = post_order_recursive(self.tree.root)
        iterative_result = post_order_iterative(self.tree.root)
        self.assertEqual(recursive_result, iterative_result)
    
    def test_empty_tree(self):
        """Тест обходов пустого дерева."""
        empty_tree = BinarySearchTree()
        
        self.assertEqual(in_order_recursive(empty_tree.root), [])
        self.assertEqual(pre_order_recursive(empty_tree.root), [])
        self.assertEqual(post_order_recursive(empty_tree.root), [])
        self.assertEqual(in_order_iterative(empty_tree.root), [])
        self.assertEqual(pre_order_iterative(empty_tree.root), [])
        self.assertEqual(post_order_iterative(empty_tree.root), [])
    
    def test_single_node(self):
        """Тест обходов дерева с одним узлом."""
        single_tree = BinarySearchTree()
        single_tree.insert(5)
        
        self.assertEqual(in_order_recursive(single_tree.root), [5])
        self.assertEqual(pre_order_recursive(single_tree.root), [5])
        self.assertEqual(post_order_recursive(single_tree.root), [5])
        self.assertEqual(in_order_iterative(single_tree.root), [5])
        self.assertEqual(pre_order_iterative(single_tree.root), [5])
        self.assertEqual(post_order_iterative(single_tree.root), [5])
    
    def test_in_order_sorted(self):
        """Тест, что in-order обход возвращает отсортированную последовательность."""
        # Создаем дерево с произвольными значениями
        tree = BinarySearchTree()
        values = [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 9, 11, 13, 16, 20]
        for value in values:
            tree.insert(value)
        
        result = in_order_recursive(tree.root)
        self.assertEqual(result, sorted(values))


if __name__ == '__main__':
    unittest.main()

