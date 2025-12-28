"""
Модуль для сравнительного анализа различных подходов динамического программирования.
"""

import time
import tracemalloc
from typing import List, Tuple, Dict, Callable
from src.modules.dynamic_programming import (
    fibonacci_memoized,
    fibonacci_bottom_up,
    knapsack_01_bottom_up
)


def measure_time_and_memory(func: Callable, *args, **kwargs) -> Tuple[float, float, any]:
    """
    Измеряет время выполнения и потребление памяти функции.
    
    Returns:
        Tuple[время в секундах, память в байтах, результат функции]
    """
    tracemalloc.start()
    start_time = time.perf_counter()
    
    result = func(*args, **kwargs)
    
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = end_time - start_time
    memory_used = peak
    
    return execution_time, memory_used, result


def compare_fibonacci_approaches(max_n: int = 40, step: int = 5) -> Dict:
    """
    Сравнение нисходящего (с мемоизацией) и восходящего подходов для чисел Фибоначчи.
    
    Args:
        max_n: максимальное значение n
        step: шаг для значений n
    
    Returns:
        Словарь с результатами сравнения
    """
    results = {
        'n_values': [],
        'memoized_time': [],
        'memoized_memory': [],
        'bottom_up_time': [],
        'bottom_up_memory': [],
        'memoized_results': [],
        'bottom_up_results': []
    }
    
    for n in range(step, max_n + 1, step):
        results['n_values'].append(n)
        
        # Нисходящий подход с мемоизацией
        time_memo, mem_memo, result_memo = measure_time_and_memory(
            fibonacci_memoized, n
        )
        results['memoized_time'].append(time_memo)
        results['memoized_memory'].append(mem_memo)
        results['memoized_results'].append(result_memo)
        
        # Восходящий подход
        time_bu, mem_bu, result_bu = measure_time_and_memory(
            fibonacci_bottom_up, n
        )
        results['bottom_up_time'].append(time_bu)
        results['bottom_up_memory'].append(mem_bu)
        results['bottom_up_results'].append(result_bu)
        
        # Проверка корректности
        assert result_memo == result_bu, f"Результаты не совпадают для n={n}"
    
    return results


def greedy_knapsack_continuous(weights: List[int], values: List[int], capacity: int) -> float:
    """
    Жадный алгоритм для непрерывного рюкзака (можно брать части предметов).
    
    Returns:
        Максимальная стоимость
    """
    # Сортируем по убыванию отношения стоимость/вес
    items = [(values[i] / weights[i], weights[i], values[i], i) 
             for i in range(len(weights))]
    items.sort(reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    
    for ratio, weight, value, _ in items:
        if remaining_capacity >= weight:
            total_value += value
            remaining_capacity -= weight
        else:
            total_value += ratio * remaining_capacity
            break
    
    return total_value


def compare_knapsack_approaches(
    num_items: int = 10,
    capacity: int = 50,
    num_tests: int = 5
) -> Dict:
    """
    Сравнение жадного алгоритма для непрерывного рюкзака с ДП для 0-1 рюкзака.
    
    Args:
        num_items: количество предметов
        capacity: вместимость рюкзака
        num_tests: количество тестов
    
    Returns:
        Словарь с результатами сравнения
    """
    import random
    
    results = {
        'test_num': [],
        'dp_value': [],
        'greedy_value': [],
        'dp_time': [],
        'greedy_time': [],
        'weights': [],
        'values': []
    }
    
    for test in range(num_tests):
        # Генерируем случайные веса и стоимости
        weights = [random.randint(1, 20) for _ in range(num_items)]
        values = [random.randint(10, 100) for _ in range(num_items)]
        
        results['test_num'].append(test + 1)
        results['weights'].append(weights.copy())
        results['values'].append(values.copy())
        
        # ДП для 0-1 рюкзака
        time_dp, _, (dp_value, _) = measure_time_and_memory(
            knapsack_01_bottom_up, weights, values, capacity
        )
        results['dp_value'].append(dp_value)
        results['dp_time'].append(time_dp)
        
        # Жадный алгоритм для непрерывного рюкзака
        time_greedy, _, greedy_value = measure_time_and_memory(
            greedy_knapsack_continuous, weights, values, capacity
        )
        results['greedy_value'].append(greedy_value)
        results['greedy_time'].append(time_greedy)
    
    return results


def analyze_knapsack_scalability(
    max_items: int = 50,
    step: int = 5,
    capacity: int = 100
) -> Dict:
    """
    Анализ масштабируемости алгоритма рюкзака при увеличении размера входных данных.
    
    Args:
        max_items: максимальное количество предметов
        step: шаг для количества предметов
        capacity: вместимость рюкзака
    
    Returns:
        Словарь с результатами анализа
    """
    import random
    
    results = {
        'num_items': [],
        'execution_time': [],
        'memory_used': [],
        'max_value': []
    }
    
    for n in range(step, max_items + 1, step):
        # Генерируем случайные данные
        weights = [random.randint(1, 20) for _ in range(n)]
        values = [random.randint(10, 100) for _ in range(n)]
        
        time_exec, mem_used, (max_val, _) = measure_time_and_memory(
            knapsack_01_bottom_up, weights, values, capacity
        )
        
        results['num_items'].append(n)
        results['execution_time'].append(time_exec)
        results['memory_used'].append(mem_used)
        results['max_value'].append(max_val)
    
    return results

