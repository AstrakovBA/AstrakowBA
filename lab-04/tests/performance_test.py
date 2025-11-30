"""
Модуль для эмпирического анализа производительности алгоритмов сортировки.

Замеряет время выполнения каждой сортировки на различных типах данных
и размерах массивов.
"""

import timeit
import json
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
from src.modules.generate_data import load_data_from_file, generate_all_datasets


# Словарь всех алгоритмов сортировки
SORT_ALGORITHMS = {
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'quick_sort': quick_sort
}

# Размеры массивов для тестирования
SIZES = [100, 1000, 5000, 10000]

# Типы данных
DATA_TYPES = ['random', 'sorted', 'reversed', 'almost_sorted']

# Количество запусков для каждого теста
NUMBER_OF_RUNS = 3


def measure_sort_time(sort_func, data):
    """
    Замеряет время выполнения функции сортировки на данных.
    
    Args:
        sort_func: функция сортировки
        data: данные для сортировки (копия исходного массива)
    
    Returns:
        float: среднее время выполнения в секундах
    """
    # Используем timeit для более точных замеров
    timer = timeit.Timer(lambda: sort_func(data.copy()))
    
    # Запускаем несколько раз и берем среднее
    times = timer.repeat(repeat=NUMBER_OF_RUNS, number=1)
    return sum(times) / len(times)


def run_performance_tests(data_dir="src/data", results_file="results/performance_results.json"):
    """
    Запускает все тесты производительности и сохраняет результаты.
    
    Args:
        data_dir: директория с тестовыми данными
        results_file: путь к файлу для сохранения результатов
    """
    data_path = Path(data_dir)
    results_path = Path(results_file)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    print("Начало тестирования производительности...")
    print("=" * 60)
    
    for size in SIZES:
        print(f"\nРазмер массива: {size}")
        results[size] = {}
        
        for data_type in DATA_TYPES:
            print(f"  Тип данных: {data_type}")
            filename = f"{data_type}_{size}.txt"
            filepath = data_path / filename
            
            if not filepath.exists():
                print(f"    Файл не найден: {filepath}, пропускаем...")
                continue
            
            # Загружаем данные
            data = load_data_from_file(str(filepath))
            results[size][data_type] = {}
            
            # Тестируем каждый алгоритм
            for algo_name, algo_func in SORT_ALGORITHMS.items():
                print(f"    Тестирование {algo_name}...", end=" ")
                try:
                    time_taken = measure_sort_time(algo_func, data)
                    results[size][data_type][algo_name] = time_taken
                    print(f"✓ {time_taken:.6f} сек")
                except Exception as e:
                    print(f"✗ Ошибка: {e}")
                    results[size][data_type][algo_name] = None
    
    # Сохраняем результаты в JSON
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"Тестирование завершено! Результаты сохранены в {results_path}")
    
    return results


def print_summary_table(results):
    """
    Выводит сводную таблицу результатов.
    
    Args:
        results: словарь с результатами тестирования
    """
    print("\n" + "=" * 80)
    print("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("=" * 80)
    
    for size in SIZES:
        if size not in results:
            continue
        
        print(f"\nРазмер массива: {size}")
        print("-" * 80)
        print(f"{'Алгоритм':<20} {'Random':<15} {'Sorted':<15} {'Reversed':<15} {'Almost Sorted':<15}")
        print("-" * 80)
        
        for algo_name in SORT_ALGORITHMS.keys():
            row = f"{algo_name:<20}"
            for data_type in DATA_TYPES:
                if data_type in results[size] and algo_name in results[size][data_type]:
                    time = results[size][data_type][algo_name]
                    if time is not None:
                        row += f"{time:<15.6f}"
                    else:
                        row += f"{'N/A':<15}"
                else:
                    row += f"{'N/A':<15}"
            print(row)


if __name__ == "__main__":
    # Генерируем данные, если их еще нет
    data_dir = Path("src/data")
    if not any(data_dir.glob("*.txt")):
        print("Генерация тестовых данных...")
        generate_all_datasets()
    
    # Запускаем тесты производительности
    results = run_performance_tests()
    
    # Выводим сводную таблицу
    print_summary_table(results)


