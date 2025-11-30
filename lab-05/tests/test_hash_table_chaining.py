"""
Unit-тесты для хеш-таблицы с методом цепочек.
"""

import unittest
from src.modules.hash_table_chaining import HashTableChaining


class TestHashTableChaining(unittest.TestCase):
    """Тесты для хеш-таблицы с методом цепочек."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.table = HashTableChaining(initial_size=10, hash_function='djb2')
    
    def test_insert_and_get(self):
        """Тест вставки и получения элементов."""
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        
        self.assertEqual(self.table.get("key1"), "value1")
        self.assertEqual(self.table.get("key2"), "value2")
        self.assertIsNone(self.table.get("nonexistent"))
    
    def test_update_existing_key(self):
        """Тест обновления существующего ключа."""
        self.table.insert("key1", "value1")
        self.table.insert("key1", "new_value")
        
        self.assertEqual(self.table.get("key1"), "new_value")
        self.assertEqual(self.table.count, 1)
    
    def test_delete(self):
        """Тест удаления элементов."""
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        
        self.assertTrue(self.table.delete("key1"))
        self.assertIsNone(self.table.get("key1"))
        self.assertEqual(self.table.get("key2"), "value2")
        self.assertFalse(self.table.delete("nonexistent"))
    
    def test_contains(self):
        """Тест проверки наличия ключа."""
        self.table.insert("key1", "value1")
        
        self.assertTrue(self.table.contains("key1"))
        self.assertFalse(self.table.contains("nonexistent"))
    
    def test_collision_handling(self):
        """Тест обработки коллизий."""
        # Вставляем несколько элементов, которые могут вызвать коллизии
        for i in range(20):
            self.table.insert(f"key{i}", f"value{i}")
        
        # Проверяем, что все элементы доступны
        for i in range(20):
            self.assertEqual(self.table.get(f"key{i}"), f"value{i}")
    
    def test_resize(self):
        """Тест автоматического увеличения размера."""
        initial_size = self.table.size
        
        # Вставляем много элементов, чтобы вызвать рехеширование
        for i in range(100):
            self.table.insert(f"key{i}", f"value{i}")
        
        # Размер должен увеличиться
        self.assertGreater(self.table.size, initial_size)
        
        # Все элементы должны быть доступны
        for i in range(100):
            self.assertEqual(self.table.get(f"key{i}"), f"value{i}")
    
    def test_statistics(self):
        """Тест получения статистики."""
        for i in range(10):
            self.table.insert(f"key{i}", f"value{i}")
        
        stats = self.table.get_statistics()
        
        self.assertIn('size', stats)
        self.assertIn('count', stats)
        self.assertIn('load_factor', stats)
        self.assertIn('max_chain_length', stats)
        self.assertIn('avg_chain_length', stats)
        self.assertIn('empty_slots', stats)
        self.assertIn('collisions', stats)
        
        self.assertEqual(stats['count'], 10)
        self.assertGreaterEqual(stats['load_factor'], 0)
        self.assertLessEqual(stats['load_factor'], 1)
    
    def test_different_hash_functions(self):
        """Тест работы с разными хеш-функциями."""
        for hash_func in ['simple', 'polynomial', 'djb2']:
            table = HashTableChaining(hash_function=hash_func)
            table.insert("key1", "value1")
            self.assertEqual(table.get("key1"), "value1")
    
    def test_empty_table(self):
        """Тест работы с пустой таблицей."""
        stats = self.table.get_statistics()
        self.assertEqual(stats['count'], 0)
        self.assertEqual(stats['load_factor'], 0)
        self.assertIsNone(self.table.get("any_key"))
    
    def test_invalid_initialization(self):
        """Тест обработки неверных параметров инициализации."""
        with self.assertRaises(ValueError):
            HashTableChaining(initial_size=0)
        
        with self.assertRaises(ValueError):
            HashTableChaining(load_factor_threshold=1.5)
        
        with self.assertRaises(ValueError):
            HashTableChaining(hash_function='unknown')


if __name__ == '__main__':
    unittest.main()


