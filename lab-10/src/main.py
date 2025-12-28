"""
Основной файл для запуска экспериментов и практических задач на графах.

Выполняет:
1. Сравнительный анализ эффективности представлений графов
2. Визуализацию графов и результатов
3. Практические задачи (лабиринт, связность сети, топологическая сортировка)
"""
import time
import random
import os
import sys
from typing import List, Tuple, Dict, Optional
import matplotlib.pyplot as plt
import numpy as np

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

from modules.graph_representation import AdjacencyMatrix, AdjacencyList
from modules.graph_traversal import GraphTraversal
from modules.shortest_path import ShortestPath, Connectivity, TopologicalSort


def generate_random_graph(vertex_count: int, edge_probability: float, 
                         weighted: bool = False, directed: bool = False):
    """
    Генерация случайного графа.
    
    Args:
        vertex_count: Количество вершин
        edge_probability: Вероятность наличия ребра между парой вершин
        weighted: Если True, генерирует взвешенный граф
        directed: Если True, генерирует ориентированный граф
    """
    matrix_graph = AdjacencyMatrix(directed=directed, weighted=weighted)
    list_graph = AdjacencyList(directed=directed, weighted=weighted)
    
    for i in range(vertex_count):
        matrix_graph.add_vertex(i)
        list_graph.add_vertex(i)
    
    for i in range(vertex_count):
        for j in range(vertex_count):
            if i != j and (not directed or i < j):
                if random.random() < edge_probability:
                    weight = random.uniform(1.0, 10.0) if weighted else 1.0
                    matrix_graph.add_edge(i, j, weight)
                    list_graph.add_edge(i, j, weight)
    
    return matrix_graph, list_graph


def benchmark_operations(vertex_counts: List[int], edge_probability: float = 0.3):
    """
    Бенчмарк операций для разных представлений графов.
    
    Returns:
        Словарь с результатами замеров времени
    """
    results = {
        'vertex_counts': vertex_counts,
        'matrix_add_edge': [],
        'list_add_edge': [],
        'matrix_get_neighbors': [],
        'list_get_neighbors': [],
        'matrix_has_edge': [],
        'list_has_edge': [],
    }
    
    for v_count in vertex_counts:
        print(f"Тестирование с {v_count} вершинами...")
        matrix_graph, list_graph = generate_random_graph(v_count, edge_probability)
        
        # Тест добавления ребра
        start = time.perf_counter()
        for _ in range(100):
            u, v = random.randint(0, v_count - 1), random.randint(0, v_count - 1)
            if u != v:
                matrix_graph.add_edge(u, v)
        results['matrix_add_edge'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for _ in range(100):
            u, v = random.randint(0, v_count - 1), random.randint(0, v_count - 1)
            if u != v:
                list_graph.add_edge(u, v)
        results['list_add_edge'].append(time.perf_counter() - start)
        
        # Тест получения соседей
        start = time.perf_counter()
        for _ in range(100):
            vertex = random.randint(0, v_count - 1)
            matrix_graph.get_neighbors(vertex)
        results['matrix_get_neighbors'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for _ in range(100):
            vertex = random.randint(0, v_count - 1)
            list_graph.get_neighbors(vertex)
        results['list_get_neighbors'].append(time.perf_counter() - start)
        
        # Тест проверки наличия ребра
        vertices = list(range(v_count))
        edges_to_test = [(random.choice(vertices), random.choice(vertices)) 
                         for _ in range(100)]
        
        start = time.perf_counter()
        for u, v in edges_to_test:
            matrix_graph.has_edge(u, v)
        results['matrix_has_edge'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for u, v in edges_to_test:
            list_graph.has_edge(u, v)
        results['list_has_edge'].append(time.perf_counter() - start)
    
    return results


def benchmark_algorithms(vertex_counts: List[int], edge_probability: float = 0.3):
    """
    Бенчмарк алгоритмов обхода для разных представлений.
    
    Returns:
        Словарь с результатами замеров времени
    """
    results = {
        'vertex_counts': vertex_counts,
        'matrix_bfs': [],
        'list_bfs': [],
        'matrix_dfs_iterative': [],
        'list_dfs_iterative': [],
        'matrix_dfs_recursive': [],
        'list_dfs_recursive': [],
    }
    
    for v_count in vertex_counts:
        print(f"Тестирование алгоритмов с {v_count} вершинами...")
        matrix_graph, list_graph = generate_random_graph(v_count, edge_probability)
        
        if v_count == 0:
            continue
        
        start_vertex = 0
        
        # BFS
        start = time.perf_counter()
        GraphTraversal.bfs(matrix_graph, start_vertex)
        results['matrix_bfs'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        GraphTraversal.bfs(list_graph, start_vertex)
        results['list_bfs'].append(time.perf_counter() - start)
        
        # DFS итеративный
        start = time.perf_counter()
        GraphTraversal.dfs_iterative(matrix_graph, start_vertex)
        results['matrix_dfs_iterative'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        GraphTraversal.dfs_iterative(list_graph, start_vertex)
        results['list_dfs_iterative'].append(time.perf_counter() - start)
        
        # DFS рекурсивный (только для небольших графов)
        if v_count <= 1000:
            try:
                start = time.perf_counter()
                GraphTraversal.dfs_recursive(matrix_graph, start_vertex)
                results['matrix_dfs_recursive'].append(time.perf_counter() - start)
                
                start = time.perf_counter()
                GraphTraversal.dfs_recursive(list_graph, start_vertex)
                results['list_dfs_recursive'].append(time.perf_counter() - start)
            except RecursionError:
                results['matrix_dfs_recursive'].append(None)
                results['list_dfs_recursive'].append(None)
        else:
            results['matrix_dfs_recursive'].append(None)
            results['list_dfs_recursive'].append(None)
    
    return results


def visualize_benchmark_results(operations_results: Dict, algorithms_results: Dict):
    """Визуализация результатов бенчмарков"""
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # График операций
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    vertex_counts = operations_results['vertex_counts']
    
    # Добавление ребра
    axes[0, 0].plot(vertex_counts, operations_results['matrix_add_edge'], 
                    'o-', label='Матрица смежности', linewidth=2)
    axes[0, 0].plot(vertex_counts, operations_results['list_add_edge'], 
                    's-', label='Список смежности', linewidth=2)
    axes[0, 0].set_xlabel('Количество вершин')
    axes[0, 0].set_ylabel('Время (секунды)')
    axes[0, 0].set_title('Добавление ребра (100 операций)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Получение соседей
    axes[0, 1].plot(vertex_counts, operations_results['matrix_get_neighbors'], 
                    'o-', label='Матрица смежности', linewidth=2)
    axes[0, 1].plot(vertex_counts, operations_results['list_get_neighbors'], 
                    's-', label='Список смежности', linewidth=2)
    axes[0, 1].set_xlabel('Количество вершин')
    axes[0, 1].set_ylabel('Время (секунды)')
    axes[0, 1].set_title('Получение соседей (100 операций)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Проверка наличия ребра
    axes[1, 0].plot(vertex_counts, operations_results['matrix_has_edge'], 
                    'o-', label='Матрица смежности', linewidth=2)
    axes[1, 0].plot(vertex_counts, operations_results['list_has_edge'], 
                    's-', label='Список смежности', linewidth=2)
    axes[1, 0].set_xlabel('Количество вершин')
    axes[1, 0].set_ylabel('Время (секунды)')
    axes[1, 0].set_title('Проверка наличия ребра (100 операций)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Сравнение памяти (приблизительно)
    memory_matrix = [v * v for v in vertex_counts]  # O(V²)
    memory_list = [v * v * 0.3 * 2 for v in vertex_counts]  # O(V + E), E ≈ V² * 0.3
    
    axes[1, 1].plot(vertex_counts, memory_matrix, 'o-', 
                    label='Матрица смежности O(V²)', linewidth=2)
    axes[1, 1].plot(vertex_counts, memory_list, 's-', 
                    label='Список смежности O(V + E)', linewidth=2)
    axes[1, 1].set_xlabel('Количество вершин')
    axes[1, 1].set_ylabel('Потребление памяти (относительно)')
    axes[1, 1].set_title('Потребление памяти')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(docs_dir, 'benchmark_operations.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График операций сохранён в docs/benchmark_operations.png")
    
    # График алгоритмов
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    vertex_counts_alg = algorithms_results['vertex_counts']
    
    # BFS
    axes[0, 0].plot(vertex_counts_alg, algorithms_results['matrix_bfs'], 
                    'o-', label='Матрица смежности', linewidth=2)
    axes[0, 0].plot(vertex_counts_alg, algorithms_results['list_bfs'], 
                    's-', label='Список смежности', linewidth=2)
    axes[0, 0].set_xlabel('Количество вершин')
    axes[0, 0].set_ylabel('Время (секунды)')
    axes[0, 0].set_title('BFS (обход в ширину)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # DFS итеративный
    axes[0, 1].plot(vertex_counts_alg, algorithms_results['matrix_dfs_iterative'], 
                    'o-', label='Матрица смежности', linewidth=2)
    axes[0, 1].plot(vertex_counts_alg, algorithms_results['list_dfs_iterative'], 
                    's-', label='Список смежности', linewidth=2)
    axes[0, 1].set_xlabel('Количество вершин')
    axes[0, 1].set_ylabel('Время (секунды)')
    axes[0, 1].set_title('DFS итеративный')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # DFS рекурсивный (только валидные значения)
    valid_counts = [v for i, v in enumerate(vertex_counts_alg) 
                    if algorithms_results['matrix_dfs_recursive'][i] is not None]
    valid_matrix_dfs = [t for t in algorithms_results['matrix_dfs_recursive'] if t is not None]
    valid_list_dfs = [t for i, t in enumerate(algorithms_results['list_dfs_recursive']) 
                      if algorithms_results['matrix_dfs_recursive'][i] is not None]
    
    if valid_counts:
        axes[1, 0].plot(valid_counts, valid_matrix_dfs, 'o-', 
                        label='Матрица смежности', linewidth=2)
        axes[1, 0].plot(valid_counts, valid_list_dfs, 's-', 
                        label='Список смежности', linewidth=2)
        axes[1, 0].set_xlabel('Количество вершин')
        axes[1, 0].set_ylabel('Время (секунды)')
        axes[1, 0].set_title('DFS рекурсивный')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    
    # Сравнение BFS и DFS
    axes[1, 1].plot(vertex_counts_alg, algorithms_results['list_bfs'], 
                    'o-', label='BFS', linewidth=2)
    axes[1, 1].plot(vertex_counts_alg, algorithms_results['list_dfs_iterative'], 
                    's-', label='DFS итеративный', linewidth=2)
    axes[1, 1].set_xlabel('Количество вершин')
    axes[1, 1].set_ylabel('Время (секунды)')
    axes[1, 1].set_title('Сравнение BFS и DFS (список смежности)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(docs_dir, 'benchmark_algorithms.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"График алгоритмов сохранён в docs/benchmark_algorithms.png")


def solve_maze_shortest_path(maze: List[List[int]], start: Tuple[int, int], 
                             end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Решение задачи поиска кратчайшего пути в лабиринте.
    
    Лабиринт представлен матрицей: 0 - проход, 1 - стена
    
    Args:
        maze: Матрица лабиринта
        start: Начальная позиция (row, col)
        end: Конечная позиция (row, col)
    
    Returns:
        Список позиций, образующих кратчайший путь, или None
    """
    rows, cols = len(maze), len(maze[0])
    
    # Преобразуем лабиринт в граф
    graph = AdjacencyList(directed=False, weighted=False)
    
    # Добавляем вершины для всех проходов
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0:
                graph.add_vertex((i, j))
    
    # Добавляем рёбра между соседними проходами
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 0:
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] == 0:
                        graph.add_edge((i, j), (ni, nj))
    
    # Используем BFS для поиска кратчайшего пути
    path = GraphTraversal.bfs_path(graph, start, end)
    return path


def visualize_maze_solution(maze: List[List[int]], start: Tuple[int, int], 
                           end: Tuple[int, int], path: Optional[List[Tuple[int, int]]]):
    """Визуализация решения лабиринта"""
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Отображаем лабиринт
    maze_array = np.array(maze)
    ax.imshow(maze_array, cmap='gray_r', interpolation='nearest')
    
    # Отображаем путь
    if path:
        path_array = np.array(path)
        ax.plot(path_array[:, 1], path_array[:, 0], 'r-', linewidth=2, label='Путь')
        ax.plot(path_array[0, 1], path_array[0, 0], 'go', markersize=15, label='Старт')
        ax.plot(path_array[-1, 1], path_array[-1, 0], 'ro', markersize=15, label='Финиш')
    else:
        ax.plot(start[1], start[0], 'go', markersize=15, label='Старт')
        ax.plot(end[1], end[0], 'ro', markersize=15, label='Финиш')
    
    ax.set_title('Кратчайший путь в лабиринте')
    ax.legend()
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(docs_dir, 'maze_solution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Решение лабиринта сохранено в docs/maze_solution.png")


def solve_network_connectivity(graph):
    """Решение задачи определения связности сети"""
    is_connected = Connectivity.is_connected(graph)
    components = Connectivity.find_connected_components(graph)
    
    print(f"\n=== Анализ связности сети ===")
    print(f"Граф связный: {'Да' if is_connected else 'Нет'}")
    print(f"Количество компонент связности: {len(components)}")
    
    for i, component in enumerate(components, 1):
        print(f"Компонента {i}: {component}")
    
    return is_connected, components


def solve_topological_sort_task():
    """Решение задачи на топологическую сортировку"""
    # Пример: задачи проекта с зависимостями
    graph = AdjacencyList(directed=True, weighted=False)
    
    # Задачи проекта: 0-планирование, 1-дизайн, 2-разработка, 3-тестирование, 4-деплой
    graph.add_edge(0, 1)  # Планирование -> Дизайн
    graph.add_edge(1, 2)  # Дизайн -> Разработка
    graph.add_edge(2, 3)  # Разработка -> Тестирование
    graph.add_edge(3, 4)  # Тестирование -> Деплой
    graph.add_edge(0, 2)  # Планирование -> Разработка (параллельная ветка)
    
    print(f"\n=== Топологическая сортировка ===")
    print("Граф зависимостей задач проекта:")
    print("0 - Планирование")
    print("1 - Дизайн")
    print("2 - Разработка")
    print("3 - Тестирование")
    print("4 - Деплой")
    
    topological_order = TopologicalSort.topological_sort(graph)
    
    if topological_order:
        print(f"\nПорядок выполнения задач: {topological_order}")
        task_names = ['Планирование', 'Дизайн', 'Разработка', 'Тестирование', 'Деплой']
        print("Детальный порядок:")
        for i, task in enumerate(topological_order, 1):
            print(f"{i}. {task_names[task]}")
    else:
        print("\nОшибка: граф содержит циклы, топологическая сортировка невозможна")
    
    return topological_order


def visualize_graph(graph, title: str, filename: str, pos: Dict = None):
    """Визуализация графа с помощью matplotlib"""
    try:
        import networkx as nx
        
        docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # Создаём NetworkX граф
        if graph.directed:
            nx_graph = nx.DiGraph()
        else:
            nx_graph = nx.Graph()
        
        # Добавляем рёбра
        for u, v, weight in graph.get_edges():
            nx_graph.add_edge(u, v, weight=weight)
        
        # Если позиции не заданы, вычисляем их
        if pos is None:
            pos = nx.spring_layout(nx_graph, k=1, iterations=50)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Рисуем граф
        nx.draw(nx_graph, pos, ax=ax, with_labels=True, 
                node_color='lightblue', node_size=1000,
                font_size=10, font_weight='bold',
                arrows=graph.directed, arrowsize=20)
        
        # Добавляем веса рёбер, если граф взвешенный
        if graph.weighted:
            edge_labels = {(u, v): f'{w:.1f}' 
                          for u, v, w in graph.get_edges()}
            nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels, ax=ax, font_size=8)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(docs_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Граф сохранён в docs/{filename}")
        
    except ImportError:
        print("NetworkX не установлен, визуализация графа пропущена")


def main():
    """Основная функция для запуска всех экспериментов и задач"""
    print("=" * 60)
    print("Лабораторная работа: Алгоритмы на графах")
    print("=" * 60)
    
    # 1. Бенчмарк операций
    print("\n1. Сравнительный анализ операций...")
    vertex_counts_ops = [10, 50, 100, 200, 500]
    operations_results = benchmark_operations(vertex_counts_ops, edge_probability=0.3)
    
    # 2. Бенчмарк алгоритмов
    print("\n2. Сравнительный анализ алгоритмов...")
    vertex_counts_alg = [10, 50, 100, 200, 500]
    algorithms_results = benchmark_algorithms(vertex_counts_alg, edge_probability=0.3)
    
    # 3. Визуализация результатов
    print("\n3. Создание графиков...")
    visualize_benchmark_results(operations_results, algorithms_results)
    
    # 4. Задача 1: Кратчайший путь в лабиринте
    print("\n4. Задача: Кратчайший путь в лабиринте")
    maze = [
        [0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    start_pos = (0, 0)
    end_pos = (5, 5)
    
    path = solve_maze_shortest_path(maze, start_pos, end_pos)
    if path:
        print(f"Найден путь длиной {len(path) - 1} шагов")
        print(f"Путь: {path}")
    else:
        print("Путь не найден")
    
    visualize_maze_solution(maze, start_pos, end_pos, path)
    
    # 5. Задача 2: Связность сети
    print("\n5. Задача: Определение связности сети")
    network_graph = AdjacencyList(directed=False, weighted=False)
    # Создаём сеть с несколькими компонентами
    network_graph.add_edge(1, 2)
    network_graph.add_edge(2, 3)
    network_graph.add_edge(4, 5)
    network_graph.add_vertex(6)  # Изолированная вершина
    
    solve_network_connectivity(network_graph)
    visualize_graph(network_graph, "Сеть (анализ связности)", "network_connectivity.png")
    
    # 6. Задача 3: Топологическая сортировка
    print("\n6. Задача: Топологическая сортировка")
    solve_topological_sort_task()
    
    # Дополнительная визуализация: пример графа
    example_graph = AdjacencyList(directed=False, weighted=True)
    example_graph.add_edge(1, 2, 3.0)
    example_graph.add_edge(2, 3, 5.0)
    example_graph.add_edge(1, 4, 2.0)
    example_graph.add_edge(4, 5, 1.0)
    example_graph.add_edge(2, 5, 4.0)
    
    visualize_graph(example_graph, "Пример взвешенного графа", "example_graph.png")
    
    # Тест Дейкстры на примере
    print("\n7. Тест алгоритма Дейкстры на примере графа")
    distances, parents = ShortestPath.dijkstra(example_graph, 1)
    print(f"Кратчайшие расстояния от вершины 1: {distances}")
    
    path_1_to_5 = ShortestPath.dijkstra_path(example_graph, 1, 5)
    if path_1_to_5:
        path, dist = path_1_to_5
        print(f"Кратчайший путь от 1 до 5: {path}, расстояние: {dist}")
    
    print("\n" + "=" * 60)
    print("Все эксперименты завершены!")
    print("Графики сохранены в папке docs/")
    print("=" * 60)


if __name__ == '__main__':
    main()

