"""
Модуль для визуализации результатов работы жадных алгоритмов.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, List
import os
from greedy_algorithms import HuffmanNode


def visualize_huffman_tree(root: HuffmanNode, output_path: str = "docs/huffman_tree.png"):
    """
    Визуализация дерева кодов Хаффмана.
    
    Args:
        root: Корневой узел дерева Хаффмана
        output_path: Путь для сохранения изображения
    """
    if root is None:
        return
    
    # Создаем директорию, если её нет
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Рекурсивная функция для отрисовки дерева
    def draw_node(node, x, y, dx, dy, level=0):
        if node is None:
            return
        
        # Определяем цвет узла
        if node.char is not None:
            color = 'lightblue'
            label = f"{node.char}\n({node.freq})"
        else:
            color = 'lightgreen'
            label = f"{node.freq}"
        
        # Рисуем узел
        circle = plt.Circle((x, y), 0.3, color=color, ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, weight='bold')
        
        # Рисуем рёбра и дочерние узлы
        if node.left is not None:
            child_x = x - dx
            child_y = y - dy
            ax.plot([x, child_x], [y - 0.3, child_y + 0.3], 'k-', linewidth=1.5)
            ax.text((x + child_x) / 2, (y + child_y) / 2, '0', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
            draw_node(node.left, child_x, child_y, dx * 0.6, dy, level + 1)
        
        if node.right is not None:
            child_x = x + dx
            child_y = y - dy
            ax.plot([x, child_x], [y - 0.3, child_y + 0.3], 'k-', linewidth=1.5)
            ax.text((x + child_x) / 2, (y + child_y) / 2, '1', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
            draw_node(node.right, child_x, child_y, dx * 0.6, dy, level + 1)
    
    # Вычисляем высоту дерева для масштабирования
    def tree_height(node):
        if node is None:
            return 0
        return 1 + max(tree_height(node.left), tree_height(node.right))
    
    height = tree_height(root)
    draw_node(root, 0, height, 2, 1.5)
    
    # Устанавливаем границы
    ax.set_xlim(-height * 2, height * 2)
    ax.set_ylim(-1, height + 1)
    
    # Легенда
    leaf_patch = mpatches.Patch(color='lightblue', label='Лист (символ)')
    internal_patch = mpatches.Patch(color='lightgreen', label='Внутренний узел')
    ax.legend(handles=[leaf_patch, internal_patch], loc='upper right')
    
    plt.title('Дерево кодов Хаффмана', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Дерево Хаффмана сохранено в {output_path}")


def plot_performance_graph(results: List[Dict], output_path: str = "docs/performance_graph.png"):
    """
    Построение графика зависимости времени работы алгоритма от размера входных данных.
    
    Args:
        results: Список словарей с результатами замеров
        output_path: Путь для сохранения графика
    """
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    sizes = [r['text_size'] for r in results]
    times = [r['total_time'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'b-o', linewidth=2, markersize=6, label='Время выполнения')
    plt.xlabel('Размер входных данных (символов)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title('Зависимость времени работы алгоритма Хаффмана от размера данных', 
              fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"График производительности сохранен в {output_path}")


def plot_compression_ratio(results: List[Dict], output_path: str = "docs/compression_ratio.png"):
    """
    Построение графика коэффициента сжатия.
    
    Args:
        results: Список словарей с результатами замеров
        output_path: Путь для сохранения графика
    """
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    sizes = [r['text_size'] for r in results]
    ratios = [r['compression_ratio'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, ratios, 'g-s', linewidth=2, markersize=6, label='Коэффициент сжатия')
    plt.xlabel('Размер входных данных (символов)', fontsize=12)
    plt.ylabel('Коэффициент сжатия', fontsize=12)
    plt.title('Эффективность сжатия алгоритмом Хаффмана', 
              fontsize=14, weight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"График коэффициента сжатия сохранен в {output_path}")


def plot_knapsack_comparison(results: Dict, output_path: str = "docs/knapsack_comparison.png"):
    """
    Визуализация сравнения жадного и точного алгоритмов для рюкзака.
    
    Args:
        results: Словарь с результатами сравнения
        output_path: Путь для сохранения графика
    """
    dirname = os.path.dirname(output_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    if results['exact_value'] is None:
        print("Точное решение недоступно для визуализации (слишком большой размер входных данных)")
        return
    
    algorithms = ['Жадный\n(непрерывный)', 'Точный\n(0-1)']
    values = [results['greedy_value'], results['exact_value']]
    times = [results['greedy_time'] * 1000, results['exact_time'] * 1000]  # в миллисекундах
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # График стоимости
    bars1 = ax1.bar(algorithms, values, color=['skyblue', 'lightcoral'], edgecolor='black', linewidth=2)
    ax1.set_ylabel('Стоимость', fontsize=12)
    ax1.set_title('Сравнение стоимости решения', fontsize=13, weight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Добавляем значения на столбцы
    for bar, val in zip(bars1, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontsize=11, weight='bold')
    
    # График времени
    bars2 = ax2.bar(algorithms, times, color=['skyblue', 'lightcoral'], edgecolor='black', linewidth=2)
    ax2.set_ylabel('Время (мс)', fontsize=12)
    ax2.set_title('Сравнение времени выполнения', fontsize=13, weight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Добавляем значения на столбцы
    for bar, val in zip(bars2, times):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.4f}', ha='center', va='bottom', fontsize=11, weight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"График сравнения рюкзака сохранен в {output_path}")

