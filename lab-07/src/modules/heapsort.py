"""
Модуль для реализации алгоритма сортировки кучей (Heapsort).

Временная сложность: O(n log n) в худшем, среднем и лучшем случае.
Пространственная сложность: O(1) для in-place версии, O(n) для версии с кучей.
"""

from .heap import Heap


def heapsort(array):
    """
    Сортировка массива с использованием кучи.
    
    Временная сложность: O(n log n), где n - количество элементов.
    Пространственная сложность: O(n) для дополнительной кучи.
    
    Args:
        array: Массив для сортировки
        
    Returns:
        Отсортированный массив (по возрастанию)
    """
    if len(array) <= 1:
        return list(array)
    
    # Создаем min-heap и вставляем все элементы
    heap = Heap(is_min=True)
    for item in array:
        heap.insert(item)
    
    # Извлекаем элементы по одному - они будут в отсортированном порядке
    result = []
    while not heap.is_empty():
        result.append(heap.extract())
    
    return result


def heapsort_inplace(array):
    """
    In-place сортировка массива кучей без использования дополнительной памяти.
    
    Временная сложность: O(n log n), где n - количество элементов.
    Пространственная сложность: O(1) - сортировка выполняется на месте.
    
    Алгоритм:
    1. Преобразуем массив в max-heap
    2. На каждом шаге извлекаем максимальный элемент и помещаем его в конец
    3. Уменьшаем размер кучи и повторяем
    
    Args:
        array: Массив для сортировки (будет изменен на месте)
        
    Returns:
        Отсортированный массив (по возрастанию)
    """
    if len(array) <= 1:
        return array
    
    n = len(array)
    
    # Шаг 1: Построение max-heap из массива
    # Начинаем с последнего родительского узла
    for i in range((n - 2) // 2, -1, -1):
        _sift_down_max(array, i, n)
    
    # Шаг 2: Извлечение элементов из кучи
    # На каждом шаге максимальный элемент перемещается в конец
    for i in range(n - 1, 0, -1):
        # Меняем корень (максимум) с последним элементом
        array[0], array[i] = array[i], array[0]
        # Восстанавливаем свойство кучи для уменьшенного массива
        _sift_down_max(array, 0, i)
    
    return array


def _sift_down_max(array, index, heap_size):
    """
    Погружение элемента вниз в max-heap.
    
    Временная сложность: O(log n).
    
    Args:
        array: Массив, представляющий кучу
        index: Индекс элемента для погружения
        heap_size: Размер кучи (может быть меньше размера массива)
    """
    left_child = 2 * index + 1
    right_child = 2 * index + 2
    largest = index
    
    # Находим наибольший элемент среди текущего и его потомков
    if left_child < heap_size and array[left_child] > array[largest]:
        largest = left_child
    
    if right_child < heap_size and array[right_child] > array[largest]:
        largest = right_child
    
    # Если наибольший элемент не является текущим, меняем местами и продолжаем
    if largest != index:
        array[index], array[largest] = array[largest], array[index]
        _sift_down_max(array, largest, heap_size)


