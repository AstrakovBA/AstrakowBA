"""
Unit-тесты для алгоритмов обхода графов.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.graph_representation import AdjacencyList
from modules.graph_traversal import GraphTraversal


class TestGraphTraversal(unittest.TestCase):
    """Тесты для алгоритмов обхода"""
    
    def setUp(self):
        """Инициализация тестового графа"""
        self.graph = AdjacencyList(directed=False, weighted=False)
        # Граф: 1-2-3
        #       | |
        #       4-5
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(1, 4)
        self.graph.add_edge(2, 5)
        self.graph.add_edge(4, 5)
    
    def test_bfs_distances(self):
        """Тест BFS: вычисление расстояний"""
        distances, parents = GraphTraversal.bfs(self.graph, 1)
        self.assertEqual(distances[1], 0)
        self.assertEqual(distances[2], 1)
        self.assertEqual(distances[3], 2)
        self.assertEqual(distances[4], 1)
        self.assertEqual(distances[5], 2)
    
    def test_bfs_path(self):
        """Тест BFS: поиск пути"""
        path = GraphTraversal.bfs_path(self.graph, 1, 3)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 1)
        self.assertEqual(path[-1], 3)
        self.assertEqual(len(path), 3)  # 1 -> 2 -> 3
    
    def test_bfs_path_nonexistent(self):
        """Тест BFS: путь между несвязными вершинами"""
        isolated_graph = AdjacencyList(directed=False, weighted=False)
        isolated_graph.add_edge(1, 2)
        isolated_graph.add_vertex(3)  # Изолированная вершина
        
        path = GraphTraversal.bfs_path(isolated_graph, 1, 3)
        self.assertIsNone(path)
    
    def test_dfs_recursive(self):
        """Тест DFS: рекурсивная версия"""
        result = GraphTraversal.dfs_recursive(self.graph, 1)
        self.assertEqual(len(result), 5)  # Все вершины должны быть посещены
        self.assertEqual(result[0], 1)  # Начинается с стартовой вершины
        self.assertEqual(len(set(result)), 5)  # Все вершины уникальны
    
    def test_dfs_iterative(self):
        """Тест DFS: итеративная версия"""
        result = GraphTraversal.dfs_iterative(self.graph, 1)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], 1)
        self.assertEqual(len(set(result)), 5)
    
    def test_dfs_all_components(self):
        """Тест DFS: поиск всех компонент связности"""
        # Граф с двумя компонентами
        disconnected_graph = AdjacencyList(directed=False, weighted=False)
        disconnected_graph.add_edge(1, 2)
        disconnected_graph.add_edge(2, 3)
        disconnected_graph.add_edge(4, 5)
        
        components = GraphTraversal.dfs_all_components(disconnected_graph)
        self.assertEqual(len(components), 2)
        # Проверяем, что все вершины присутствуют
        all_vertices = set()
        for component in components:
            all_vertices.update(component)
        self.assertEqual(all_vertices, {1, 2, 3, 4, 5})


if __name__ == '__main__':
    unittest.main()

