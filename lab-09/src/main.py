"""
Главный файл для запуска экспериментов по динамическому программированию.
"""

import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.modules.dynamic_programming import (
    fibonacci_bottom_up,
    fibonacci_memoized,
    knapsack_01_bottom_up,
    knapsack_01_get_table,
    lcs_bottom_up,
    lcs_get_table,
    levenshtein_distance,
    levenshtein_get_table,
    coin_change_min_coins,
    coin_change_ways,
    longest_increasing_subsequence,
    longest_increasing_subsequence_optimized
)
from src.modules.comparison import (
    compare_fibonacci_approaches,
    compare_knapsack_approaches,
    analyze_knapsack_scalability
)
from src.modules.visualization import (
    visualize_knapsack_table,
    visualize_lcs_table,
    visualize_levenshtein_table,
    plot_fibonacci_comparison,
    plot_knapsack_comparison,
    plot_scalability_analysis
)


def ensure_docs_dir():
    """Создает папку docs, если её нет."""
    docs_dir = project_root / 'docs'
    docs_dir.mkdir(exist_ok=True)
    return docs_dir


def print_section(title: str):
    """Печатает заголовок раздела."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_fibonacci():
    """Демонстрация вычисления чисел Фибоначчи."""
    print_section("1. ЧИСЛА ФИБОНАЧЧИ")
    
    n = 30
    print(f"Вычисление F({n}):")
    
    result_memo = fibonacci_memoized(n)
    result_bu = fibonacci_bottom_up(n)
    
    print(f"  Нисходящий подход (мемоизация): {result_memo}")
    print(f"  Восходящий подход: {result_bu}")
    print(f"  Результаты совпадают: {result_memo == result_bu}\n")


def demo_knapsack():
    """Демонстрация задачи о рюкзаке."""
    print_section("2. ЗАДАЧА О РЮКЗАКЕ (0-1 KNAPSACK)")
    
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    
    print(f"Предметы:")
    for i, (w, v) in enumerate(zip(weights, values)):
        print(f"  Предмет {i}: вес={w}, стоимость={v}")
    print(f"Вместимость рюкзака: {capacity}\n")
    
    max_value, selected_items = knapsack_01_bottom_up(weights, values, capacity)
    
    print(f"Максимальная стоимость: {max_value}")
    print(f"Выбранные предметы (индексы): {selected_items}")
    print(f"Выбранные предметы:")
    for idx in selected_items:
        print(f"  Предмет {idx}: вес={weights[idx]}, стоимость={values[idx]}")
    
    # Визуализация таблицы
    table = knapsack_01_get_table(weights, values, capacity)
    docs_dir = ensure_docs_dir()
    visualize_knapsack_table(
        weights, values, capacity, table,
        save_path=str(docs_dir / 'knapsack_table.png')
    )


def demo_lcs():
    """Демонстрация LCS."""
    print_section("3. НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS)")
    
    s1 = "ABCDGH"
    s2 = "AEDFHR"
    
    print(f"Строка 1: {s1}")
    print(f"Строка 2: {s2}\n")
    
    length, lcs_string = lcs_bottom_up(s1, s2)
    
    print(f"Длина LCS: {length}")
    print(f"LCS: {lcs_string}\n")
    
    # Визуализация таблицы
    table = lcs_get_table(s1, s2)
    docs_dir = ensure_docs_dir()
    visualize_lcs_table(s1, s2, table, save_path=str(docs_dir / 'lcs_table.png'))


def demo_levenshtein():
    """Демонстрация расстояния Левенштейна."""
    print_section("4. РАССТОЯНИЕ ЛЕВЕНШТЕЙНА")
    
    s1 = "kitten"
    s2 = "sitting"
    
    print(f"Строка 1: {s1}")
    print(f"Строка 2: {s2}\n")
    
    distance = levenshtein_distance(s1, s2)
    
    print(f"Расстояние Левенштейна: {distance}\n")
    
    # Визуализация таблицы
    table = levenshtein_get_table(s1, s2)
    docs_dir = ensure_docs_dir()
    visualize_levenshtein_table(s1, s2, table, save_path=str(docs_dir / 'levenshtein_table.png'))


def demo_coin_change():
    """Демонстрация задачи о размене монет."""
    print_section("5. РАЗМЕН МОНЕТ")
    
    coins = [1, 3, 4]
    amount = 6
    
    print(f"Номиналы монет: {coins}")
    print(f"Сумма: {amount}\n")
    
    min_coins = coin_change_min_coins(coins, amount)
    num_ways = coin_change_ways(coins, amount)
    
    print(f"Минимальное количество монет: {min_coins}")
    print(f"Количество способов размена: {num_ways}\n")


def demo_lis():
    """Демонстрация LIS."""
    print_section("6. НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS)")
    
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    
    print(f"Массив: {arr}\n")
    
    length_naive, lis_naive = longest_increasing_subsequence(arr)
    length_opt, lis_opt = longest_increasing_subsequence_optimized(arr)
    
    print(f"O(n²) алгоритм:")
    print(f"  Длина LIS: {length_naive}")
    print(f"  LIS: {lis_naive}")
    print(f"\nO(n log n) алгоритм:")
    print(f"  Длина LIS: {length_opt}")
    print(f"  LIS: {lis_opt}\n")


def run_fibonacci_comparison():
    """Запуск сравнения подходов для чисел Фибоначчи."""
    print_section("СРАВНЕНИЕ ПОДХОДОВ ДЛЯ ЧИСЕЛ ФИБОНАЧЧИ")
    
    print("Проводится сравнение нисходящего и восходящего подходов...")
    results = compare_fibonacci_approaches(max_n=40, step=5)
    
    print("\nРезультаты:")
    print(f"{'n':<5} {'Мемоизация (сек)':<20} {'Восходящий (сек)':<20} {'Мемоизация (КБ)':<20} {'Восходящий (КБ)':<20}")
    print("-" * 85)
    for i, n in enumerate(results['n_values']):
        print(f"{n:<5} {results['memoized_time'][i]:<20.6f} {results['bottom_up_time'][i]:<20.6f} "
              f"{results['memoized_memory'][i]/1024:<20.2f} {results['bottom_up_memory'][i]/1024:<20.2f}")
    
    # Визуализация
    docs_dir = ensure_docs_dir()
    plot_fibonacci_comparison(results, save_path=str(docs_dir / 'fibonacci_comparison.png'))


def run_knapsack_comparison():
    """Запуск сравнения ДП и жадного алгоритма для рюкзака."""
    print_section("СРАВНЕНИЕ ДП И ЖАДНОГО АЛГОРИТМА ДЛЯ РЮКЗАКА")
    
    print("Проводится сравнение...")
    results = compare_knapsack_approaches(num_items=10, capacity=50, num_tests=5)
    
    print("\nРезультаты:")
    print(f"{'Тест':<6} {'ДП стоимость':<15} {'Жадный стоимость':<20} {'ДП время (сек)':<18} {'Жадный время (сек)':<20}")
    print("-" * 80)
    for i in range(len(results['test_num'])):
        print(f"{results['test_num'][i]:<6} {results['dp_value'][i]:<15} {results['greedy_value'][i]:<20.2f} "
              f"{results['dp_time'][i]:<18.6f} {results['greedy_time'][i]:<20.6f}")
    
    # Визуализация
    docs_dir = ensure_docs_dir()
    plot_knapsack_comparison(results, save_path=str(docs_dir / 'knapsack_comparison.png'))


def run_scalability_analysis():
    """Запуск анализа масштабируемости."""
    print_section("АНАЛИЗ МАСШТАБИРУЕМОСТИ АЛГОРИТМА РЮКЗАКА")
    
    print("Проводится анализ масштабируемости...")
    results = analyze_knapsack_scalability(max_items=50, step=5, capacity=100)
    
    print("\nРезультаты:")
    print(f"{'Предметы':<10} {'Время (сек)':<15} {'Память (МБ)':<15} {'Макс. стоимость':<15}")
    print("-" * 55)
    for i in range(len(results['num_items'])):
        print(f"{results['num_items'][i]:<10} {results['execution_time'][i]:<15.6f} "
              f"{results['memory_used'][i]/1024/1024:<15.2f} {results['max_value'][i]:<15}")
    
    # Визуализация
    docs_dir = ensure_docs_dir()
    plot_scalability_analysis(results, save_path=str(docs_dir / 'scalability_analysis.png'))


def main():
    """Главная функция."""
    print("\n" + "=" * 80)
    print("  ЛАБОРАТОРНАЯ РАБОТА 09: ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ")
    print("=" * 80)
    
    # Демонстрация алгоритмов
    demo_fibonacci()
    demo_knapsack()
    demo_lcs()
    demo_levenshtein()
    demo_coin_change()
    demo_lis()
    
    # Сравнительный анализ
    run_fibonacci_comparison()
    run_knapsack_comparison()
    run_scalability_analysis()
    
    print_section("ЭКСПЕРИМЕНТЫ ЗАВЕРШЕНЫ")
    print("Все графики сохранены в папку docs/")
    print("Результаты анализа записаны в analytics.md")


if __name__ == "__main__":
    main()

