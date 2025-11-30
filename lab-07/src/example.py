"""
Простой пример использования модулей кучи.
"""

from modules.heap import MinHeap, MaxHeap
from modules.heapsort import heapsort, heapsort_inplace
from modules.priority_queue import PriorityQueue


def example_heap():
    """Пример работы с кучей."""
    print("="*60)
    print("Пример 1: Работа с MinHeap")
    print("="*60)
    
    # Создаем min-heap
    heap = MinHeap()
    values = [9, 5, 7, 3, 1, 8, 2, 6, 4]
    
    print(f"Исходный массив: {values}")
    print("Вставляем элементы...")
    for value in values:
        heap.insert(value)
    
    print(f"Куча: {heap}")
    print("\nИзвлечение элементов (по возрастанию):")
    while not heap.is_empty():
        print(f"  {heap.extract()}", end=" ")
    print("\n")
    
    print("="*60)
    print("Пример 2: Построение кучи из массива")
    print("="*60)
    
    array = [9, 5, 7, 3, 1, 8, 2, 6, 4]
    heap = MinHeap(initial_array=array)
    print(f"Массив: {array}")
    print(f"Куча: {heap}")
    print("Извлечение элементов:")
    result = []
    while not heap.is_empty():
        result.append(heap.extract())
    print(f"Результат: {result}")


def example_heapsort():
    """Пример работы с heapsort."""
    print("\n" + "="*60)
    print("Пример 3: Сортировка кучей")
    print("="*60)
    
    array = [9, 5, 7, 3, 1, 8, 2, 6, 4]
    print(f"Исходный массив: {array}")
    
    # Обычная сортировка
    sorted_array = heapsort(array)
    print(f"Отсортированный массив (heapsort): {sorted_array}")
    
    # In-place сортировка
    array_copy = list(array)
    heapsort_inplace(array_copy)
    print(f"Отсортированный массив (heapsort_inplace): {array_copy}")


def example_priority_queue():
    """Пример работы с приоритетной очередью."""
    print("\n" + "="*60)
    print("Пример 4: Приоритетная очередь")
    print("="*60)
    
    pq = PriorityQueue()
    
    # Добавляем задачи с приоритетами
    tasks = [
        ("Задача 1", 3),
        ("Задача 2", 1),
        ("Задача 3", 2),
        ("Задача 4", 1),
        ("Задача 5", 4),
    ]
    
    print("Добавляем задачи:")
    for task, priority in tasks:
        pq.enqueue(task, priority)
        print(f"  {task} (приоритет: {priority})")
    
    print(f"\nРазмер очереди: {pq.size()}")
    print(f"Следующая задача: {pq.peek()}")
    
    print("\nИзвлечение задач (по приоритету):")
    while not pq.is_empty():
        task = pq.dequeue()
        print(f"  Выполняется: {task}")


if __name__ == '__main__':
    example_heap()
    example_heapsort()
    example_priority_queue()


