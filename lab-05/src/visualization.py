"""
Модуль для визуализации результатов экспериментов.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List
import os


def ensure_docs_directory():
    """Создает директорию docs, если её нет."""
    docs_dir = 'docs'
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)


def plot_operation_time_vs_load_factor(results: Dict, operation: str, title: str, filename: str):
    """
    Строит график зависимости времени операции от коэффициента заполнения.
    
    Args:
        results: Словарь с результатами экспериментов
        operation: Название операции ('insert_times', 'search_times', 'delete_times')
        title: Заголовок графика
        filename: Имя файла для сохранения
    """
    ensure_docs_directory()
    
    plt.figure(figsize=(10, 6))
    
    # Метод цепочек
    if 'chaining_djb2' in results:
        plt.plot(
            results['chaining_djb2']['load_factors'],
            results['chaining_djb2'][operation],
            marker='o', label='Цепочек (DJB2)', linewidth=2
        )
    
    if 'chaining_polynomial' in results:
        plt.plot(
            results['chaining_polynomial']['load_factors'],
            results['chaining_polynomial'][operation],
            marker='s', label='Цепочек (Polynomial)', linewidth=2
        )
    
    if 'chaining_simple' in results:
        plt.plot(
            results['chaining_simple']['load_factors'],
            results['chaining_simple'][operation],
            marker='^', label='Цепочек (Simple)', linewidth=2
        )
    
    # Открытая адресация
    if 'open_linear' in results:
        plt.plot(
            results['open_linear']['load_factors'],
            results['open_linear'][operation],
            marker='d', label='Открытая адресация (линейное)', linewidth=2
        )
    
    if 'open_double' in results:
        plt.plot(
            results['open_double']['load_factors'],
            results['open_double'][operation],
            marker='v', label='Открытая адресация (двойное)', linewidth=2
        )
    
    plt.xlabel('Коэффициент заполнения', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filepath = os.path.join('docs', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График сохранен: {filepath}")


def plot_collisions_vs_load_factor(results: Dict, filename: str):
    """
    Строит график зависимости количества коллизий от коэффициента заполнения.
    
    Args:
        results: Словарь с результатами экспериментов
        filename: Имя файла для сохранения
    """
    ensure_docs_directory()
    
    plt.figure(figsize=(10, 6))
    
    if 'chaining_djb2' in results:
        plt.plot(
            results['chaining_djb2']['load_factors'],
            results['chaining_djb2']['collisions'],
            marker='o', label='Цепочек (DJB2)', linewidth=2
        )
    
    if 'chaining_polynomial' in results:
        plt.plot(
            results['chaining_polynomial']['load_factors'],
            results['chaining_polynomial']['collisions'],
            marker='s', label='Цепочек (Polynomial)', linewidth=2
        )
    
    if 'chaining_simple' in results:
        plt.plot(
            results['chaining_simple']['load_factors'],
            results['chaining_simple']['collisions'],
            marker='^', label='Цепочек (Simple)', linewidth=2
        )
    
    if 'open_linear' in results:
        plt.plot(
            results['open_linear']['load_factors'],
            results['open_linear']['collisions'],
            marker='d', label='Открытая адресация (линейное)', linewidth=2
        )
    
    if 'open_double' in results:
        plt.plot(
            results['open_double']['load_factors'],
            results['open_double']['collisions'],
            marker='v', label='Открытая адресация (двойное)', linewidth=2
        )
    
    plt.xlabel('Коэффициент заполнения', fontsize=12)
    plt.ylabel('Количество коллизий', fontsize=12)
    plt.title('Зависимость количества коллизий от коэффициента заполнения', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filepath = os.path.join('docs', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График сохранен: {filepath}")


def plot_hash_function_comparison(results: Dict, filename: str):
    """
    Создает гистограмму сравнения качества хеш-функций.
    
    Args:
        results: Словарь с результатами экспериментов
        filename: Имя файла для сохранения
    """
    ensure_docs_directory()
    
    if 'hash_quality' not in results:
        print("Нет данных о качестве хеш-функций")
        return
    
    hash_quality = results['hash_quality']
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Подготовка данных
    functions = list(hash_quality.keys())
    collisions = [hash_quality[f]['collisions'] for f in functions]
    max_chain_lengths = [hash_quality[f]['max_chain_length'] for f in functions]
    avg_chain_lengths = [hash_quality[f]['avg_chain_length'] for f in functions]
    empty_slots = [hash_quality[f]['empty_slots'] for f in functions]
    
    # График 1: Коллизии
    axes[0, 0].bar(functions, collisions, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[0, 0].set_title('Количество коллизий', fontweight='bold')
    axes[0, 0].set_ylabel('Коллизии')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # График 2: Максимальная длина цепочки
    axes[0, 1].bar(functions, max_chain_lengths, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[0, 1].set_title('Максимальная длина цепочки', fontweight='bold')
    axes[0, 1].set_ylabel('Длина')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # График 3: Средняя длина цепочки
    axes[1, 0].bar(functions, avg_chain_lengths, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[1, 0].set_title('Средняя длина цепочки', fontweight='bold')
    axes[1, 0].set_ylabel('Длина')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # График 4: Пустые слоты
    axes[1, 1].bar(functions, empty_slots, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    axes[1, 1].set_title('Количество пустых слотов', fontweight='bold')
    axes[1, 1].set_ylabel('Слоты')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    filepath = os.path.join('docs', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Гистограмма сохранена: {filepath}")


def plot_comparison_all_methods(results: Dict, filename: str):
    """
    Создает сравнительный график всех методов для всех операций.
    
    Args:
        results: Словарь с результатами экспериментов
        filename: Имя файла для сохранения
    """
    ensure_docs_directory()
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    operations = ['insert_times', 'search_times', 'delete_times']
    operation_titles = ['Вставка', 'Поиск', 'Удаление']
    
    for idx, (op, title) in enumerate(zip(operations, operation_titles)):
        ax = axes[idx]
        
        if 'chaining_djb2' in results:
            ax.plot(
                results['chaining_djb2']['load_factors'],
                results['chaining_djb2'][op],
                marker='o', label='Цепочек (DJB2)', linewidth=2
            )
        
        if 'open_linear' in results:
            ax.plot(
                results['open_linear']['load_factors'],
                results['open_linear'][op],
                marker='d', label='Открытая адресация (линейное)', linewidth=2
            )
        
        if 'open_double' in results:
            ax.plot(
                results['open_double']['load_factors'],
                results['open_double'][op],
                marker='v', label='Открытая адресация (двойное)', linewidth=2
            )
        
        ax.set_xlabel('Коэффициент заполнения', fontsize=10)
        ax.set_ylabel('Время (сек)', fontsize=10)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    filepath = os.path.join('docs', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Сравнительный график сохранен: {filepath}")


def create_all_visualizations(results: Dict):
    """
    Создает все визуализации результатов экспериментов.
    
    Args:
        results: Словарь со всеми результатами экспериментов
    """
    print("\nСоздание визуализаций...")
    
    # Графики времени операций
    plot_operation_time_vs_load_factor(
        results, 'insert_times',
        'Зависимость времени вставки от коэффициента заполнения',
        'insert_time_vs_load_factor.png'
    )
    
    plot_operation_time_vs_load_factor(
        results, 'search_times',
        'Зависимость времени поиска от коэффициента заполнения',
        'search_time_vs_load_factor.png'
    )
    
    plot_operation_time_vs_load_factor(
        results, 'delete_times',
        'Зависимость времени удаления от коэффициента заполнения',
        'delete_time_vs_load_factor.png'
    )
    
    # График коллизий
    plot_collisions_vs_load_factor(
        results,
        'collisions_vs_load_factor.png'
    )
    
    # Сравнение хеш-функций
    plot_hash_function_comparison(
        results,
        'hash_function_comparison.png'
    )
    
    # Сравнительный график всех методов
    plot_comparison_all_methods(
        results,
        'all_methods_comparison.png'
    )
    
    print("\nВсе визуализации созданы!")


