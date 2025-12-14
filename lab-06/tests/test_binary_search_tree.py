"""
Unit-тесты для бинарного дерева поиска.
"""

import unittest
from src.modules.binary_search_tree import BinarySearchTree, TreeNode


class TestTreeNode(unittest.TestCase):
    """Тесты для класса TreeNode."""
    
    def test_node_creation(self):
        """Тест создания узла."""
        node = TreeNode(5)
        self.assertEqual(node.value, 5)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)


class TestBinarySearchTree(unittest.TestCase):
    """Тесты для класса BinarySearchTree."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.tree = BinarySearchTree()
    
    def test_empty_tree(self):
        """Тест пустого дерева."""
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)
        self.assertEqual(self.tree.size(), 0)
        self.assertEqual(self.tree.height(), -1)
    
    def test_insert_single(self):
        """Тест вставки одного элемента."""
        self.tree.insert(5)
        self.assertFalse(self.tree.is_empty())
        self.assertEqual(self.tree.root.value, 5)
        self.assertEqual(self.tree.size(), 1)
        self.assertEqual(self.tree.height(), 0)
    
    def test_insert_multiple(self):
        """Тест вставки нескольких элементов."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        self.assertEqual(self.tree.size(), 7)
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_insert_duplicate(self):
        """Тест вставки дубликатов."""
        self.tree.insert(5)
        self.tree.insert(5)  # Дубликат
        self.assertEqual(self.tree.size(), 1)  # Дубликат не должен быть добавлен
    
    def test_search_existing(self):
        """Тест поиска существующего элемента."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        node = self.tree.search(4)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 4)
    
    def test_search_non_existing(self):
        """Тест поиска несуществующего элемента."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        node = self.tree.search(10)
        self.assertIsNone(node)
    
    def test_search_empty_tree(self):
        """Тест поиска в пустом дереве."""
        node = self.tree.search(5)
        self.assertIsNone(node)
    
    def test_find_min(self):
        """Тест поиска минимума."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        min_node = self.tree.find_min()
        self.assertIsNotNone(min_node)
        self.assertEqual(min_node.value, 2)
    
    def test_find_max(self):
        """Тест поиска максимума."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        max_node = self.tree.find_max()
        self.assertIsNotNone(max_node)
        self.assertEqual(max_node.value, 8)
    
    def test_find_min_max_empty(self):
        """Тест поиска мин/макс в пустом дереве."""
        self.assertIsNone(self.tree.find_min())
        self.assertIsNone(self.tree.find_max())
    
    def test_delete_leaf(self):
        """Тест удаления листа."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        self.tree.delete(2)
        self.assertEqual(self.tree.size(), 6)
        self.assertIsNone(self.tree.search(2))
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_delete_node_with_one_child(self):
        """Тест удаления узла с одним ребенком."""
        values = [5, 3, 7, 2, 6]
        for value in values:
            self.tree.insert(value)
        
        self.tree.delete(7)
        self.assertEqual(self.tree.size(), 4)
        self.assertIsNone(self.tree.search(7))
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_delete_node_with_two_children(self):
        """Тест удаления узла с двумя детьми."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        self.tree.delete(5)  # Корень с двумя детьми
        self.assertEqual(self.tree.size(), 6)
        self.assertIsNone(self.tree.search(5))
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_delete_root(self):
        """Тест удаления корня."""
        self.tree.insert(5)
        self.tree.delete(5)
        self.assertTrue(self.tree.is_empty())
        self.assertEqual(self.tree.size(), 0)
    
    def test_delete_non_existing(self):
        """Тест удаления несуществующего элемента."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        initial_size = self.tree.size()
        self.tree.delete(10)  # Несуществующий элемент
        self.assertEqual(self.tree.size(), initial_size)
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_is_valid_bst_valid(self):
        """Тест проверки корректного BST."""
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_is_valid_bst_empty(self):
        """Тест проверки пустого дерева."""
        self.assertTrue(self.tree.is_valid_bst())
    
    def test_height(self):
        """Тест вычисления высоты."""
        # Пустое дерево
        self.assertEqual(self.tree.height(), -1)
        
        # Один элемент
        self.tree.insert(5)
        self.assertEqual(self.tree.height(), 0)
        
        # Несколько элементов
        values = [5, 3, 7, 2, 4, 6, 8]
        self.tree = BinarySearchTree()
        for value in values:
            self.tree.insert(value)
        
        height = self.tree.height()
        self.assertGreaterEqual(height, 2)
        self.assertLessEqual(height, 6)
    
    def test_size(self):
        """Тест подсчета размера."""
        self.assertEqual(self.tree.size(), 0)
        
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
        
        self.assertEqual(self.tree.size(), 7)
    
    def test_visualize(self):
        """Тест визуализации."""
        values = [5, 3, 7, 2, 4]
        for value in values:
            self.tree.insert(value)
        
        visualization = self.tree.visualize()
        self.assertIsInstance(visualization, str)
        self.assertIn("5", visualization)
    
    def test_to_bracket_notation(self):
        """Тест скобочной нотации."""
        values = [5, 3, 7]
        for value in values:
            self.tree.insert(value)
        
        bracket = self.tree.to_bracket_notation()
        self.assertIsInstance(bracket, str)
        self.assertIn("5", bracket)
    
    def test_properties_after_operations(self):
        """Тест сохранения свойств BST после операций."""
        values = [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 9, 11, 13, 16, 20]
        for value in values:
            self.tree.insert(value)
        
        # Проверяем свойства после вставки
        self.assertTrue(self.tree.is_valid_bst())
        
        # Удаляем несколько элементов
        to_delete = [5, 15, 1, 20]
        for value in to_delete:
            self.tree.delete(value)
            self.assertTrue(self.tree.is_valid_bst())


if __name__ == '__main__':
    unittest.main()

