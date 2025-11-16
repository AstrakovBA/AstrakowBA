"""
Модуль для визуализации результатов тестирования производительности.

Строит графики зависимости времени выполнения от размера массива
и от типа данных.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_results(results_file="results/performance_results.json"):
    """
    Загружает результаты тестирования из JSON файла.
    
    Args:
        results_file: путь к файлу с результатами
    
    Returns:
        dict: словарь с результатами
    """
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def plot_by_size(results, data_type='random', ax=None):
    """
    Строит график зависимости времени выполнения от размера массива
    для каждого алгоритма на заданном типе данных.
    
    Args:
        results: словарь с результатами
        data_type: тип данных для построения графика
        ax: ось matplotlib для построения графика (если None, создается новая)
    """
    algorithms = ['bubble_sort', 'selection_sort', 'insertion_sort', 
                  'merge_sort', 'quick_sort']
    sizes = sorted([int(s) for s in results.keys()])
    
    for algo in algorithms:
        times = []
        valid_sizes = []
        
        for size in sizes:
            if str(size) in results:
                if data_type in results[str(size)]:
                    if algo in results[str(size)][data_type]:
                        time = results[str(size)][data_type][algo]
                        if time is not None and time > 0:
                            times.append(time)
                            valid_sizes.append(size)
        
        if times:
            ax.loglog(valid_sizes, times, marker='o', linewidth=2, 
                     markersize=6, label=algo.replace('_', ' ').title())
    
    ax.set_xlabel('Размер массива (n)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Время выполнения (сек)', fontsize=10, fontweight='bold')
    ax.set_title(f'{data_type.replace("_", " ").title()}', 
                fontsize=11, fontweight='bold')
    ax.grid(True, which="both", ls="-", alpha=0.3)
    ax.legend(fontsize=8, loc='best')


def plot_by_data_type(results, size=5000, ax=None):
    """
    Строит график зависимости времени выполнения от типа данных
    для фиксированного размера массива.
    
    Args:
        results: словарь с результатами
        size: размер массива для построения графика
        ax: ось matplotlib для построения графика (если None, создается новая)
    """
    algorithms = ['bubble_sort', 'selection_sort', 'insertion_sort', 
                  'merge_sort', 'quick_sort']
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    
    x = np.arange(len(data_types))
    width = 0.15
    
    for i, algo in enumerate(algorithms):
        times = []
        for data_type in data_types:
            if str(size) in results:
                if data_type in results[str(size)]:
                    if algo in results[str(size)][data_type]:
                        time = results[str(size)][data_type][algo]
                        times.append(time if time is not None else 0)
                    else:
                        times.append(0)
                else:
                    times.append(0)
            else:
                times.append(0)
        
        offset = (i - len(algorithms) / 2) * width + width / 2
        bars = ax.bar(x + offset, times, width, 
                     label=algo.replace('_', ' ').title())
        
        # Добавляем значения на столбцы (только если значения достаточно большие)
        for bar in bars:
            height = bar.get_height()
            if height > 0 and height > ax.get_ylim()[0] * 10:  # Показываем только если видимо
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                       f'{height:.4f}', ha='center', va='bottom', 
                       fontsize=7, rotation=90)
    
    ax.set_yscale('log')
    ax.set_xlabel('Тип данных', fontsize=10, fontweight='bold')
    ax.set_ylabel('Время выполнения (сек)', fontsize=10, fontweight='bold')
    ax.set_title(f'n = {size}', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([dt.replace('_', ' ').title() for dt in data_types], 
                       fontsize=9)
    ax.legend(fontsize=7, loc='best')
    ax.grid(True, which="both", ls="-", alpha=0.3, axis='y')


def create_summary_table(results, output_dir="docs"):
    """
    Создает сводную таблицу результатов и сохраняет в текстовый файл.
    
    Args:
        results: словарь с результатами
        output_dir: директория для сохранения таблицы
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    algorithms = ['bubble_sort', 'selection_sort', 'insertion_sort', 
                  'merge_sort', 'quick_sort']
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    sizes = sorted([int(s) for s in results.keys()])
    
    table_lines = []
    table_lines.append("=" * 100)
    table_lines.append("СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    table_lines.append("=" * 100)
    table_lines.append("")
    
    for size in sizes:
        table_lines.append(f"Размер массива: {size}")
        table_lines.append("-" * 100)
        header = f"{'Алгоритм':<20}"
        for dt in data_types:
            header += f"{dt.replace('_', ' ').title():<20}"
        table_lines.append(header)
        table_lines.append("-" * 100)
        
        for algo in algorithms:
            row = f"{algo.replace('_', ' ').title():<20}"
            for data_type in data_types:
                if str(size) in results:
                    if data_type in results[str(size)]:
                        if algo in results[str(size)][data_type]:
                            time = results[str(size)][data_type][algo]
                            if time is not None:
                                row += f"{time:<20.6f}"
                            else:
                                row += f"{'N/A':<20}"
                        else:
                            row += f"{'N/A':<20}"
                    else:
                        row += f"{'N/A':<20}"
                else:
                    row += f"{'N/A':<20}"
            table_lines.append(row)
        
        table_lines.append("")
    
    table_text = "\n".join(table_lines)
    
    filename = "summary_table.txt"
    filepath = output_path / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(table_text)
    
    print(f"Таблица сохранена: {filepath}")
    print("\n" + table_text)


def plot_all(results, output_dir="docs"):
    """
    Строит все графики на основе результатов.
    Группирует графики: одно изображение с 4 графиками зависимости от размера,
    одно изображение с 4 графиками зависимости от типа данных.
    
    Args:
        results: словарь с результатами
        output_dir: директория для сохранения графиков
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Построение графиков...")
    
    data_types = ['random', 'sorted', 'reversed', 'almost_sorted']
    sizes = sorted([int(s) for s in results.keys()])
    
    # Создаем одно изображение с 4 графиками зависимости от размера массива
    fig1, axes1 = plt.subplots(2, 2, figsize=(16, 12))
    fig1.suptitle('Зависимость времени выполнения от размера массива\n(логарифмические шкалы)', 
                  fontsize=16, fontweight='bold')
    
    axes1_flat = axes1.flatten()
    for idx, data_type in enumerate(data_types):
        plot_by_size(results, data_type, axes1_flat[idx])
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    filename1 = "time_vs_size_all_types.png"
    filepath1 = output_path / filename1
    plt.savefig(filepath1, dpi=300, bbox_inches='tight')
    print(f"График сохранен: {filepath1}")
    plt.show()
    plt.close(fig1)
    
    # Создаем одно изображение с 4 графиками зависимости от типа данных
    fig2, axes2 = plt.subplots(2, 2, figsize=(16, 12))
    fig2.suptitle('Зависимость времени выполнения от типа данных\n(логарифмическая шкала Y)', 
                  fontsize=16, fontweight='bold')
    
    axes2_flat = axes2.flatten()
    for idx, size in enumerate(sizes):
        if idx < 4:  # Максимум 4 графика
            plot_by_data_type(results, size, axes2_flat[idx])
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    filename2 = "time_vs_data_type_all_sizes.png"
    filepath2 = output_path / filename2
    plt.savefig(filepath2, dpi=300, bbox_inches='tight')
    print(f"График сохранен: {filepath2}")
    plt.show()
    plt.close(fig2)
    
    # Создаем сводную таблицу
    create_summary_table(results, output_dir)
    
    print("Все графики построены и сохранены!")


if __name__ == "__main__":
    results_file = "results/performance_results.json"
    
    if not Path(results_file).exists():
        print(f"Файл с результатами не найден: {results_file}")
        print("Сначала запустите tests/performance_test.py")
    else:
        results = load_results(results_file)
        plot_all(results)

