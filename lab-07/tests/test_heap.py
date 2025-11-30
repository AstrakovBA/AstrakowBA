"""
Unit-тесты для модуля heap.
"""

import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.heap import Heap, MinHeap, MaxHeap


class TestHeap(unittest.TestCase):
    """Тесты для класса Heap."""
    
    def test_min_heap_insert_extract(self):
        """Тест вставки и извлечения в min-heap."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        heap.insert(1)
        heap.insert(9)
        
        self.assertEqual(heap.extract(), 1)
        self.assertEqual(heap.extract(), 3)
        self.assertEqual(heap.extract(), 5)
        self.assertEqual(heap.extract(), 7)
        self.assertEqual(heap.extract(), 9)
    
    def test_max_heap_insert_extract(self):
        """Тест вставки и извлечения в max-heap."""
        heap = MaxHeap()
        heap.insert(5)
        heap.insert(3)
        heap.insert(7)
        heap.insert(1)
        heap.insert(9)
        
        self.assertEqual(heap.extract(), 9)
        self.assertEqual(heap.extract(), 7)
        self.assertEqual(heap.extract(), 5)
        self.assertEqual(heap.extract(), 3)
        self.assertEqual(heap.extract(), 1)
    
    def test_peek(self):
        """Тест просмотра корня без извлечения."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(3)
        
        self.assertEqual(heap.peek(), 3)
        self.assertEqual(heap.size(), 2)  # Размер не изменился
        self.assertEqual(heap.extract(), 3)
    
    def test_build_heap_min(self):
        """Тест построения min-heap из массива."""
        array = [9, 5, 7, 3, 1, 8, 2, 6, 4]
        heap = MinHeap(initial_array=array)
        
        # Проверяем, что элементы извлекаются в правильном порядке
        result = []
        while not heap.is_empty():
            result.append(heap.extract())
        
        self.assertEqual(result, sorted(array))
    
    def test_build_heap_max(self):
        """Тест построения max-heap из массива."""
        array = [9, 5, 7, 3, 1, 8, 2, 6, 4]
        heap = MaxHeap(initial_array=array)
        
        # Проверяем, что элементы извлекаются в правильном порядке
        result = []
        while not heap.is_empty():
            result.append(heap.extract())
        
        self.assertEqual(result, sorted(array, reverse=True))
    
    def test_empty_heap(self):
        """Тест работы с пустой кучей."""
        heap = MinHeap()
        
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size(), 0)
        
        with self.assertRaises(IndexError):
            heap.extract()
        
        with self.assertRaises(IndexError):
            heap.peek()
    
    def test_heap_property_after_operations(self):
        """Тест сохранения свойства кучи после операций."""
        heap = MinHeap()
        
        # Добавляем элементы
        for i in [5, 2, 8, 1, 9, 3, 7, 4, 6]:
            heap.insert(i)
        
        # После каждой операции извлечения свойство кучи должно сохраняться
        prev = heap.extract()
        while not heap.is_empty():
            current = heap.extract()
            self.assertGreaterEqual(current, prev)
            prev = current
    
    def test_single_element(self):
        """Тест работы с одним элементом."""
        heap = MinHeap()
        heap.insert(42)
        
        self.assertEqual(heap.size(), 1)
        self.assertEqual(heap.peek(), 42)
        self.assertEqual(heap.extract(), 42)
        self.assertTrue(heap.is_empty())
    
    def test_duplicate_elements(self):
        """Тест работы с дублирующимися элементами."""
        heap = MinHeap()
        heap.insert(5)
        heap.insert(3)
        heap.insert(5)
        heap.insert(3)
        heap.insert(5)
        
        result = []
        while not heap.is_empty():
            result.append(heap.extract())
        
        self.assertEqual(result, [3, 3, 5, 5, 5])


if __name__ == '__main__':
    unittest.main()


