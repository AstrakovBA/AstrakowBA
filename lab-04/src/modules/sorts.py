"""
Модуль с реализациями алгоритмов сортировки.

Содержит 5 алгоритмов сортировки:
- Пузырьковая сортировка (Bubble Sort)
- Сортировка выбором (Selection Sort)
- Сортировка вставками (Insertion Sort)
- Сортировка слиянием (Merge Sort)
- Быстрая сортировка (Quick Sort)
"""


def bubble_sort(arr):
    """
    Пузырьковая сортировка.
    
    Временная сложность:
    - Лучший случай: O(n) - массив уже отсортирован
    - Средний случай: O(n²)
    - Худший случай: O(n²) - массив отсортирован в обратном порядке
    
    Пространственная сложность: O(1) - сортировка in-place
    
    Args:
        arr: список для сортировки (изменяется in-place)
    
    Returns:
        arr: отсортированный список (тот же объект)
    """
    n = len(arr)
    arr = arr.copy()  # Создаем копию, чтобы не изменять исходный массив
    
    for i in range(n):
        swapped = False
        # Последние i элементов уже на месте
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Если не было обменов, массив отсортирован
        if not swapped:
            break
    
    return arr


def selection_sort(arr):
    """
    Сортировка выбором.
    
    Временная сложность:
    - Лучший случай: O(n²)
    - Средний случай: O(n²)
    - Худший случай: O(n²)
    
    Пространственная сложность: O(1) - сортировка in-place
    
    Args:
        arr: список для сортировки
    
    Returns:
        arr: отсортированный список
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        # Находим минимальный элемент в оставшейся части
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Меняем местами найденный минимальный элемент с первым элементом
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def insertion_sort(arr):
    """
    Сортировка вставками.
    
    Временная сложность:
    - Лучший случай: O(n) - массив уже отсортирован
    - Средний случай: O(n²)
    - Худший случай: O(n²) - массив отсортирован в обратном порядке
    
    Пространственная сложность: O(1) - сортировка in-place
    
    Args:
        arr: список для сортировки
    
    Returns:
        arr: отсортированный список
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Сдвигаем элементы, которые больше key, на одну позицию вправо
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def merge_sort(arr):
    """
    Сортировка слиянием.
    
    Временная сложность:
    - Лучший случай: O(n log n)
    - Средний случай: O(n log n)
    - Худший случай: O(n log n)
    
    Пространственная сложность: O(n) - требуется дополнительный массив
    
    Args:
        arr: список для сортировки
    
    Returns:
        arr: отсортированный список
    """
    if len(arr) <= 1:
        return arr.copy()
    
    # Разделяем массив пополам
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Сливаем отсортированные части
    return _merge(left, right)


def _merge(left, right):
    """
    Вспомогательная функция для слияния двух отсортированных массивов.
    
    Args:
        left: левый отсортированный массив
        right: правый отсортированный массив
    
    Returns:
        result: объединенный отсортированный массив
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Добавляем оставшиеся элементы
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def quick_sort(arr):
    """
    Быстрая сортировка (Quick Sort).
    
    Временная сложность:
    - Лучший случай: O(n log n) - разделение пополам
    - Средний случай: O(n log n)
    - Худший случай: O(n²) - плохое разделение (например, уже отсортированный массив)
    
    Пространственная сложность: 
    - Лучший/средний случай: O(log n) - глубина рекурсии
    - Худший случай: O(n) - глубина рекурсии
    
    Args:
        arr: список для сортировки
    
    Returns:
        arr: отсортированный список
    """
    if len(arr) <= 1:
        return arr.copy()
    
    # Используем медиану трех для выбора опорного элемента
    pivot = _median_of_three(arr)
    left = []
    middle = []
    right = []
    
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        else:
            right.append(x)
    
    return quick_sort(left) + middle + quick_sort(right)


def _median_of_three(arr):
    """
    Выбор медианы из первого, среднего и последнего элементов.
    Помогает избежать худшего случая O(n²) для отсортированных массивов.
    
    Args:
        arr: список
    
    Returns:
        медиана из трех элементов
    """
    first = arr[0]
    middle = arr[len(arr) // 2]
    last = arr[-1]
    
    if first <= middle <= last or last <= middle <= first:
        return middle
    elif middle <= first <= last or last <= first <= middle:
        return first
    else:
        return last


