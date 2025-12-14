"""
Модуль для экспериментального исследования производительности BST.

Проводит анализ сложности операций для сбалансированного и вырожденного деревьев.
"""

import time
import random
import sys
import matplotlib
# Используем TkAgg для отображения графиков (можно также использовать 'Qt5Agg')
try:
    matplotlib.use('TkAgg')
except:
    try:
        matplotlib.use('Qt5Agg')
    except:
        matplotlib.use('Agg')  # Fallback для систем без GUI
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from src.modules.binary_search_tree import BinarySearchTree

# Увеличиваем лимит рекурсии для больших деревьев
sys.setrecursionlimit(10000)


def build_balanced_tree(size):
    """
    Построение сбалансированного дерева путем вставки элементов в случайном порядке.
    
    Args:
        size: Количество элементов
        
    Returns:
        BinarySearchTree: Построенное дерево
    """
    tree = BinarySearchTree()
    values = list(range(size))
    random.shuffle(values)
    
    for value in values:
        tree.insert(value)
    
    return tree


def build_degenerate_tree(size):
    """
    Построение вырожденного дерева путем вставки элементов в отсортированном порядке.
    
    Args:
        size: Количество элементов
        
    Returns:
        BinarySearchTree: Построенное дерево
    """
    tree = BinarySearchTree()
    
    # Используем итеративную вставку для больших деревьев, чтобы избежать переполнения стека
    if size > 500:
        for value in range(size):
            tree.insert_iterative(value)
    else:
        for value in range(size):
            tree.insert(value)
    
    return tree


def measure_search_time(tree, num_searches=1000):
    """
    Замер времени выполнения операций поиска.
    
    Args:
        tree: Дерево для поиска
        num_searches: Количество операций поиска
        
    Returns:
        float: Среднее время одной операции поиска в секундах
    """
    if tree.size() == 0:
        return 0.0
    
    # Генерируем случайные значения для поиска
    max_value = tree.size() - 1
    search_values = [random.randint(0, max_value) for _ in range(num_searches)]
    
    start_time = time.perf_counter()
    
    for value in search_values:
        tree.search(value)
    
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / num_searches


def measure_insert_time(tree, values):
    """
    Замер времени выполнения операций вставки.
    
    Args:
        tree: Дерево для вставки
        values: Список значений для вставки
        
    Returns:
        float: Среднее время одной операции вставки в секундах
    """
    start_time = time.perf_counter()
    
    for value in values:
        tree.insert(value)
    
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / len(values) if len(values) > 0 else 0


def measure_delete_time(tree, values):
    """
    Замер времени выполнения операций удаления.
    
    Args:
        tree: Дерево для удаления
        values: Список значений для удаления
        
    Returns:
        float: Среднее время одной операции удаления в секундах
    """
    start_time = time.perf_counter()
    
    for value in values:
        tree.delete(value)
    
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    return total_time / len(values) if len(values) > 0 else 0


def analyze_trees(sizes, num_searches=1000, num_trials=5):
    """
    Проведение анализа производительности для деревьев разных размеров.
    
    Args:
        sizes: Список размеров деревьев для анализа
        num_searches: Количество операций поиска для каждого замера
        num_trials: Количество попыток для усреднения результатов
        
    Returns:
        dict: Результаты анализа с временами для сбалансированных и вырожденных деревьев
    """
    results = {
        'sizes': sizes,
        'balanced_search_times': [],
        'degenerate_search_times': [],
        'balanced_heights': [],
        'degenerate_heights': []
    }
    
    print("Начало анализа производительности BST...")
    print(f"Размеры деревьев: {sizes}")
    print(f"Количество операций поиска: {num_searches}")
    print(f"Количество попыток для усреднения: {num_trials}\n")
    
    for size in sizes:
        print(f"Анализ для размера {size}...")
        
        balanced_search_times = []
        degenerate_search_times = []
        balanced_heights = []
        degenerate_heights = []
        
        for trial in range(num_trials):
            # Сбалансированное дерево
            balanced_tree = build_balanced_tree(size)
            balanced_height = balanced_tree.height()
            balanced_heights.append(balanced_height)
            
            search_time = measure_search_time(balanced_tree, num_searches)
            balanced_search_times.append(search_time)
            
            # Вырожденное дерево
            degenerate_tree = build_degenerate_tree(size)
            degenerate_height = degenerate_tree.height()
            degenerate_heights.append(degenerate_height)
            
            search_time = measure_search_time(degenerate_tree, num_searches)
            degenerate_search_times.append(search_time)
        
        # Усредняем результаты
        avg_balanced = np.mean(balanced_search_times)
        avg_degenerate = np.mean(degenerate_search_times)
        avg_balanced_height = np.mean(balanced_heights)
        avg_degenerate_height = np.mean(degenerate_heights)
        
        results['balanced_search_times'].append(avg_balanced)
        results['degenerate_search_times'].append(avg_degenerate)
        results['balanced_heights'].append(avg_balanced_height)
        results['degenerate_heights'].append(avg_degenerate_height)
        
        print(f"  Сбалансированное: среднее время поиска = {avg_balanced:.2e} сек, высота = {avg_balanced_height:.1f}")
        print(f"  Вырожденное: среднее время поиска = {avg_degenerate:.2e} сек, высота = {avg_degenerate_height:.1f}\n")
    
    return results


def plot_results(results, output_dir='data'):
    """
    Построение графиков зависимости времени операций от количества элементов.
    
    Args:
        results: Результаты анализа
        output_dir: Директория для сохранения графиков
    """
    # Создаем директорию, если её нет
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    sizes = results['sizes']
    balanced_times = results['balanced_search_times']
    degenerate_times = results['degenerate_search_times']
    
    # График времени поиска
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes, balanced_times, 'b-o', label='Сбалансированное дерево', linewidth=2, markersize=6)
    plt.plot(sizes, degenerate_times, 'r-s', label='Вырожденное дерево', linewidth=2, markersize=6)
    plt.xlabel('Количество элементов (n)', fontsize=12)
    plt.ylabel('Среднее время поиска (сек)', fontsize=12)
    plt.title('Зависимость времени поиска от размера дерева', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # График высоты дерева
    plt.subplot(1, 2, 2)
    plt.plot(sizes, results['balanced_heights'], 'b-o', label='Сбалансированное дерево', linewidth=2, markersize=6)
    plt.plot(sizes, results['degenerate_heights'], 'r-s', label='Вырожденное дерево', linewidth=2, markersize=6)
    plt.xlabel('Количество элементов (n)', fontsize=12)
    plt.ylabel('Высота дерева', fontsize=12)
    plt.title('Зависимость высоты дерева от размера', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/bst_analysis.png', dpi=300, bbox_inches='tight')
    print(f"График сохранен в {output_dir}/bst_analysis.png")
    plt.show()
    
    # График сравнения сложности (теоретическая vs практическая)
    plt.figure(figsize=(12, 5))
    
    # Теоретические значения для сравнения
    log_n_balanced = [np.log2(n) if n > 0 else 0 for n in sizes]
    n_degenerate = sizes
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes, balanced_times, 'b-o', label='Практическое (сбалансированное)', linewidth=2, markersize=6)
    plt.plot(sizes, [t * max(balanced_times) / max(log_n_balanced) for t in log_n_balanced], 
             'b--', label='Теоретическое O(log n)', linewidth=2, alpha=0.7)
    plt.xlabel('Количество элементов (n)', fontsize=12)
    plt.ylabel('Нормализованное время', fontsize=12)
    plt.title('Сбалансированное дерево: практика vs теория', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    plt.subplot(1, 2, 2)
    plt.plot(sizes, degenerate_times, 'r-s', label='Практическое (вырожденное)', linewidth=2, markersize=6)
    plt.plot(sizes, [t * max(degenerate_times) / max(n_degenerate) for t in n_degenerate], 
             'r--', label='Теоретическое O(n)', linewidth=2, alpha=0.7)
    plt.xlabel('Количество элементов (n)', fontsize=12)
    plt.ylabel('Нормализованное время', fontsize=12)
    plt.title('Вырожденное дерево: практика vs теория', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/bst_complexity_comparison.png', dpi=300, bbox_inches='tight')
    print(f"График сравнения сохранен в {output_dir}/bst_complexity_comparison.png")
    plt.show()


def print_analysis_summary(results):
    """
    Вывод сводки результатов анализа.
    
    Args:
        results: Результаты анализа
    """
    print("\n" + "="*70)
    print("СВОДКА РЕЗУЛЬТАТОВ АНАЛИЗА")
    print("="*70)
    print(f"{'Размер':<10} {'Сбалансированное':<25} {'Вырожденное':<25}")
    print(f"{'':<10} {'Время (сек)':<12} {'Высота':<12} {'Время (сек)':<12} {'Высота':<12}")
    print("-"*70)
    
    for i, size in enumerate(results['sizes']):
        balanced_time = results['balanced_search_times'][i]
        balanced_height = results['balanced_heights'][i]
        degenerate_time = results['degenerate_search_times'][i]
        degenerate_height = results['degenerate_heights'][i]
        
        print(f"{size:<10} {balanced_time:<12.2e} {balanced_height:<12.1f} "
              f"{degenerate_time:<12.2e} {degenerate_height:<12.1f}")
    
    print("="*70)
    print("\nВЫВОДЫ:")
    print("1. Сбалансированное дерево:")
    print("   - Временная сложность поиска: O(log n) в среднем")
    print("   - Высота дерева растет логарифмически")
    print("   - Время поиска растет медленно с увеличением размера")
    
    print("\n2. Вырожденное дерево:")
    print("   - Временная сложность поиска: O(n) в худшем случае")
    print("   - Высота дерева равна количеству элементов - 1")
    print("   - Время поиска растет линейно с увеличением размера")
    
    print("\n3. Сравнение:")
    ratio = results['degenerate_search_times'][-1] / results['balanced_search_times'][-1]
    print(f"   - Для размера {results['sizes'][-1]}: вырожденное дерево в {ratio:.1f} раз медленнее")
    print("="*70)

