"""
Модуль для реализации структуры данных "куча" (heap).

Реализует min-heap и max-heap на основе массива.
"""


class Heap:
    """
    Универсальная куча (min-heap или max-heap).
    
    Временная сложность операций:
    - insert: O(log n)
    - extract: O(log n)
    - peek: O(1)
    - build_heap: O(n)
    """
    
    def __init__(self, is_min=True, initial_array=None):
        """
        Инициализация кучи.
        
        Args:
            is_min: True для min-heap, False для max-heap
            initial_array: Начальный массив для построения кучи
        """
        self.is_min = is_min
        self.heap = []
        
        if initial_array:
            self.build_heap(initial_array)
    
    def _compare(self, a, b):
        """
        Сравнение элементов в зависимости от типа кучи.
        
        Args:
            a: Первый элемент
            b: Второй элемент
            
        Returns:
            True если a должен быть выше b в куче
        """
        if self.is_min:
            return a < b
        else:
            return a > b
    
    def _get_parent_index(self, index):
        """Возвращает индекс родителя. Сложность: O(1)"""
        return (index - 1) // 2
    
    def _get_left_child_index(self, index):
        """Возвращает индекс левого потомка. Сложность: O(1)"""
        return 2 * index + 1
    
    def _get_right_child_index(self, index):
        """Возвращает индекс правого потомка. Сложность: O(1)"""
        return 2 * index + 2
    
    def _sift_up(self, index):
        """
        Всплытие элемента вверх по куче.
        
        Временная сложность: O(log n), где n - количество элементов в куче.
        """
        if index == 0:
            return
        
        parent_index = self._get_parent_index(index)
        
        if self._compare(self.heap[index], self.heap[parent_index]):
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._sift_up(parent_index)
    
    def _sift_down(self, index):
        """
        Погружение элемента вниз по куче.
        
        Временная сложность: O(log n), где n - количество элементов в куче.
        """
        left_child = self._get_left_child_index(index)
        right_child = self._get_right_child_index(index)
        
        target_index = index
        
        # Находим индекс элемента, который должен быть наверху
        if left_child < len(self.heap) and self._compare(self.heap[left_child], self.heap[target_index]):
            target_index = left_child
        
        if right_child < len(self.heap) and self._compare(self.heap[right_child], self.heap[target_index]):
            target_index = right_child
        
        # Если нужно, меняем местами и продолжаем погружение
        if target_index != index:
            self.heap[index], self.heap[target_index] = self.heap[target_index], self.heap[index]
            self._sift_down(target_index)
    
    def insert(self, value):
        """
        Вставка элемента в кучу.
        
        Временная сложность: O(log n), где n - количество элементов в куче.
        
        Args:
            value: Значение для вставки
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)
    
    def extract(self):
        """
        Извлечение корня кучи (минимального или максимального элемента).
        
        Временная сложность: O(log n), где n - количество элементов в куче.
        
        Returns:
            Корневой элемент кучи
            
        Raises:
            IndexError: Если куча пуста
        """
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        
        return root
    
    def peek(self):
        """
        Просмотр корня кучи без извлечения.
        
        Временная сложность: O(1).
        
        Returns:
            Корневой элемент кучи
            
        Raises:
            IndexError: Если куча пуста
        """
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        return self.heap[0]
    
    def build_heap(self, array):
        """
        Построение кучи из произвольного массива.
        
        Временная сложность: O(n), где n - количество элементов в массиве.
        Использует алгоритм построения кучи снизу вверх.
        
        Args:
            array: Массив для построения кучи
        """
        self.heap = list(array)
        
        # Начинаем с последнего родительского узла и идем вверх
        # Последний родительский узел находится на позиции (n-2)//2
        for i in range((len(self.heap) - 2) // 2, -1, -1):
            self._sift_down(i)
    
    def size(self):
        """Возвращает размер кучи. Сложность: O(1)"""
        return len(self.heap)
    
    def is_empty(self):
        """Проверяет, пуста ли куча. Сложность: O(1)"""
        return len(self.heap) == 0
    
    def __str__(self):
        """Строковое представление кучи"""
        return str(self.heap)
    
    def __repr__(self):
        """Представление кучи для отладки"""
        heap_type = "MinHeap" if self.is_min else "MaxHeap"
        return f"{heap_type}({self.heap})"


class MinHeap(Heap):
    """Минимальная куча (min-heap)."""
    
    def __init__(self, initial_array=None):
        super().__init__(is_min=True, initial_array=initial_array)


class MaxHeap(Heap):
    """Максимальная куча (max-heap)."""
    
    def __init__(self, initial_array=None):
        super().__init__(is_min=False, initial_array=initial_array)


