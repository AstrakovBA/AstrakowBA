"""
Главный файл для демонстрации работы жадных алгоритмов.
"""

import os
import sys
from pathlib import Path

# Добавляем директорию modules в путь для импортов
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from greedy_algorithms import (
    interval_scheduling,
    fractional_knapsack,
    huffman_encode,
    huffman_decode,
    coin_change_greedy,
    prim_mst,
    build_huffman_tree,
    build_huffman_codes
)
from analysis import (
    compare_knapsack_algorithms,
    measure_huffman_performance,
    compare_greedy_vs_naive_interval_scheduling
)
from visualization import (
    visualize_huffman_tree,
    plot_performance_graph,
    plot_compression_ratio,
    plot_knapsack_comparison
)


def demo_interval_scheduling():
    """Демонстрация задачи о выборе заявок."""
    print("\n" + "="*60)
    print("1. ЗАДАЧА О ВЫБОРЕ ЗАЯВОК (Interval Scheduling)")
    print("="*60)
    
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), 
                 (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
    
    print(f"\nИсходные интервалы: {intervals}")
    
    selected = interval_scheduling(intervals)
    print(f"\nВыбранные интервалы (жадный алгоритм): {selected}")
    print(f"Количество выбранных интервалов: {len(selected)}")
    
    # Сравнение с наивным подходом
    print("\n--- Сравнение с наивным подходом ---")
    comparison = compare_greedy_vs_naive_interval_scheduling(intervals)
    print(f"Жадный алгоритм: {comparison['greedy_count']} интервалов за {comparison['greedy_time']*1000:.4f} мс")
    if comparison['naive_count'] is not None:
        print(f"Наивный подход: {comparison['naive_count']} интервалов за {comparison['naive_time']*1000:.4f} мс")
        print(f"Ускорение: {comparison['naive_time']/comparison['greedy_time']:.2f}x")


def demo_fractional_knapsack():
    """Демонстрация задачи о непрерывном рюкзаке."""
    print("\n" + "="*60)
    print("2. НЕПРЕРЫВНЫЙ РЮКЗАК (Fractional Knapsack)")
    print("="*60)
    
    items = [(10, 60), (20, 100), (30, 120)]  # (вес, стоимость)
    capacity = 50
    
    print(f"\nПредметы (вес, стоимость): {items}")
    print(f"Вместимость рюкзака: {capacity}")
    
    value, selected = fractional_knapsack(items, capacity)
    print(f"\nМаксимальная стоимость: {value:.2f}")
    print(f"Выбранные предметы: {selected}")
    
    # Сравнение с точным алгоритмом для 0-1 рюкзака
    print("\n--- Сравнение с точным алгоритмом (0-1 рюкзак) ---")
    comparison = compare_knapsack_algorithms(items, capacity)
    print(f"Жадный (непрерывный): стоимость = {comparison['greedy_value']:.2f}, "
          f"время = {comparison['greedy_time']*1000:.4f} мс")
    
    if comparison['exact_value'] is not None:
        print(f"Точный (0-1): стоимость = {comparison['exact_value']:.2f}, "
              f"время = {comparison['exact_time']*1000:.4f} мс")
        print(f"Разница в стоимости: {comparison['greedy_value'] - comparison['exact_value']:.2f}")
        
        # Визуализация
        project_root = Path(__file__).parent.parent
        plot_knapsack_comparison(comparison, str(project_root / "docs" / "knapsack_comparison.png"))


def demo_huffman_coding():
    """Демонстрация алгоритма Хаффмана."""
    print("\n" + "="*60)
    print("3. АЛГОРИТМ ХАФФМАНА (Huffman Coding)")
    print("="*60)
    
    project_root = Path(__file__).parent.parent
    text = "abracadabra"
    print(f"\nИсходный текст: '{text}'")
    
    codes, encoded = huffman_encode(text)
    print(f"\nКоды символов:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")
    
    print(f"\nЗакодированный текст: {encoded}")
    print(f"Длина исходного текста (в битах, ASCII): {len(text) * 8}")
    print(f"Длина закодированного текста: {len(encoded)}")
    print(f"Коэффициент сжатия: {len(encoded) / (len(text) * 8):.2%}")
    
    # Декодирование
    decoded = huffman_decode(encoded, codes)
    print(f"\nДекодированный текст: '{decoded}'")
    print(f"Корректность декодирования: {decoded == text}")
    
    # Визуализация дерева
    from collections import Counter
    frequencies = dict(Counter(text))
    root = build_huffman_tree(frequencies)
    data_path = project_root / "docs" / "huffman_tree.png"
    visualize_huffman_tree(root, str(data_path))
    
    # Экспериментальное исследование производительности
    print("\n--- Экспериментальное исследование производительности ---")
    text_sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    results = measure_huffman_performance(text_sizes)
    
    print("\nРезультаты замеров:")
    print(f"{'Размер':<10} {'Время (мс)':<15} {'Коэф. сжатия':<15} {'Уник. символов':<15}")
    print("-" * 60)
    for r in results:
        print(f"{r['text_size']:<10} {r['total_time']*1000:<15.4f} "
              f"{r['compression_ratio']:<15.4f} {r['unique_chars']:<15}")
    
    # Визуализация графиков
    plot_performance_graph(results, str(project_root / "docs" / "performance_graph.png"))
    plot_compression_ratio(results, str(project_root / "docs" / "compression_ratio.png"))


def demo_coin_change():
    """Демонстрация задачи о минимальном количестве монет."""
    print("\n" + "="*60)
    print("4. ЗАДАЧА О МИНИМАЛЬНОМ КОЛИЧЕСТВЕ МОНЕТ")
    print("="*60)
    
    amount = 67
    coins = [1, 5, 10, 25, 50]  # Стандартная система монет
    
    print(f"\nСумма для выдачи: {amount}")
    print(f"Доступные монеты: {coins}")
    
    try:
        count, used_coins = coin_change_greedy(amount, coins)
        print(f"\nМинимальное количество монет: {count}")
        print(f"Использованные монеты: {used_coins}")
        print(f"Проверка: {sum(used_coins)} = {amount}")
    except ValueError as e:
        print(f"\nОшибка: {e}")


def demo_prim_mst():
    """Демонстрация алгоритма Прима."""
    print("\n" + "="*60)
    print("5. АЛГОРИТМ ПРИМА (Минимальное остовное дерево)")
    print("="*60)
    
    # Пример графа
    graph = {
        'A': [('B', 4), ('H', 8)],
        'B': [('A', 4), ('C', 8), ('H', 11)],
        'C': [('B', 8), ('D', 7), ('F', 4), ('I', 2)],
        'D': [('C', 7), ('E', 9), ('F', 14)],
        'E': [('D', 9), ('F', 10)],
        'F': [('C', 4), ('D', 14), ('E', 10), ('G', 2)],
        'G': [('F', 2), ('H', 1), ('I', 6)],
        'H': [('A', 8), ('B', 11), ('G', 1), ('I', 7)],
        'I': [('C', 2), ('G', 6), ('H', 7)]
    }
    
    print("\nГраф (вершина: [(сосед, вес), ...]):")
    for vertex, edges in graph.items():
        print(f"  {vertex}: {edges}")
    
    mst_edges = prim_mst(graph)
    total_weight = sum(edge[2] for edge in mst_edges)
    
    print(f"\nРёбра минимального остовного дерева:")
    for u, v, weight in mst_edges:
        print(f"  {u} -- {v} (вес: {weight})")
    print(f"\nОбщий вес MST: {total_weight}")


def main():
    """Главная функция для запуска всех демонстраций."""
    print("\n" + "="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №8: ЖАДНЫЕ АЛГОРИТМЫ")
    print("="*60)
    
    # Создаем директорию для данных (относительно корня проекта)
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Запускаем демонстрации
    demo_interval_scheduling()
    demo_fractional_knapsack()
    demo_huffman_coding()
    demo_coin_change()
    demo_prim_mst()
    
    print("\n" + "="*60)
    print("ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ")
    print("="*60)
    print("\nРезультаты сохранены в директории data/")
    print("Подробный анализ корректности см. в файле analytics.md")


if __name__ == "__main__":
    main()

