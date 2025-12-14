"""
Модуль для реализации приоритетной очереди на основе кучи.

Приоритетная очередь - это структура данных, где элементы извлекаются
в порядке их приоритета (наивысший приоритет первым).
"""

from .heap import Heap


class PriorityQueue:
    """
    Приоритетная очередь на основе кучи.
    
    Элементы с меньшим значением приоритета имеют более высокий приоритет
    (извлекаются первыми).
    
    Временная сложность операций:
    - enqueue: O(log n)
    - dequeue: O(log n)
    - peek: O(1)
    """
    
    def __init__(self):
        """Инициализация приоритетной очереди."""
        # Используем min-heap, где приоритет - это значение элемента
        # Для более сложных случаев можно использовать кортежи (priority, item)
        self.heap = Heap(is_min=True)
    
    def enqueue(self, item, priority):
        """
        Добавление элемента в очередь с указанным приоритетом.
        
        Временная сложность: O(log n), где n - количество элементов в очереди.
        
        Args:
            item: Элемент для добавления
            priority: Приоритет элемента (меньшее значение = выше приоритет)
        """
        # Сохраняем как кортеж (приоритет, элемент)
        # При сравнении кортежей сначала сравнивается первый элемент
        self.heap.insert((priority, item))
    
    def dequeue(self):
        """
        Извлечение элемента с наивысшим приоритетом.
        
        Временная сложность: O(log n), где n - количество элементов в очереди.
        
        Returns:
            Элемент с наивысшим приоритетом
            
        Raises:
            IndexError: Если очередь пуста
        """
        if self.heap.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority, item = self.heap.extract()
        return item
    
    def peek(self):
        """
        Просмотр элемента с наивысшим приоритетом без извлечения.
        
        Временная сложность: O(1).
        
        Returns:
            Элемент с наивысшим приоритетом
            
        Raises:
            IndexError: Если очередь пуста
        """
        if self.heap.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority, item = self.heap.peek()
        return item
    
    def is_empty(self):
        """
        Проверка, пуста ли очередь.
        
        Временная сложность: O(1).
        
        Returns:
            True если очередь пуста, False иначе
        """
        return self.heap.is_empty()
    
    def size(self):
        """
        Возвращает количество элементов в очереди.
        
        Временная сложность: O(1).
        
        Returns:
            Количество элементов
        """
        return self.heap.size()
    
    def __str__(self):
        """Строковое представление очереди"""
        return f"PriorityQueue(size={self.size()})"
    
    def __repr__(self):
        """Представление очереди для отладки"""
        return f"PriorityQueue(size={self.size()})"


