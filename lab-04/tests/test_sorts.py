"""
Тесты корректности алгоритмов сортировки.
"""

import unittest
import random
import sys
from pathlib import Path

# Добавляем путь к src для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modules.sorts import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort
)


class TestSorts(unittest.TestCase):
    """Тесты для всех алгоритмов сортировки."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        self.empty_array = []
        self.single_element = [42]
        self.sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.reversed_array = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.random_array = [random.randint(1, 100) for _ in range(50)]
        self.duplicates_array = [5, 2, 8, 2, 9, 1, 5, 5, 3]
        self.negative_array = [-5, -1, -10, 0, 5, 2, -3]
    
    def test_bubble_sort(self):
        """Тест пузырьковой сортировки."""
        self.assertEqual(bubble_sort(self.empty_array), [])
        self.assertEqual(bubble_sort(self.single_element), [42])
        self.assertEqual(bubble_sort(self.sorted_array), self.sorted_array)
        self.assertEqual(bubble_sort(self.reversed_array), self.sorted_array)
        self._assert_sorted(bubble_sort(self.random_array))
        self.assertEqual(bubble_sort(self.duplicates_array), sorted(self.duplicates_array))
        self.assertEqual(bubble_sort(self.negative_array), sorted(self.negative_array))
    
    def test_selection_sort(self):
        """Тест сортировки выбором."""
        self.assertEqual(selection_sort(self.empty_array), [])
        self.assertEqual(selection_sort(self.single_element), [42])
        self.assertEqual(selection_sort(self.sorted_array), self.sorted_array)
        self.assertEqual(selection_sort(self.reversed_array), self.sorted_array)
        self._assert_sorted(selection_sort(self.random_array))
        self.assertEqual(selection_sort(self.duplicates_array), sorted(self.duplicates_array))
        self.assertEqual(selection_sort(self.negative_array), sorted(self.negative_array))
    
    def test_insertion_sort(self):
        """Тест сортировки вставками."""
        self.assertEqual(insertion_sort(self.empty_array), [])
        self.assertEqual(insertion_sort(self.single_element), [42])
        self.assertEqual(insertion_sort(self.sorted_array), self.sorted_array)
        self.assertEqual(insertion_sort(self.reversed_array), self.sorted_array)
        self._assert_sorted(insertion_sort(self.random_array))
        self.assertEqual(insertion_sort(self.duplicates_array), sorted(self.duplicates_array))
        self.assertEqual(insertion_sort(self.negative_array), sorted(self.negative_array))
    
    def test_merge_sort(self):
        """Тест сортировки слиянием."""
        self.assertEqual(merge_sort(self.empty_array), [])
        self.assertEqual(merge_sort(self.single_element), [42])
        self.assertEqual(merge_sort(self.sorted_array), self.sorted_array)
        self.assertEqual(merge_sort(self.reversed_array), self.sorted_array)
        self._assert_sorted(merge_sort(self.random_array))
        self.assertEqual(merge_sort(self.duplicates_array), sorted(self.duplicates_array))
        self.assertEqual(merge_sort(self.negative_array), sorted(self.negative_array))
    
    def test_quick_sort(self):
        """Тест быстрой сортировки."""
        self.assertEqual(quick_sort(self.empty_array), [])
        self.assertEqual(quick_sort(self.single_element), [42])
        self.assertEqual(quick_sort(self.sorted_array), self.sorted_array)
        self.assertEqual(quick_sort(self.reversed_array), self.sorted_array)
        self._assert_sorted(quick_sort(self.random_array))
        self.assertEqual(quick_sort(self.duplicates_array), sorted(self.duplicates_array))
        self.assertEqual(quick_sort(self.negative_array), sorted(self.negative_array))
    
    def _assert_sorted(self, arr):
        """Проверяет, что массив отсортирован."""
        for i in range(len(arr) - 1):
            self.assertLessEqual(arr[i], arr[i + 1], 
                               f"Массив не отсортирован: {arr}")
    
    def test_all_sorts_equivalent(self):
        """Проверяет, что все алгоритмы дают одинаковый результат."""
        test_cases = [
            self.random_array,
            self.duplicates_array,
            self.negative_array,
            [random.randint(-1000, 1000) for _ in range(100)]
        ]
        
        for test_array in test_cases:
            results = [
                bubble_sort(test_array),
                selection_sort(test_array),
                insertion_sort(test_array),
                merge_sort(test_array),
                quick_sort(test_array)
            ]
            # Все результаты должны быть одинаковыми
            for i in range(1, len(results)):
                self.assertEqual(results[0], results[i], 
                               f"Алгоритмы дали разные результаты для {test_array}")


if __name__ == '__main__':
    unittest.main()


