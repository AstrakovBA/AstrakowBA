"""
Unit-тесты для модуля heapsort.
"""

import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.heapsort import heapsort, heapsort_inplace


class TestHeapsort(unittest.TestCase):
    """Тесты для функции heapsort."""
    
    def test_heapsort_basic(self):
        """Тест базовой сортировки."""
        array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        result = heapsort(array)
        self.assertEqual(result, sorted(array))
    
    def test_heapsort_empty(self):
        """Тест сортировки пустого массива."""
        self.assertEqual(heapsort([]), [])
    
    def test_heapsort_single_element(self):
        """Тест сортировки массива с одним элементом."""
        self.assertEqual(heapsort([42]), [42])
    
    def test_heapsort_already_sorted(self):
        """Тест сортировки уже отсортированного массива."""
        array = [1, 2, 3, 4, 5]
        result = heapsort(array)
        self.assertEqual(result, array)
    
    def test_heapsort_reverse_sorted(self):
        """Тест сортировки обратно отсортированного массива."""
        array = [5, 4, 3, 2, 1]
        result = heapsort(array)
        self.assertEqual(result, sorted(array))
    
    def test_heapsort_duplicates(self):
        """Тест сортировки массива с дубликатами."""
        array = [5, 2, 5, 1, 2, 3, 5, 1]
        result = heapsort(array)
        self.assertEqual(result, sorted(array))
    
    def test_heapsort_negative_numbers(self):
        """Тест сортировки с отрицательными числами."""
        array = [-5, 2, -8, 1, -9, 3, 7, -4, 6]
        result = heapsort(array)
        self.assertEqual(result, sorted(array))
    
    def test_heapsort_inplace_basic(self):
        """Тест базовой in-place сортировки."""
        array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        original_array = list(array)
        result = heapsort_inplace(array)
        
        self.assertEqual(result, sorted(original_array))
        # Проверяем, что массив был изменен на месте
        self.assertEqual(array, sorted(original_array))
    
    def test_heapsort_inplace_empty(self):
        """Тест in-place сортировки пустого массива."""
        array = []
        result = heapsort_inplace(array)
        self.assertEqual(result, [])
    
    def test_heapsort_inplace_single_element(self):
        """Тест in-place сортировки массива с одним элементом."""
        array = [42]
        result = heapsort_inplace(array)
        self.assertEqual(result, [42])
    
    def test_heapsort_inplace_large_array(self):
        """Тест in-place сортировки большого массива."""
        import random
        array = [random.randint(1, 1000) for _ in range(100)]
        original_array = list(array)
        result = heapsort_inplace(array)
        
        self.assertEqual(result, sorted(original_array))
        self.assertEqual(array, sorted(original_array))


if __name__ == '__main__':
    unittest.main()


