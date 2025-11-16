"""
Главная точка входа для проекта анализа алгоритмов сортировки.

Выполняет следующие шаги:
1. Генерация тестовых данных
2. Запуск тестов корректности алгоритмов
3. Замер производительности алгоритмов
4. Построение графиков и таблиц результатов
"""

import sys
import argparse
from pathlib import Path

# Добавляем текущую директорию в путь для импорта модулей
sys.path.insert(0, str(Path(__file__).parent))

from modules.generate_data import generate_all_datasets
from modules.plot_results import plot_all, load_results


def main():
    """Главная функция программы."""
    parser = argparse.ArgumentParser(
        description='Анализ производительности алгоритмов сортировки'
    )
    parser.add_argument(
        '--skip-generation',
        action='store_true',
        help='Пропустить генерацию тестовых данных'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Пропустить тесты корректности'
    )
    parser.add_argument(
        '--skip-performance',
        action='store_true',
        help='Пропустить замер производительности'
    )
    parser.add_argument(
        '--skip-plots',
        action='store_true',
        help='Пропустить построение графиков'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ СОРТИРОВКИ")
    print("=" * 80)
    print()
    
    # Шаг 1: Генерация тестовых данных
    if not args.skip_generation:
        print("ШАГ 1: Генерация тестовых данных")
        print("-" * 80)
        generate_all_datasets()
        print()
    else:
        print("ШАГ 1: Пропущена генерация данных")
        print()
    
    # Шаг 2: Тесты корректности
    if not args.skip_tests:
        print("ШАГ 2: Запуск тестов корректности алгоритмов")
        print("-" * 80)
        import subprocess
        result = subprocess.run(
            [sys.executable, '-m', 'unittest', 'tests.test_sorts'],
            cwd=Path(__file__).parent.parent
        )
        if result.returncode != 0:
            print("ВНИМАНИЕ: Некоторые тесты не прошли!")
        print()
    else:
        print("ШАГ 2: Пропущены тесты корректности")
        print()
    
    # Шаг 3: Замер производительности
    if not args.skip_performance:
        print("ШАГ 3: Замер производительности алгоритмов")
        print("-" * 80)
        from tests.performance_test import run_performance_tests, print_summary_table
        results = run_performance_tests()
        print_summary_table(results)
        print()
    else:
        print("ШАГ 3: Пропущен замер производительности")
        print()
    
    # Шаг 4: Построение графиков
    if not args.skip_plots:
        print("ШАГ 4: Построение графиков и таблиц")
        print("-" * 80)
        results_file = "results/performance_results.json"
        if Path(results_file).exists():
            results = load_results(results_file)
            plot_all(results)
        else:
            print(f"Файл с результатами не найден: {results_file}")
            print("Сначала выполните замер производительности (ШАГ 3)")
        print()
    else:
        print("ШАГ 4: Пропущено построение графиков")
        print()
    
    print("=" * 80)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 80)
    
    print("\nРЕЗУЛЬТАТЫ:")
    print("- Тестовые данные: src/data/")
    print("- Результаты производительности: results/performance_results.json")
    print("- Графики: docs/")
    print("- Сводная таблица: docs/summary_table.txt")


if __name__ == "__main__":
    main()


