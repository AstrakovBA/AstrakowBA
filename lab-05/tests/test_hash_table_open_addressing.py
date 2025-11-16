"""
Unit-тесты для хеш-таблицы с открытой адресацией.
"""

import unittest
from src.modules.hash_table_open_addressing import HashTableOpenAddressing


class TestHashTableOpenAddressing(unittest.TestCase):
    """Тесты для хеш-таблицы с открытой адресацией."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.table_linear = HashTableOpenAddressing(
            initial_size=10, 
            hash_function='djb2',
            probing_method='linear'
        )
        self.table_double = HashTableOpenAddressing(
            initial_size=10,
            hash_function='djb2',
            probing_method='double'
        )
    
    def test_insert_and_get_linear(self):
        """Тест вставки и получения элементов (линейное пробирование)."""
        self.table_linear.insert("key1", "value1")
        self.table_linear.insert("key2", "value2")
        
        self.assertEqual(self.table_linear.get("key1"), "value1")
        self.assertEqual(self.table_linear.get("key2"), "value2")
        self.assertIsNone(self.table_linear.get("nonexistent"))
    
    def test_insert_and_get_double(self):
        """Тест вставки и получения элементов (двойное хеширование)."""
        self.table_double.insert("key1", "value1")
        self.table_double.insert("key2", "value2")
        
        self.assertEqual(self.table_double.get("key1"), "value1")
        self.assertEqual(self.table_double.get("key2"), "value2")
        self.assertIsNone(self.table_double.get("nonexistent"))
    
    def test_update_existing_key(self):
        """Тест обновления существующего ключа."""
        self.table_linear.insert("key1", "value1")
        self.table_linear.insert("key1", "new_value")
        
        self.assertEqual(self.table_linear.get("key1"), "new_value")
        self.assertEqual(self.table_linear.count, 1)
    
    def test_delete_linear(self):
        """Тест удаления элементов (линейное пробирование)."""
        self.table_linear.insert("key1", "value1")
        self.table_linear.insert("key2", "value2")
        
        self.assertTrue(self.table_linear.delete("key1"))
        self.assertIsNone(self.table_linear.get("key1"))
        self.assertEqual(self.table_linear.get("key2"), "value2")
        self.assertFalse(self.table_linear.delete("nonexistent"))
    
    def test_delete_double(self):
        """Тест удаления элементов (двойное хеширование)."""
        self.table_double.insert("key1", "value1")
        self.table_double.insert("key2", "value2")
        
        self.assertTrue(self.table_double.delete("key1"))
        self.assertIsNone(self.table_double.get("key1"))
        self.assertEqual(self.table_double.get("key2"), "value2")
    
    def test_delete_and_reinsert(self):
        """Тест повторной вставки после удаления."""
        self.table_linear.insert("key1", "value1")
        self.table_linear.delete("key1")
        self.table_linear.insert("key1", "value2")
        
        self.assertEqual(self.table_linear.get("key1"), "value2")
    
    def test_contains(self):
        """Тест проверки наличия ключа."""
        self.table_linear.insert("key1", "value1")
        
        self.assertTrue(self.table_linear.contains("key1"))
        self.assertFalse(self.table_linear.contains("nonexistent"))
    
    def test_collision_handling(self):
        """Тест обработки коллизий."""
        # Вставляем несколько элементов
        for i in range(20):
            self.table_linear.insert(f"key{i}", f"value{i}")
            self.table_double.insert(f"key{i}", f"value{i}")
        
        # Проверяем, что все элементы доступны
        for i in range(20):
            self.assertEqual(self.table_linear.get(f"key{i}"), f"value{i}")
            self.assertEqual(self.table_double.get(f"key{i}"), f"value{i}")
    
    def test_resize(self):
        """Тест автоматического увеличения размера."""
        initial_size = self.table_linear.size
        
        # Вставляем много элементов, чтобы вызвать рехеширование
        for i in range(100):
            self.table_linear.insert(f"key{i}", f"value{i}")
        
        # Размер должен увеличиться
        self.assertGreater(self.table_linear.size, initial_size)
        
        # Все элементы должны быть доступны
        for i in range(100):
            self.assertEqual(self.table_linear.get(f"key{i}"), f"value{i}")
    
    def test_statistics(self):
        """Тест получения статистики."""
        for i in range(10):
            self.table_linear.insert(f"key{i}", f"value{i}")
        
        stats = self.table_linear.get_statistics()
        
        self.assertIn('size', stats)
        self.assertIn('count', stats)
        self.assertIn('deleted_count', stats)
        self.assertIn('load_factor', stats)
        self.assertIn('empty_slots', stats)
        self.assertIn('collisions', stats)
        
        self.assertEqual(stats['count'], 10)
        self.assertGreaterEqual(stats['load_factor'], 0)
        self.assertLessEqual(stats['load_factor'], 1)
    
    def test_different_hash_functions(self):
        """Тест работы с разными хеш-функциями."""
        for hash_func in ['simple', 'polynomial', 'djb2']:
            table = HashTableOpenAddressing(hash_function=hash_func)
            table.insert("key1", "value1")
            self.assertEqual(table.get("key1"), "value1")
    
    def test_empty_table(self):
        """Тест работы с пустой таблицей."""
        stats = self.table_linear.get_statistics()
        self.assertEqual(stats['count'], 0)
        self.assertEqual(stats['load_factor'], 0)
        self.assertIsNone(self.table_linear.get("any_key"))
    
    def test_invalid_initialization(self):
        """Тест обработки неверных параметров инициализации."""
        with self.assertRaises(ValueError):
            HashTableOpenAddressing(initial_size=0)
        
        with self.assertRaises(ValueError):
            HashTableOpenAddressing(load_factor_threshold=1.5)
        
        with self.assertRaises(ValueError):
            HashTableOpenAddressing(hash_function='unknown')
        
        with self.assertRaises(ValueError):
            HashTableOpenAddressing(probing_method='unknown')


if __name__ == '__main__':
    unittest.main()


