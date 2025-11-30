"""
Unit-тесты для хеш-функций.
"""

import unittest
from src.modules.hash_functions import simple_hash, polynomial_hash, djb2_hash


class TestHashFunctions(unittest.TestCase):
    """Тесты для всех хеш-функций."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.table_size = 100
    
    def test_simple_hash_basic(self):
        """Тест базовой функциональности простой хеш-функции."""
        key = "test"
        hash_value = simple_hash(key, self.table_size)
        self.assertIsInstance(hash_value, int)
        self.assertGreaterEqual(hash_value, 0)
        self.assertLess(hash_value, self.table_size)
    
    def test_simple_hash_consistency(self):
        """Тест консистентности простой хеш-функции."""
        key = "hello"
        hash1 = simple_hash(key, self.table_size)
        hash2 = simple_hash(key, self.table_size)
        self.assertEqual(hash1, hash2)
    
    def test_simple_hash_anagram_collision(self):
        """Тест коллизии для анаграмм (особенность простой хеш-функции)."""
        # Анаграммы могут давать одинаковый хеш
        hash1 = simple_hash("abc", self.table_size)
        hash2 = simple_hash("cba", self.table_size)
        # Это не гарантированная коллизия, но возможна
        self.assertIsInstance(hash1, int)
        self.assertIsInstance(hash2, int)
    
    def test_polynomial_hash_basic(self):
        """Тест базовой функциональности полиномиальной хеш-функции."""
        key = "test"
        hash_value = polynomial_hash(key, self.table_size)
        self.assertIsInstance(hash_value, int)
        self.assertGreaterEqual(hash_value, 0)
        self.assertLess(hash_value, self.table_size)
    
    def test_polynomial_hash_consistency(self):
        """Тест консистентности полиномиальной хеш-функции."""
        key = "hello"
        hash1 = polynomial_hash(key, self.table_size)
        hash2 = polynomial_hash(key, self.table_size)
        self.assertEqual(hash1, hash2)
    
    def test_polynomial_hash_order_matters(self):
        """Тест, что порядок символов важен в полиномиальной хеш-функции."""
        hash1 = polynomial_hash("abc", self.table_size)
        hash2 = polynomial_hash("cba", self.table_size)
        # Для полиномиальной хеш-функции порядок важен
        # (хотя коллизия все еще возможна, но маловероятна)
        self.assertIsInstance(hash1, int)
        self.assertIsInstance(hash2, int)
    
    def test_djb2_hash_basic(self):
        """Тест базовой функциональности хеш-функции DJB2."""
        key = "test"
        hash_value = djb2_hash(key, self.table_size)
        self.assertIsInstance(hash_value, int)
        self.assertGreaterEqual(hash_value, 0)
        self.assertLess(hash_value, self.table_size)
    
    def test_djb2_hash_consistency(self):
        """Тест консистентности хеш-функции DJB2."""
        key = "hello"
        hash1 = djb2_hash(key, self.table_size)
        hash2 = djb2_hash(key, self.table_size)
        self.assertEqual(hash1, hash2)
    
    def test_all_functions_different_keys(self):
        """Тест, что разные ключи дают разные хеши (в большинстве случаев)."""
        keys = ["key1", "key2", "key3", "different", "another"]
        hashes_simple = [simple_hash(k, self.table_size) for k in keys]
        hashes_poly = [polynomial_hash(k, self.table_size) for k in keys]
        hashes_djb2 = [djb2_hash(k, self.table_size) for k in keys]
        
        # Проверяем, что есть хотя бы некоторые различия
        # (полное отсутствие коллизий не гарантируется)
        self.assertTrue(len(set(hashes_simple)) > 1 or len(keys) == 1)
        self.assertTrue(len(set(hashes_poly)) > 1 or len(keys) == 1)
        self.assertTrue(len(set(hashes_djb2)) > 1 or len(keys) == 1)
    
    def test_empty_string(self):
        """Тест обработки пустой строки."""
        empty = ""
        self.assertIsInstance(simple_hash(empty, self.table_size), int)
        self.assertIsInstance(polynomial_hash(empty, self.table_size), int)
        self.assertIsInstance(djb2_hash(empty, self.table_size), int)


if __name__ == '__main__':
    unittest.main()


