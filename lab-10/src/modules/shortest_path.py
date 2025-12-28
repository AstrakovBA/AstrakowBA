"""
Модуль для алгоритмов поиска кратчайших путей и других алгоритмов на графах.

Реализует:
1. Алгоритм Дейкстры для поиска кратчайших путей во взвешенных графах
2. Поиск компонент связности
3. Топологическую сортировку
"""
from typing import Dict, List, Set, Optional, Tuple
from collections import deque
import heapq


class ShortestPath:
    """
    Класс для алгоритмов поиска кратчайших путей.
    """
    
    @staticmethod
    def dijkstra(graph, start: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Алгоритм Дейкстры для поиска кратчайших путей во взвешенном графе.
        
        Сложность: O((V + E) * log(V)) с использованием кучи
        Требования: Граф должен быть взвешенным, веса должны быть неотрицательными
        
        Args:
            graph: Взвешенный граф с методами get_neighbors() и get_vertices()
            start: Начальная вершина
        
        Returns:
            Кортеж (distances, parents):
            - distances: словарь {вершина: кратчайшее расстояние от start}
            - parents: словарь {вершина: родительская вершина} для восстановления пути
        """
        distances: Dict[int, float] = {v: float('inf') for v in graph.get_vertices()}
        distances[start] = 0.0
        parents: Dict[int, Optional[int]] = {v: None for v in graph.get_vertices()}
        
        # Приоритетная очередь: (расстояние, вершина)
        pq: List[Tuple[float, int]] = [(0.0, start)]
        visited: Set[int] = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor, weight in graph.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    parents[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return distances, parents
    
    @staticmethod
    def dijkstra_path(graph, start: int, end: int) -> Optional[Tuple[List[int], float]]:
        """
        Поиск кратчайшего пути между двумя вершинами с помощью алгоритма Дейкстры.
        
        Сложность: O((V + E) * log(V))
        
        Args:
            graph: Взвешенный граф
            start: Начальная вершина
            end: Конечная вершина
        
        Returns:
            Кортеж (путь, расстояние) или None, если путь не найден
        """
        distances, parents = ShortestPath.dijkstra(graph, start)
        
        if distances[end] == float('inf'):
            return None
        
        # Восстанавливаем путь
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = parents[current]
        
        path.reverse()
        return path, distances[end]


class Connectivity:
    """
    Класс для работы с компонентами связности.
    """
    
    @staticmethod
    def find_connected_components(graph) -> List[List[int]]:
        """
        Находит все компоненты связности в неориентированном графе.
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф (должен быть неориентированным)
        
        Returns:
            Список компонент связности (каждая компонента - список вершин)
        """
        visited: Set[int] = set()
        components: List[List[int]] = []
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                component = Connectivity._dfs_component(graph, vertex, visited)
                components.append(component)
        
        return components
    
    @staticmethod
    def _dfs_component(graph, start: int, visited: Set[int]) -> List[int]:
        """Вспомогательный метод для DFS обхода компоненты"""
        component: List[int] = []
        stack: List[int] = [start]
        
        while stack:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                component.append(current)
                
                for neighbor, _ in graph.get_neighbors(current):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return component
    
    @staticmethod
    def is_connected(graph) -> bool:
        """
        Проверяет, является ли граф связным.
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф
        
        Returns:
            True, если граф связный, False иначе
        """
        vertices = graph.get_vertices()
        if not vertices:
            return True
        
        components = Connectivity.find_connected_components(graph)
        return len(components) == 1


class TopologicalSort:
    """
    Класс для топологической сортировки.
    """
    
    @staticmethod
    def topological_sort(graph) -> Optional[List[int]]:
        """
        Топологическая сортировка для ориентированного ациклического графа (DAG).
        
        Сложность: O(V + E)
        
        Args:
            graph: Ориентированный граф (должен быть DAG)
        
        Returns:
            Список вершин в топологическом порядке или None, если граф содержит цикл
        """
        if not graph.directed:
            raise ValueError("Топологическая сортировка работает только для ориентированных графов")
        
        # Вычисляем степени входа
        in_degree: Dict[int, int] = {v: 0 for v in graph.get_vertices()}
        
        for u in graph.get_vertices():
            for v, _ in graph.get_neighbors(u):
                in_degree[v] = in_degree.get(v, 0) + 1
        
        # Инициализируем очередь вершинами с нулевой степенью входа
        queue: deque = deque([v for v, degree in in_degree.items() if degree == 0])
        result: List[int] = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            # Уменьшаем степени входа соседей
            for neighbor, _ in graph.get_neighbors(current):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Если количество вершин в результате не совпадает с общим количеством,
        # значит граф содержит цикл
        if len(result) != len(graph.get_vertices()):
            return None
        
        return result
    
    @staticmethod
    def topological_sort_dfs(graph) -> Optional[List[int]]:
        """
        Топологическая сортировка с использованием DFS.
        
        Сложность: O(V + E)
        
        Args:
            graph: Ориентированный граф
        
        Returns:
            Список вершин в топологическом порядке или None, если граф содержит цикл
        """
        if not graph.directed:
            raise ValueError("Топологическая сортировка работает только для ориентированных графов")
        
        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        result: List[int] = []
        
        def dfs(vertex: int) -> bool:
            """Возвращает False, если обнаружен цикл"""
            if vertex in rec_stack:
                return False  # Обнаружен цикл
            
            if vertex in visited:
                return True
            
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor, _ in graph.get_neighbors(vertex):
                if not dfs(neighbor):
                    return False
            
            rec_stack.remove(vertex)
            result.append(vertex)
            return True
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                if not dfs(vertex):
                    return None
        
        result.reverse()
        return result

