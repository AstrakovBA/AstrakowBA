"""
Модуль для визуализации таблиц динамического программирования и графиков производительности.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import os


def visualize_dp_table(
    table: List[List[int]],
    row_labels: List[str],
    col_labels: List[str],
    title: str,
    save_path: str = None
):
    """
    Визуализация таблицы динамического программирования.
    
    Args:
        table: 2D таблица значений
        row_labels: метки строк
        col_labels: метки столбцов
        title: заголовок графика
        save_path: путь для сохранения (опционально)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Преобразуем в numpy массив для удобства
    data = np.array(table)
    
    # Создаем тепловую карту
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
    
    # Добавляем значения в ячейки
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            text = ax.text(j, i, str(data[i, j]),
                          ha="center", va="center", color="black", fontsize=8)
    
    # Устанавливаем метки
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    
    # Поворачиваем метки оси X
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Столбцы', fontsize=12)
    ax.set_ylabel('Строки', fontsize=12)
    
    # Добавляем цветовую шкалу
    plt.colorbar(im, ax=ax)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def plot_fibonacci_comparison(results: Dict, save_path: str = None):
    """
    Построение графика сравнения подходов для чисел Фибоначчи.
    
    Args:
        results: результаты сравнения из compare_fibonacci_approaches
        save_path: путь для сохранения
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    n_values = results['n_values']
    
    # График времени выполнения
    ax1.plot(n_values, results['memoized_time'], 'o-', label='Нисходящий (мемоизация)', linewidth=2)
    ax1.plot(n_values, results['bottom_up_time'], 's-', label='Восходящий', linewidth=2)
    ax1.set_xlabel('n (номер числа Фибоначчи)', fontsize=11)
    ax1.set_ylabel('Время выполнения (секунды)', fontsize=11)
    ax1.set_title('Сравнение времени выполнения', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График потребления памяти
    ax2.plot(n_values, [m / 1024 for m in results['memoized_memory']], 
             'o-', label='Нисходящий (мемоизация)', linewidth=2)
    ax2.plot(n_values, [m / 1024 for m in results['bottom_up_memory']], 
             's-', label='Восходящий', linewidth=2)
    ax2.set_xlabel('n (номер числа Фибоначчи)', fontsize=11)
    ax2.set_ylabel('Память (КБ)', fontsize=11)
    ax2.set_title('Сравнение потребления памяти', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def plot_knapsack_comparison(results: Dict, save_path: str = None):
    """
    Построение графика сравнения ДП и жадного алгоритма для рюкзака.
    
    Args:
        results: результаты сравнения из compare_knapsack_approaches
        save_path: путь для сохранения
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    test_nums = results['test_num']
    
    # График стоимости
    x = np.arange(len(test_nums))
    width = 0.35
    
    ax1.bar(x - width/2, results['dp_value'], width, label='ДП (0-1 рюкзак)', alpha=0.8)
    ax1.bar(x + width/2, results['greedy_value'], width, label='Жадный (непрерывный)', alpha=0.8)
    ax1.set_xlabel('Номер теста', fontsize=11)
    ax1.set_ylabel('Максимальная стоимость', fontsize=11)
    ax1.set_title('Сравнение результатов', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(test_nums)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # График времени выполнения
    ax2.bar(x - width/2, results['dp_time'], width, label='ДП (0-1 рюкзак)', alpha=0.8)
    ax2.bar(x + width/2, results['greedy_time'], width, label='Жадный (непрерывный)', alpha=0.8)
    ax2.set_xlabel('Номер теста', fontsize=11)
    ax2.set_ylabel('Время выполнения (секунды)', fontsize=11)
    ax2.set_title('Сравнение времени выполнения', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(test_nums)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def plot_scalability_analysis(results: Dict, save_path: str = None):
    """
    Построение графика масштабируемости алгоритма рюкзака.
    
    Args:
        results: результаты из analyze_knapsack_scalability
        save_path: путь для сохранения
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    num_items = results['num_items']
    
    # График времени выполнения
    ax1.plot(num_items, results['execution_time'], 'o-', linewidth=2, markersize=6)
    ax1.set_xlabel('Количество предметов', fontsize=11)
    ax1.set_ylabel('Время выполнения (секунды)', fontsize=11)
    ax1.set_title('Масштабируемость по времени', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # График потребления памяти
    ax2.plot(num_items, [m / 1024 / 1024 for m in results['memory_used']], 
             's-', linewidth=2, markersize=6, color='orange')
    ax2.set_xlabel('Количество предметов', fontsize=11)
    ax2.set_ylabel('Память (МБ)', fontsize=11)
    ax2.set_title('Масштабируемость по памяти', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def visualize_knapsack_table(
    weights: List[int],
    values: List[int],
    capacity: int,
    table: List[List[int]],
    save_path: str = None
):
    """
    Визуализация таблицы ДП для задачи о рюкзаке.
    
    Args:
        weights: веса предметов
        values: стоимости предметов
        capacity: вместимость рюкзака
        table: таблица ДП
        save_path: путь для сохранения
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    data = np.array(table)
    
    # Создаем метки
    row_labels = ['0'] + [f'Предмет {i}' for i in range(1, len(weights) + 1)]
    col_labels = [str(w) for w in range(capacity + 1)]
    
    # Ограничиваем количество столбцов для читаемости
    if capacity > 20:
        step = max(1, capacity // 20)
        data = data[:, ::step]
        col_labels = col_labels[::step]
    
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
    
    # Добавляем значения
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            text = ax.text(j, i, str(data[i, j]),
                          ha="center", va="center", color="black", fontsize=7)
    
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    ax.set_title(f'Таблица ДП для задачи о рюкзаке\n'
                 f'Предметы: {len(weights)}, Вместимость: {capacity}', 
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Вместимость', fontsize=11)
    ax.set_ylabel('Предметы', fontsize=11)
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def visualize_lcs_table(s1: str, s2: str, table: List[List[int]], save_path: str = None):
    """
    Визуализация таблицы ДП для LCS.
    
    Args:
        s1, s2: входные строки
        table: таблица ДП
        save_path: путь для сохранения
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    data = np.array(table)
    
    # Создаем метки
    row_labels = [''] + list(s1)
    col_labels = [''] + list(s2)
    
    im = ax.imshow(data, cmap='Blues', aspect='auto')
    
    # Добавляем значения
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            text = ax.text(j, i, str(data[i, j]),
                          ha="center", va="center", color="white" if data[i, j] > data.max() / 2 else "black",
                          fontsize=10, fontweight='bold')
    
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    
    ax.set_title(f'Таблица ДП для LCS\nСтрока 1: "{s1}", Строка 2: "{s2}"',
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Строка 2', fontsize=11)
    ax.set_ylabel('Строка 1', fontsize=11)
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()


def visualize_levenshtein_table(s1: str, s2: str, table: List[List[int]], save_path: str = None):
    """
    Визуализация таблицы ДП для расстояния Левенштейна.
    
    Args:
        s1, s2: входные строки
        table: таблица ДП
        save_path: путь для сохранения
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    data = np.array(table)
    
    # Создаем метки
    row_labels = [''] + list(s1)
    col_labels = [''] + list(s2)
    
    im = ax.imshow(data, cmap='Reds', aspect='auto')
    
    # Добавляем значения
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            text = ax.text(j, i, str(data[i, j]),
                          ha="center", va="center", color="white" if data[i, j] > data.max() / 2 else "black",
                          fontsize=10, fontweight='bold')
    
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    
    ax.set_title(f'Таблица ДП для расстояния Левенштейна\nСтрока 1: "{s1}", Строка 2: "{s2}"',
                 fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel('Строка 2', fontsize=11)
    ax.set_ylabel('Строка 1', fontsize=11)
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    plt.close()

