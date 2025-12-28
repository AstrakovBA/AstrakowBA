"""
Модуль для сравнительного анализа эффективности жадных алгоритмов.
"""

import time
from typing import List, Tuple, Dict
from itertools import product
from collections import Counter
from greedy_algorithms import fractional_knapsack, huffman_encode, build_huffman_tree, build_huffman_codes


def knapsack_01_bruteforce(items: List[Tuple[float, float]], capacity: float) -> Tuple[float, List[int]]:
    """
    Точное решение задачи 0-1 рюкзака методом полного перебора.
    
    Args:
        items: Список предметов в формате (вес, стоимость)
        capacity: Вместимость рюкзака
    
    Returns:
        Кортеж (максимальная стоимость, список индексов выбранных предметов)
    
    Временная сложность: O(2^n) - экспоненциальная
    """
    n = len(items)
    max_value = 0.0
    best_combination = []
    
    # Перебираем все возможные комбинации
    for combination in product([0, 1], repeat=n):
        total_weight = sum(items[i][0] for i in range(n) if combination[i] == 1)
        total_value = sum(items[i][1] for i in range(n) if combination[i] == 1)
        
        if total_weight <= capacity and total_value > max_value:
            max_value = total_value
            best_combination = [i for i in range(n) if combination[i] == 1]
    
    return max_value, best_combination


def compare_knapsack_algorithms(items: List[Tuple[float, float]], capacity: float) -> Dict:
    """
    Сравнение жадного алгоритма для непрерывного рюкзака и точного алгоритма
    для дискретного 0-1 рюкзака.
    
    Args:
        items: Список предметов в формате (вес, стоимость)
        capacity: Вместимость рюкзака
    
    Returns:
        Словарь с результатами сравнения
    """
    # Жадный алгоритм для непрерывного рюкзака
    start_time = time.perf_counter()
    greedy_value, greedy_items = fractional_knapsack(items, capacity)
    greedy_time = time.perf_counter() - start_time
    
    # Точный алгоритм для 0-1 рюкзака (только для маленьких входных данных)
    if len(items) <= 15:  # Ограничение для полного перебора
        start_time = time.perf_counter()
        exact_value, exact_items = knapsack_01_bruteforce(items, capacity)
        exact_time = time.perf_counter() - start_time
    else:
        exact_value = None
        exact_items = None
        exact_time = None
    
    return {
        'greedy_value': greedy_value,
        'greedy_time': greedy_time,
        'greedy_items': greedy_items,
        'exact_value': exact_value,
        'exact_time': exact_time,
        'exact_items': exact_items,
        'items_count': len(items),
        'capacity': capacity
    }


def measure_huffman_performance(text_sizes: List[int], base_text: str = None) -> List[Dict]:
    """
    Замер времени работы алгоритма Хаффмана на данных разного размера.
    
    Args:
        text_sizes: Список размеров текстов для тестирования
        base_text: Базовый текст для генерации данных (если None, генерируется случайный)
    
    Returns:
        Список словарей с результатами замеров
    """
    import random
    import string
    
    if base_text is None:
        # Генерируем случайный текст из букв и пробелов
        base_text = ''.join(random.choices(string.ascii_letters + ' ', k=1000))
    
    results = []
    
    for size in text_sizes:
        # Генерируем текст нужного размера
        if size <= len(base_text):
            test_text = base_text[:size]
        else:
            # Повторяем базовый текст
            test_text = (base_text * ((size // len(base_text)) + 1))[:size]
        
        # Замер времени кодирования
        start_time = time.perf_counter()
        codes, encoded = huffman_encode(test_text)
        encode_time = time.perf_counter() - start_time
        
        # Замер времени построения дерева
        frequencies = dict(Counter(test_text))
        start_time = time.perf_counter()
        tree = build_huffman_tree(frequencies)
        tree_time = time.perf_counter() - start_time
        
        # Замер времени построения кодов
        start_time = time.perf_counter()
        codes_dict = build_huffman_codes(tree)
        codes_time = time.perf_counter() - start_time
        
        # Вычисляем коэффициент сжатия
        original_bits = len(test_text) * 8  # Предполагаем 8 бит на символ
        compressed_bits = len(encoded)
        compression_ratio = compressed_bits / original_bits if original_bits > 0 else 0
        
        results.append({
            'text_size': size,
            'encode_time': encode_time,
            'tree_time': tree_time,
            'codes_time': codes_time,
            'total_time': encode_time,
            'compression_ratio': compression_ratio,
            'unique_chars': len(frequencies)
        })
    
    return results


def compare_greedy_vs_naive_interval_scheduling(intervals: List[Tuple[int, int]]) -> Dict:
    """
    Сравнение жадного алгоритма и наивного подхода для задачи о выборе заявок.
    
    Наивный подход: перебор всех возможных комбинаций интервалов.
    
    Args:
        intervals: Список интервалов
    
    Returns:
        Словарь с результатами сравнения
    """
    from greedy_algorithms import interval_scheduling
    
    # Жадный алгоритм
    start_time = time.perf_counter()
    greedy_result = interval_scheduling(intervals)
    greedy_time = time.perf_counter() - start_time
    
    # Наивный подход (только для маленьких входных данных)
    if len(intervals) <= 15:
        start_time = time.perf_counter()
        
        def is_valid_combination(combo):
            """Проверяет, что интервалы не пересекаются."""
            sorted_combo = sorted(combo, key=lambda x: x[0])
            for i in range(len(sorted_combo) - 1):
                if sorted_combo[i][1] > sorted_combo[i + 1][0]:
                    return False
            return True
        
        max_count = 0
        best_combination = []
        
        # Перебираем все возможные комбинации
        from itertools import combinations
        for r in range(1, len(intervals) + 1):
            for combo in combinations(intervals, r):
                if is_valid_combination(combo):
                    if len(combo) > max_count:
                        max_count = len(combo)
                        best_combination = list(combo)
        
        naive_time = time.perf_counter() - start_time
        naive_result = best_combination
    else:
        naive_time = None
        naive_result = None
    
    return {
        'greedy_count': len(greedy_result),
        'greedy_time': greedy_time,
        'greedy_result': greedy_result,
        'naive_count': len(naive_result) if naive_result else None,
        'naive_time': naive_time,
        'naive_result': naive_result,
        'intervals_count': len(intervals)
    }

