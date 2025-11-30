"""
Главный файл для запуска всех операций с бинарным деревом поиска.

Демонстрирует:
1. Основные операции BST (вставка, поиск, удаление)
2. Различные методы обхода дерева
3. Визуализацию дерева
4. Экспериментальное исследование производительности
"""

import random
from src.modules.binary_search_tree import BinarySearchTree
from src.modules.tree_traversal import (
    in_order_recursive,
    pre_order_recursive,
    post_order_recursive,
    in_order_iterative,
    print_in_order,
    print_pre_order,
    print_post_order
)
from src.modules.analysis import (
    build_balanced_tree,
    build_degenerate_tree,
    analyze_trees,
    plot_results,
    print_analysis_summary
)


def demonstrate_basic_operations():
    """Демонстрация основных операций BST."""
    print("="*70)
    print("ДЕМОНСТРАЦИЯ ОСНОВНЫХ ОПЕРАЦИЙ BST")
    print("="*70)
    
    tree = BinarySearchTree()
    
    # Вставка элементов
    print("\n1. Вставка элементов: [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for value in values:
        tree.insert(value)
    
    print(f"   Размер дерева: {tree.size()}")
    print(f"   Высота дерева: {tree.height()}")
    print(f"   Является ли BST: {tree.is_valid_bst()}")
    
    # Поиск элементов
    print("\n2. Поиск элементов:")
    search_values = [40, 25, 100]
    for value in search_values:
        node = tree.search(value)
        if node:
            print(f"   Элемент {value} найден")
        else:
            print(f"   Элемент {value} не найден")
    
    # Поиск минимума и максимума
    print("\n3. Поиск минимума и максимума:")
    min_node = tree.find_min()
    max_node = tree.find_max()
    print(f"   Минимум: {min_node.value if min_node else 'None'}")
    print(f"   Максимум: {max_node.value if max_node else 'None'}")
    
    # Удаление элементов
    print("\n4. Удаление элементов: [25, 70]")
    tree.delete(25)
    tree.delete(70)
    print(f"   Размер после удаления: {tree.size()}")
    print(f"   Высота после удаления: {tree.height()}")
    print(f"   Является ли BST: {tree.is_valid_bst()}")
    
    print("\n" + "="*70 + "\n")


def demonstrate_traversals():
    """Демонстрация методов обхода дерева."""
    print("="*70)
    print("ДЕМОНСТРАЦИЯ МЕТОДОВ ОБХОДА ДЕРЕВА")
    print("="*70)
    
    tree = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for value in values:
        tree.insert(value)
    
    print("\nДерево: [50, 30, 70, 20, 40, 60, 80]")
    print("\nРекурсивные обходы:")
    print_in_order(tree.root)
    print_pre_order(tree.root)
    print_post_order(tree.root)
    
    print("\nИтеративные обходы:")
    print("In-order (итеративный):", in_order_iterative(tree.root))
    
    print("\nСравнение рекурсивного и итеративного in-order:")
    recursive = in_order_recursive(tree.root)
    iterative = in_order_iterative(tree.root)
    print(f"Рекурсивный: {recursive}")
    print(f"Итеративный: {iterative}")
    print(f"Результаты совпадают: {recursive == iterative}")
    
    print("\n" + "="*70 + "\n")


def demonstrate_visualization():
    """Демонстрация визуализации дерева."""
    print("="*70)
    print("ВИЗУАЛИЗАЦИЯ ДЕРЕВА")
    print("="*70)
    
    tree = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for value in values:
        tree.insert(value)
    
    print("\n1. Визуализация с отступами:")
    print(tree.visualize())
    
    print("\n2. Скобочная нотация:")
    print(tree.to_bracket_notation())
    
    print("\n" + "="*70 + "\n")


def demonstrate_balanced_vs_degenerate():
    """Демонстрация разницы между сбалансированным и вырожденным деревьями."""
    print("="*70)
    print("СРАВНЕНИЕ СБАЛАНСИРОВАННОГО И ВЫРОЖДЕННОГО ДЕРЕВЬЕВ")
    print("="*70)
    
    size = 15
    
    # Сбалансированное дерево
    print(f"\n1. Сбалансированное дерево (размер {size}):")
    balanced_tree = build_balanced_tree(size)
    print(f"   Высота: {balanced_tree.height()}")
    print(f"   Теоретическая высота (log2(n)): {size.bit_length() - 1}")
    print("\n   Визуализация:")
    print(balanced_tree.visualize())
    
    # Вырожденное дерево
    print(f"\n2. Вырожденное дерево (размер {size}):")
    degenerate_tree = build_degenerate_tree(size)
    print(f"   Высота: {degenerate_tree.height()}")
    print(f"   Теоретическая высота (n-1): {size - 1}")
    print("\n   Визуализация:")
    print(degenerate_tree.visualize())
    
    print("\n" + "="*70 + "\n")


def run_performance_analysis():
    """Запуск экспериментального исследования производительности."""
    print("="*70)
    print("ЭКСПЕРИМЕНТАЛЬНОЕ ИССЛЕДОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*70)
    
    # Размеры деревьев для анализа (уменьшены для избежания проблем с рекурсией)
    sizes = [100, 200, 500, 1000, 2000]
    
    # Проводим анализ
    results = analyze_trees(sizes, num_searches=1000, num_trials=3)
    
    # Выводим сводку
    print_analysis_summary(results)
    
    # Строим графики
    print("\nПостроение графиков...")
    plot_results(results, output_dir='data')
    
    print("\n" + "="*70 + "\n")


def main():
    """Главная функция для запуска всех демонстраций."""
    print("\n" + "="*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №6: БИНАРНОЕ ДЕРЕВО ПОИСКА")
    print("="*70 + "\n")
    
    # 1. Основные операции
    demonstrate_basic_operations()
    
    # 2. Методы обхода
    demonstrate_traversals()
    
    # 3. Визуализация
    demonstrate_visualization()
    
    # 4. Сравнение сбалансированного и вырожденного деревьев
    demonstrate_balanced_vs_degenerate()
    
    # 5. Экспериментальное исследование
    run_performance_analysis()
    
    print("\n" + "="*70)
    print("ВСЕ ОПЕРАЦИИ ЗАВЕРШЕНЫ")
    print("="*70)
    print("\nГрафики сохранены в папку docs/")
    print("Для запуска тестов выполните: python -m pytest tests/")


if __name__ == '__main__':
    main()

