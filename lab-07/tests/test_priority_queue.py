"""
Unit-тесты для модуля priority_queue.
"""

import unittest
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.priority_queue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    """Тесты для класса PriorityQueue."""
    
    def test_enqueue_dequeue(self):
        """Тест добавления и извлечения элементов."""
        pq = PriorityQueue()
        pq.enqueue("task1", 3)
        pq.enqueue("task2", 1)
        pq.enqueue("task3", 2)
        
        # Элемент с наименьшим приоритетом должен извлекаться первым
        self.assertEqual(pq.dequeue(), "task2")  # приоритет 1
        self.assertEqual(pq.dequeue(), "task3")  # приоритет 2
        self.assertEqual(pq.dequeue(), "task1")  # приоритет 3
    
    def test_peek(self):
        """Тест просмотра элемента без извлечения."""
        pq = PriorityQueue()
        pq.enqueue("task1", 3)
        pq.enqueue("task2", 1)
        
        self.assertEqual(pq.peek(), "task2")
        self.assertEqual(pq.size(), 2)  # Размер не изменился
        self.assertEqual(pq.dequeue(), "task2")
    
    def test_empty_queue(self):
        """Тест работы с пустой очередью."""
        pq = PriorityQueue()
        
        self.assertTrue(pq.is_empty())
        self.assertEqual(pq.size(), 0)
        
        with self.assertRaises(IndexError):
            pq.dequeue()
        
        with self.assertRaises(IndexError):
            pq.peek()
    
    def test_same_priority(self):
        """Тест работы с элементами одинакового приоритета."""
        pq = PriorityQueue()
        pq.enqueue("task1", 2)
        pq.enqueue("task2", 2)
        pq.enqueue("task3", 2)
        
        # При одинаковом приоритете порядок может быть любым
        # но все элементы должны быть извлечены
        result = []
        while not pq.is_empty():
            result.append(pq.dequeue())
        
        self.assertEqual(set(result), {"task1", "task2", "task3"})
        self.assertEqual(len(result), 3)
    
    def test_priority_order(self):
        """Тест правильности порядка приоритетов."""
        pq = PriorityQueue()
        pq.enqueue("low", 10)
        pq.enqueue("high", 1)
        pq.enqueue("medium", 5)
        pq.enqueue("very_high", 0)
        
        self.assertEqual(pq.dequeue(), "very_high")
        self.assertEqual(pq.dequeue(), "high")
        self.assertEqual(pq.dequeue(), "medium")
        self.assertEqual(pq.dequeue(), "low")
    
    def test_size(self):
        """Тест размера очереди."""
        pq = PriorityQueue()
        self.assertEqual(pq.size(), 0)
        
        pq.enqueue("task1", 1)
        self.assertEqual(pq.size(), 1)
        
        pq.enqueue("task2", 2)
        self.assertEqual(pq.size(), 2)
        
        pq.dequeue()
        self.assertEqual(pq.size(), 1)
        
        pq.dequeue()
        self.assertEqual(pq.size(), 0)


if __name__ == '__main__':
    unittest.main()


