"""
Модуль для визуализации кучи и построения графиков.
"""

import matplotlib.pyplot as plt
import numpy as np
import os


def visualize_heap_tree(heap, title="Heap Tree", save_path=None):
    """
    Визуализация кучи в виде дерева (текстовый вывод).
    
    Args:
        heap: Объект Heap для визуализации
        title: Заголовок
        save_path: Путь для сохранения (опционально)
    """
    if heap.is_empty():
        print(f"{title}: Empty heap")
        return
    
    def print_tree(index, prefix="", is_last=True):
        """Рекурсивный вывод дерева."""
        if index >= len(heap.heap):
            return
        
        print(prefix + ("└── " if is_last else "├── ") + str(heap.heap[index]))
        
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < len(heap.heap) or right < len(heap.heap):
            new_prefix = prefix + ("    " if is_last else "│   ")
            if right < len(heap.heap):
                print_tree(left, new_prefix, False)
                print_tree(right, new_prefix, True)
            elif left < len(heap.heap):
                print_tree(left, new_prefix, True)
    
    print(f"\n{title}:")
    print_tree(0)
    print()


def plot_performance_comparison(results, save_path=None):
    """
    Построение графиков сравнения производительности.
    
    Args:
        results: Словарь с результатами измерений
        save_path: Путь для сохранения графика
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # График 1: Построение кучи (логарифмический масштаб)
    ax1 = axes[0, 0]
    if 'heap_build' in results:
        sizes = results['heap_build']['sizes']
        sequential = results['heap_build']['sequential']
        build_heap = results['heap_build']['build_heap']
        
        ax1.loglog(sizes, sequential, 'o-', label='Последовательная вставка', linewidth=2)
        ax1.loglog(sizes, build_heap, 's-', label='build_heap', linewidth=2)
        ax1.set_xlabel('Размер массива (log)', fontsize=12)
        ax1.set_ylabel('Время (секунды, log)', fontsize=12)
        ax1.set_title('Сравнение методов построения кучи', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3, which='both')
    
    # График 2: Сравнение алгоритмов сортировки (логарифмический масштаб)
    ax2 = axes[0, 1]
    if 'sorting' in results:
        sizes = results['sorting']['sizes']
        heapsort_times = results['sorting']['heapsort']
        quicksort_times = results['sorting']['quicksort']
        mergesort_times = results['sorting']['mergesort']
        
        ax2.loglog(sizes, heapsort_times, 'o-', label='Heapsort', linewidth=2)
        ax2.loglog(sizes, quicksort_times, 's-', label='Quicksort', linewidth=2)
        ax2.loglog(sizes, mergesort_times, '^-', label='Mergesort', linewidth=2)
        ax2.set_xlabel('Размер массива (log)', fontsize=12)
        ax2.set_ylabel('Время (секунды, log)', fontsize=12)
        ax2.set_title('Сравнение алгоритмов сортировки', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, which='both')
    
    # График 3: Операции кучи (логарифмический масштаб)
    ax3 = axes[1, 0]
    if 'heap_operations' in results:
        sizes = results['heap_operations']['sizes']
        insert_times = results['heap_operations']['insert']
        extract_times = results['heap_operations']['extract']
        
        ax3.loglog(sizes, insert_times, 'o-', label='insert', linewidth=2)
        ax3.loglog(sizes, extract_times, 's-', label='extract', linewidth=2)
        ax3.set_xlabel('Размер кучи (log)', fontsize=12)
        ax3.set_ylabel('Время (секунды, log)', fontsize=12)
        ax3.set_title('Время операций insert и extract', fontsize=14, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, which='both')
    
    # График 4: Логарифмический масштаб для сортировки (дубликат для полноты)
    ax4 = axes[1, 1]
    if 'sorting' in results:
        sizes = results['sorting']['sizes']
        heapsort_times = results['sorting']['heapsort']
        quicksort_times = results['sorting']['quicksort']
        mergesort_times = results['sorting']['mergesort']
        
        ax4.loglog(sizes, heapsort_times, 'o-', label='Heapsort', linewidth=2)
        ax4.loglog(sizes, quicksort_times, 's-', label='Quicksort', linewidth=2)
        ax4.loglog(sizes, mergesort_times, '^-', label='Mergesort', linewidth=2)
        ax4.set_xlabel('Размер массива (log)', fontsize=12)
        ax4.set_ylabel('Время (секунды, log)', fontsize=12)
        ax4.set_title('Сравнение алгоритмов (логарифмический масштаб)', fontsize=14, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен: {save_path}")
    
    plt.show()
    plt.close()


def plot_complexity_analysis(results, save_path=None):
    """
    Построение графика для анализа сложности.
    
    Args:
        results: Словарь с результатами измерений
        save_path: Путь для сохранения графика
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # График 1: Теоретическая vs практическая сложность построения кучи (логарифмический масштаб)
    ax1 = axes[0]
    if 'heap_build' in results:
        sizes = results['heap_build']['sizes']
        sequential = results['heap_build']['sequential']
        build_heap = results['heap_build']['build_heap']
        
        # Теоретическая сложность: O(n log n) для последовательной вставки
        # и O(n) для build_heap
        theoretical_sequential = [n * np.log2(n) if n > 0 else 0 for n in sizes]
        theoretical_build = sizes
        
        # Нормализуем для сравнения
        if max(sequential) > 0:
            norm_seq = max(sequential) / max(theoretical_sequential) if max(theoretical_sequential) > 0 else 1
            theoretical_sequential = [t * norm_seq for t in theoretical_sequential]
        
        if max(build_heap) > 0:
            norm_build = max(build_heap) / max(theoretical_build) if max(theoretical_build) > 0 else 1
            theoretical_build = [t * norm_build for t in theoretical_build]
        
        ax1.loglog(sizes, sequential, 'o-', label='Последовательная вставка (практика)', linewidth=2)
        ax1.loglog(sizes, theoretical_sequential, '--', label='O(n log n) (теория)', linewidth=2, alpha=0.7)
        ax1.loglog(sizes, build_heap, 's-', label='build_heap (практика)', linewidth=2)
        ax1.loglog(sizes, theoretical_build, '--', label='O(n) (теория)', linewidth=2, alpha=0.7)
        ax1.set_xlabel('Размер массива (log)', fontsize=12)
        ax1.set_ylabel('Нормализованное время (log)', fontsize=12)
        ax1.set_title('Теоретическая vs практическая сложность', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3, which='both')
    
    # График 2: Анализ сложности операций (логарифмический масштаб)
    ax2 = axes[1]
    if 'heap_operations' in results:
        sizes = results['heap_operations']['sizes']
        insert_times = results['heap_operations']['insert']
        extract_times = results['heap_operations']['extract']
        
        # Теоретическая сложность: O(log n)
        theoretical_log = [np.log2(n) if n > 0 else 0 for n in sizes]
        
        # Нормализуем
        if max(insert_times) > 0:
            norm = max(insert_times) / max(theoretical_log) if max(theoretical_log) > 0 else 1
            theoretical_log = [t * norm for t in theoretical_log]
        
        ax2.loglog(sizes, insert_times, 'o-', label='insert (практика)', linewidth=2)
        ax2.loglog(sizes, extract_times, 's-', label='extract (практика)', linewidth=2)
        ax2.loglog(sizes, theoretical_log, '--', label='O(log n) (теория)', linewidth=2, alpha=0.7)
        ax2.set_xlabel('Размер кучи (log)', fontsize=12)
        ax2.set_ylabel('Нормализованное время (log)', fontsize=12)
        ax2.set_title('Сложность операций кучи', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен: {save_path}")
    
    plt.show()
    plt.close()

