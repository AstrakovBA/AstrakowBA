"""
Главный модуль для запуска экспериментов и визуализации.

Выполняет:
1. Экспериментальное исследование производительности
2. Сравнение алгоритмов
3. Визуализацию результатов
"""

import time
import random
import sys
import os
import numpy as np

# Добавляем путь к модулям
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from modules.heap import MinHeap
from modules.heapsort import heapsort, heapsort_inplace
from visualization import visualize_heap_tree, plot_performance_comparison, plot_complexity_analysis


def quicksort(array):
    """
    Реализация быстрой сортировки для сравнения.
    
    Временная сложность: O(n log n) в среднем, O(n²) в худшем случае.
    """
    if len(array) <= 1:
        return array
    
    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)


def mergesort(array):
    """
    Реализация сортировки слиянием для сравнения.
    
    Временная сложность: O(n log n) во всех случаях.
    """
    if len(array) <= 1:
        return array
    
    mid = len(array) // 2
    left = mergesort(array[:mid])
    right = mergesort(array[mid:])
    
    return merge(left, right)


def merge(left, right):
    """Вспомогательная функция для слияния двух отсортированных массивов."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def measure_heap_build_performance():
    """
    Измерение времени построения кучи двумя методами.
    
    Сравнивает:
    1. Последовательную вставку элементов (O(n log n))
    2. Алгоритм build_heap (O(n))
    """
    print("\n" + "="*60)
    print("Эксперимент 1: Сравнение методов построения кучи")
    print("="*60)
    
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    sequential_times = []
    build_heap_times = []
    
    for size in sizes:
        print(f"\nРазмер массива: {size}")
        
        # Генерируем случайный массив
        array = [random.randint(1, 10000) for _ in range(size)]
        
        # Метод 1: Последовательная вставка
        start_time = time.perf_counter()
        heap1 = MinHeap()
        for item in array:
            heap1.insert(item)
        sequential_time = time.perf_counter() - start_time
        sequential_times.append(sequential_time)
        print(f"  Последовательная вставка: {sequential_time:.6f} сек")
        
        # Метод 2: build_heap
        start_time = time.perf_counter()
        heap2 = MinHeap(initial_array=array)
        build_time = time.perf_counter() - start_time
        build_heap_times.append(build_time)
        print(f"  build_heap: {build_time:.6f} сек")
        print(f"  Ускорение: {sequential_time / build_time:.2f}x")
    
    return {
        'sizes': sizes,
        'sequential': sequential_times,
        'build_heap': build_heap_times
    }


def measure_sorting_performance():
    """
    Сравнение производительности алгоритмов сортировки.
    
    Сравнивает:
    1. Heapsort
    2. Quicksort
    3. Mergesort
    """
    print("\n" + "="*60)
    print("Эксперимент 2: Сравнение алгоритмов сортировки")
    print("="*60)
    
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    heapsort_times = []
    quicksort_times = []
    mergesort_times = []
    
    for size in sizes:
        print(f"\nРазмер массива: {size}")
        
        # Генерируем случайный массив
        array = [random.randint(1, 10000) for _ in range(size)]
        
        # Heapsort
        test_array = list(array)
        start_time = time.perf_counter()
        heapsort_inplace(test_array)
        heapsort_time = time.perf_counter() - start_time
        heapsort_times.append(heapsort_time)
        print(f"  Heapsort: {heapsort_time:.6f} сек")
        
        # Quicksort
        test_array = list(array)
        start_time = time.perf_counter()
        sorted_array = quicksort(test_array)
        quicksort_time = time.perf_counter() - start_time
        quicksort_times.append(quicksort_time)
        print(f"  Quicksort: {quicksort_time:.6f} сек")
        
        # Mergesort
        test_array = list(array)
        start_time = time.perf_counter()
        sorted_array = mergesort(test_array)
        mergesort_time = time.perf_counter() - start_time
        mergesort_times.append(mergesort_time)
        print(f"  Mergesort: {mergesort_time:.6f} сек")
    
    return {
        'sizes': sizes,
        'heapsort': heapsort_times,
        'quicksort': quicksort_times,
        'mergesort': mergesort_times
    }


def measure_heap_operations():
    """
    Измерение времени операций insert и extract.
    
    Проверяет сложность O(log n) для этих операций.
    """
    print("\n" + "="*60)
    print("Эксперимент 3: Измерение времени операций кучи")
    print("="*60)
    
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    insert_times = []
    extract_times = []
    
    for size in sizes:
        print(f"\nРазмер кучи: {size}")
        
        # Создаем кучу заданного размера
        array = [random.randint(1, 10000) for _ in range(size)]
        heap = MinHeap(initial_array=array)
        
        # Измеряем время insert
        start_time = time.perf_counter()
        for _ in range(100):  # Выполняем 100 операций для усреднения
            heap.insert(random.randint(1, 10000))
        insert_time = (time.perf_counter() - start_time) / 100
        insert_times.append(insert_time)
        print(f"  Среднее время insert: {insert_time:.9f} сек")
        
        # Измеряем время extract
        # Восстанавливаем кучу
        heap = MinHeap(initial_array=array)
        start_time = time.perf_counter()
        for _ in range(min(100, size)):  # Выполняем до 100 операций
            if not heap.is_empty():
                heap.extract()
        extract_time = (time.perf_counter() - start_time) / min(100, size)
        extract_times.append(extract_time)
        print(f"  Среднее время extract: {extract_time:.9f} сек")
    
    return {
        'sizes': sizes,
        'insert': insert_times,
        'extract': extract_times
    }


def demonstrate_heap_visualization():
    """Демонстрация визуализации кучи."""
    print("\n" + "="*60)
    print("Демонстрация визуализации кучи")
    print("="*60)
    
    # Создаем небольшую кучу для визуализации
    array = [9, 5, 7, 3, 1, 8, 2, 6, 4]
    heap = MinHeap(initial_array=array)
    
    print("\nМинимальная куча из массива [9, 5, 7, 3, 1, 8, 2, 6, 4]:")
    visualize_heap_tree(heap, "MinHeap")
    
    # Демонстрируем операции
    print("\nИзвлечение элементов по одному:")
    while not heap.is_empty():
        print(f"Извлечен: {heap.extract()}")
        if heap.size() <= 10:  # Показываем только для небольших размеров
            visualize_heap_tree(heap, f"Heap после извлечения (размер: {heap.size()})")


def analyze_results(results):
    """
    Анализ результатов экспериментов.
    
    Args:
        results: Словарь с результатами всех экспериментов
    """
    print("\n" + "="*60)
    print("Анализ результатов")
    print("="*60)
    
    # Анализ построения кучи
    if 'heap_build' in results:
        print("\n1. Анализ построения кучи:")
        sizes = results['heap_build']['sizes']
        sequential = results['heap_build']['sequential']
        build_heap = results['heap_build']['build_heap']
        
        print("   Теоретическая сложность:")
        print("   - Последовательная вставка: O(n log n)")
        print("   - build_heap: O(n)")
        
        print("\n   Практические результаты:")
        for i, size in enumerate(sizes):
            ratio = sequential[i] / build_heap[i] if build_heap[i] > 0 else 0
            print(f"   Размер {size}: ускорение build_heap в {ratio:.2f} раз")
        
        # Проверяем рост времени
        if len(sizes) >= 2:
            seq_growth = sequential[-1] / sequential[0] if sequential[0] > 0 else 0
            build_growth = build_heap[-1] / build_heap[0] if build_heap[0] > 0 else 0
            size_growth = sizes[-1] / sizes[0]
            
            print(f"\n   Рост времени при увеличении размера в {size_growth:.1f} раз:")
            print(f"   - Последовательная вставка: {seq_growth:.2f}x")
            print(f"   - build_heap: {build_growth:.2f}x")
            print(f"   - Ожидаемый рост для O(n log n): ~{size_growth * np.log2(size_growth):.2f}x")
            print(f"   - Ожидаемый рост для O(n): ~{size_growth:.2f}x")
    
    # Анализ сортировки
    if 'sorting' in results:
        print("\n2. Анализ алгоритмов сортировки:")
        sizes = results['sorting']['sizes']
        heapsort_times = results['sorting']['heapsort']
        quicksort_times = results['sorting']['quicksort']
        mergesort_times = results['sorting']['mergesort']
        
        print("   Теоретическая сложность: O(n log n) для всех алгоритмов")
        
        print("\n   Сравнение производительности:")
        for i, size in enumerate(sizes):
            print(f"   Размер {size}:")
            print(f"     Heapsort: {heapsort_times[i]:.6f} сек")
            print(f"     Quicksort: {quicksort_times[i]:.6f} сек")
            print(f"     Mergesort: {mergesort_times[i]:.6f} сек")
            
            if quicksort_times[i] > 0:
                print(f"     Heapsort/Quicksort: {heapsort_times[i] / quicksort_times[i]:.2f}x")
            if mergesort_times[i] > 0:
                print(f"     Heapsort/Mergesort: {heapsort_times[i] / mergesort_times[i]:.2f}x")
    
    # Анализ операций кучи
    if 'heap_operations' in results:
        print("\n3. Анализ операций кучи:")
        sizes = results['heap_operations']['sizes']
        insert_times = results['heap_operations']['insert']
        extract_times = results['heap_operations']['extract']
        
        print("   Теоретическая сложность: O(log n) для insert и extract")
        
        print("\n   Практические результаты:")
        for i, size in enumerate(sizes):
            log_n = np.log2(size) if size > 0 else 0
            print(f"   Размер {size} (log n = {log_n:.2f}):")
            print(f"     insert: {insert_times[i]:.9f} сек")
            print(f"     extract: {extract_times[i]:.9f} сек")
        
        # Проверяем логарифмический рост
        if len(sizes) >= 2:
            size_ratio = sizes[-1] / sizes[0]
            log_ratio = np.log2(size_ratio)
            insert_ratio = insert_times[-1] / insert_times[0] if insert_times[0] > 0 else 0
            extract_ratio = extract_times[-1] / extract_times[0] if extract_times[0] > 0 else 0
            
            print(f"\n   Рост времени при увеличении размера в {size_ratio:.1f} раз:")
            print(f"   - insert: {insert_ratio:.2f}x (ожидается ~{log_ratio:.2f}x)")
            print(f"   - extract: {extract_ratio:.2f}x (ожидается ~{log_ratio:.2f}x)")


def main():
    """Главная функция для запуска всех экспериментов."""
    print()
    print("Модель: Infinix InBook Y3 Plus (YL512)")
    print("Процессор: 12th Gen Intel(R) Core(TM) i3-1215U")
    print("Видеочип: Intel(R) UHD Graphics")
    print("ОЗУ: 16 ГБ, тип: LPDDR4")
    print()
    
    # Создаем папку для данных, если её нет
    # Определяем корневую директорию проекта (на уровень выше src)
    project_root = os.path.join(os.path.dirname(__file__), '..')
    data_dir = os.path.join(project_root, 'docs')
    os.makedirs(data_dir, exist_ok=True)
    
    # Демонстрация визуализации
    demonstrate_heap_visualization()
    
    # Проводим эксперименты
    results = {}
    
    results['heap_build'] = measure_heap_build_performance()
    results['sorting'] = measure_sorting_performance()
    results['heap_operations'] = measure_heap_operations()
    
    # Анализ результатов
    analyze_results(results)
    
    # Построение графиков
    print("\n" + "="*60)
    print("Построение графиков")
    print("="*60)
    
    performance_path = os.path.join(data_dir, 'performance_comparison.png')
    plot_performance_comparison(results, save_path=performance_path)
    
    complexity_path = os.path.join(data_dir, 'complexity_analysis.png')
    plot_complexity_analysis(results, save_path=complexity_path)
    
    print("\n" + "="*60)
    print("Эксперименты завершены!")
    print(f"Графики сохранены в папку: {data_dir}")
    print("="*60)


if __name__ == '__main__':
    main()

