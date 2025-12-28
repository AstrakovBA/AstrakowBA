"""
Модуль для обхода графов.

Реализует алгоритмы:
1. BFS (Breadth-First Search) - обход в ширину
2. DFS (Depth-First Search) - обход в глубину (рекурсивный и итеративный)

Сложность: O(V + E), где V - количество вершин, E - количество рёбер
"""
from typing import Dict, List, Set, Optional, Tuple, Deque
from collections import deque


class GraphTraversal:
    """
    Класс для обхода графов.
    
    Работает с представлениями графов, имеющими методы:
    - get_vertices() -> List[int]
    - get_neighbors(vertex: int) -> List[Tuple[int, float]]
    """
    
    @staticmethod
    def bfs(graph, start: int) -> Tuple[Dict[int, int], Dict[int, Optional[int]]]:
        """
        Обход графа в ширину (BFS).
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф с методами get_neighbors()
            start: Начальная вершина
        
        Returns:
            Кортеж (distances, parents):
            - distances: словарь {вершина: расстояние от start}
            - parents: словарь {вершина: родительская вершина} для восстановления пути
        """
        distances: Dict[int, int] = {start: 0}
        parents: Dict[int, Optional[int]] = {start: None}
        queue: Deque[int] = deque([start])
        visited: Set[int] = {start}
        
        while queue:
            current = queue.popleft()
            current_distance = distances[current]
            
            for neighbor, _ in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = current_distance + 1
                    parents[neighbor] = current
                    queue.append(neighbor)
        
        return distances, parents
    
    @staticmethod
    def bfs_path(graph, start: int, end: int) -> Optional[List[int]]:
        """
        Поиск кратчайшего пути между двумя вершинами с помощью BFS.
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф
            start: Начальная вершина
            end: Конечная вершина
        
        Returns:
            Список вершин, образующих путь, или None, если путь не найден
        """
        distances, parents = GraphTraversal.bfs(graph, start)
        
        if end not in distances:
            return None
        
        # Восстанавливаем путь
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = parents[current]
        
        path.reverse()
        return path
    
    @staticmethod
    def dfs_recursive(graph, start: int, visited: Optional[Set[int]] = None) -> List[int]:
        """
        Обход графа в глубину (DFS) - рекурсивная версия.
        
        Сложность: O(V + E)
        Особенности: Использует стек вызовов, может переполнить стек на больших графах
        
        Args:
            graph: Граф с методом get_neighbors()
            start: Начальная вершина
            visited: Множество посещённых вершин (для внутреннего использования)
        
        Returns:
            Список вершин в порядке обхода
        """
        if visited is None:
            visited = set()
        
        visited.add(start)
        result = [start]
        
        for neighbor, _ in graph.get_neighbors(start):
            if neighbor not in visited:
                result.extend(GraphTraversal.dfs_recursive(graph, neighbor, visited))
        
        return result
    
    @staticmethod
    def dfs_iterative(graph, start: int) -> List[int]:
        """
        Обход графа в глубину (DFS) - итеративная версия.
        
        Сложность: O(V + E)
        Особенности: Использует явный стек, более безопасен для больших графов
        
        Args:
            graph: Граф с методом get_neighbors()
            start: Начальная вершина
        
        Returns:
            Список вершин в порядке обхода
        """
        visited: Set[int] = set()
        stack: List[int] = [start]
        result: List[int] = []
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                result.append(current)
                
                # Добавляем соседей в обратном порядке для сохранения естественного порядка
                neighbors = graph.get_neighbors(current)
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    @staticmethod
    def dfs_all_components(graph) -> List[List[int]]:
        """
        Находит все компоненты связности графа с помощью DFS.
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф
        
        Returns:
            Список компонент связности (каждая компонента - список вершин)
        """
        visited: Set[int] = set()
        components: List[List[int]] = []
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                # Находим все вершины в компоненте
                component = GraphTraversal.dfs_iterative_from_vertex(graph, vertex, visited)
                components.append(component)
        
        return components
    
    @staticmethod
    def dfs_iterative_from_vertex(graph, start: int, visited: Set[int]) -> List[int]:
        """
        Вспомогательный метод для DFS обхода от конкретной вершины.
        
        Args:
            graph: Граф
            start: Начальная вершина
            visited: Множество уже посещённых вершин
        
        Returns:
            Список вершин в текущей компоненте
        """
        if start in visited:
            return []
        
        component: List[int] = []
        stack: List[int] = [start]
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                component.append(current)
                
                neighbors = graph.get_neighbors(current)
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return component

