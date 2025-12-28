"""
Модуль для представления графов различными способами.

Реализует два основных представления:
1. Матрица смежности (AdjacencyMatrix)
2. Список смежности (AdjacencyList)

Для каждого представления указана сложность операций и потребление памяти.
"""
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class AdjacencyMatrix:
    """
    Представление графа через матрицу смежности.
    
    Память: O(V²), где V - количество вершин
    Сложность операций:
    - Добавление/удаление ребра: O(1)
    - Проверка наличия ребра: O(1)
    - Получение соседей: O(V)
    - Добавление вершины: O(V²) (требует пересоздания матрицы)
    """
    
    def __init__(self, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа.
        
        Args:
            directed: Если True, граф ориентированный
            weighted: Если True, граф взвешенный
        """
        self.directed = directed
        self.weighted = weighted
        self.vertices: Dict[int, int] = {}  # vertex -> index mapping
        self.index_to_vertex: Dict[int, int] = {}  # index -> vertex mapping
        self.matrix: List[List[Optional[float]]] = []
        self.vertex_count = 0
        
    def add_vertex(self, vertex: int) -> None:
        """Добавление вершины. Сложность: O(V²)"""
        if vertex in self.vertices:
            return
        
        # Добавляем новую вершину
        self.vertices[vertex] = self.vertex_count
        self.index_to_vertex[self.vertex_count] = vertex
        
        # Расширяем матрицу
        new_size = self.vertex_count + 1
        new_matrix = [[None] * new_size for _ in range(new_size)]
        
        # Копируем старую матрицу
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                new_matrix[i][j] = self.matrix[i][j]
        
        self.matrix = new_matrix
        self.vertex_count += 1
    
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """
        Добавление ребра. Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенных графов)
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        u_idx = self.vertices[u]
        v_idx = self.vertices[v]
        
        self.matrix[u_idx][v_idx] = weight
        
        if not self.directed:
            self.matrix[v_idx][u_idx] = weight
    
    def remove_edge(self, u: int, v: int) -> None:
        """Удаление ребра. Сложность: O(1)"""
        if u not in self.vertices or v not in self.vertices:
            return
        
        u_idx = self.vertices[u]
        v_idx = self.vertices[v]
        
        self.matrix[u_idx][v_idx] = None
        
        if not self.directed:
            self.matrix[v_idx][u_idx] = None
    
    def has_edge(self, u: int, v: int) -> bool:
        """Проверка наличия ребра. Сложность: O(1)"""
        if u not in self.vertices or v not in self.vertices:
            return False
        
        u_idx = self.vertices[u]
        v_idx = self.vertices[v]
        
        return self.matrix[u_idx][v_idx] is not None
    
    def get_weight(self, u: int, v: int) -> Optional[float]:
        """Получение веса ребра. Сложность: O(1)"""
        if not self.has_edge(u, v):
            return None
        
        u_idx = self.vertices[u]
        v_idx = self.vertices[v]
        
        return self.matrix[u_idx][v_idx]
    
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """
        Получение списка соседей вершины. Сложность: O(V)
        
        Returns:
            Список кортежей (сосед, вес)
        """
        if vertex not in self.vertices:
            return []
        
        neighbors = []
        vertex_idx = self.vertices[vertex]
        
        for i in range(self.vertex_count):
            if self.matrix[vertex_idx][i] is not None:
                neighbor = self.index_to_vertex[i]
                weight = self.matrix[vertex_idx][i]
                neighbors.append((neighbor, weight))
        
        return neighbors
    
    def get_vertices(self) -> List[int]:
        """Получение списка всех вершин. Сложность: O(V)"""
        return list(self.vertices.keys())
    
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """Получение списка всех рёбер. Сложность: O(V²)"""
        edges = []
        visited_edges = set()
        
        for u in self.vertices:
            u_idx = self.vertices[u]
            for i in range(self.vertex_count):
                if self.matrix[u_idx][i] is not None:
                    v = self.index_to_vertex[i]
                    edge_key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                    
                    if edge_key not in visited_edges:
                        weight = self.matrix[u_idx][i]
                        edges.append((u, v, weight))
                        visited_edges.add(edge_key)
        
        return edges
    
    def get_vertex_count(self) -> int:
        """Количество вершин"""
        return self.vertex_count
    
    def get_edge_count(self) -> int:
        """Количество рёбер"""
        edges = self.get_edges()
        return len(edges)
    
    def __str__(self) -> str:
        """Строковое представление графа"""
        result = f"AdjacencyMatrix(directed={self.directed}, weighted={self.weighted})\n"
        result += f"Vertices: {self.get_vertices()}\n"
        result += f"Edges: {self.get_edges()}\n"
        return result


class AdjacencyList:
    """
    Представление графа через список смежности.
    
    Память: O(V + E), где V - количество вершин, E - количество рёбер
    Сложность операций:
    - Добавление ребра: O(1)
    - Удаление ребра: O(degree(v))
    - Проверка наличия ребра: O(degree(v))
    - Получение соседей: O(degree(v))
    - Добавление вершины: O(1)
    """
    
    def __init__(self, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа.
        
        Args:
            directed: Если True, граф ориентированный
            weighted: Если True, граф взвешенный
        """
        self.directed = directed
        self.weighted = weighted
        self.graph: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    
    def add_vertex(self, vertex: int) -> None:
        """Добавление вершины. Сложность: O(1)"""
        if vertex not in self.graph:
            self.graph[vertex] = []
    
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """
        Добавление ребра. Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенных графов)
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        self.graph[u].append((v, weight))
        
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def remove_edge(self, u: int, v: int) -> None:
        """Удаление ребра. Сложность: O(degree(u))"""
        if u not in self.graph:
            return
        
        # Удаляем (v, weight) из списка u
        self.graph[u] = [(neighbor, w) for neighbor, w in self.graph[u] if neighbor != v]
        
        if not self.directed and v in self.graph:
            # Удаляем (u, weight) из списка v
            self.graph[v] = [(neighbor, w) for neighbor, w in self.graph[v] if neighbor != u]
    
    def has_edge(self, u: int, v: int) -> bool:
        """Проверка наличия ребра. Сложность: O(degree(u))"""
        if u not in self.graph:
            return False
        
        return any(neighbor == v for neighbor, _ in self.graph[u])
    
    def get_weight(self, u: int, v: int) -> Optional[float]:
        """Получение веса ребра. Сложность: O(degree(u))"""
        if u not in self.graph:
            return None
        
        for neighbor, weight in self.graph[u]:
            if neighbor == v:
                return weight
        
        return None
    
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """
        Получение списка соседей вершины. Сложность: O(degree(vertex))
        
        Returns:
            Список кортежей (сосед, вес)
        """
        return list(self.graph.get(vertex, []))
    
    def get_vertices(self) -> List[int]:
        """Получение списка всех вершин. Сложность: O(V)"""
        return list(self.graph.keys())
    
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """Получение списка всех рёбер. Сложность: O(V + E)"""
        edges = []
        visited_edges = set()
        
        for u in self.graph:
            for v, weight in self.graph[u]:
                edge_key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                
                if edge_key not in visited_edges:
                    edges.append((u, v, weight))
                    visited_edges.add(edge_key)
        
        return edges
    
    def get_vertex_count(self) -> int:
        """Количество вершин"""
        return len(self.graph)
    
    def get_edge_count(self) -> int:
        """Количество рёбер"""
        edges = self.get_edges()
        return len(edges)
    
    def __str__(self) -> str:
        """Строковое представление графа"""
        result = f"AdjacencyList(directed={self.directed}, weighted={self.weighted})\n"
        result += f"Vertices: {self.get_vertices()}\n"
        result += f"Edges: {self.get_edges()}\n"
        return result

