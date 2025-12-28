"""
Unit-тесты для алгоритмов поиска кратчайших путей и других алгоритмов.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.graph_representation import AdjacencyList, AdjacencyMatrix
from modules.shortest_path import ShortestPath, Connectivity, TopologicalSort


class TestShortestPath(unittest.TestCase):
    """Тесты для алгоритма Дейкстры"""
    
    def setUp(self):
        """Инициализация взвешенного графа"""
        self.graph = AdjacencyList(directed=False, weighted=True)
        # Граф: 1 --2-- 2 --3-- 3
        #       |       |
        #       1       4
        #       |       |
        #       4 --1-- 5
        self.graph.add_edge(1, 2, 2.0)
        self.graph.add_edge(2, 3, 3.0)
        self.graph.add_edge(1, 4, 1.0)
        self.graph.add_edge(2, 5, 4.0)
        self.graph.add_edge(4, 5, 1.0)
    
    def test_dijkstra_distances(self):
        """Тест Дейкстры: вычисление расстояний"""
        distances, parents = ShortestPath.dijkstra(self.graph, 1)
        self.assertEqual(distances[1], 0.0)
        self.assertEqual(distances[4], 1.0)
        self.assertEqual(distances[5], 2.0)  # 1 -> 4 -> 5
        self.assertEqual(distances[2], 2.0)
        self.assertEqual(distances[3], 5.0)  # 1 -> 2 -> 3
    
    def test_dijkstra_path(self):
        """Тест Дейкстры: поиск кратчайшего пути"""
        result = ShortestPath.dijkstra_path(self.graph, 1, 5)
        self.assertIsNotNone(result)
        path, distance = result
        self.assertEqual(path[0], 1)
        self.assertEqual(path[-1], 5)
        self.assertEqual(distance, 2.0)  # 1 -> 4 -> 5
        self.assertEqual(len(path), 3)
    
    def test_dijkstra_path_nonexistent(self):
        """Тест Дейкстры: путь между несвязными вершинами"""
        isolated_graph = AdjacencyList(directed=False, weighted=True)
        isolated_graph.add_edge(1, 2, 1.0)
        isolated_graph.add_vertex(3)
        
        result = ShortestPath.dijkstra_path(isolated_graph, 1, 3)
        self.assertIsNone(result)


class TestConnectivity(unittest.TestCase):
    """Тесты для компонент связности"""
    
    def test_connected_graph(self):
        """Тест связного графа"""
        graph = AdjacencyList(directed=False, weighted=False)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)
        
        self.assertTrue(Connectivity.is_connected(graph))
        components = Connectivity.find_connected_components(graph)
        self.assertEqual(len(components), 1)
    
    def test_disconnected_graph(self):
        """Тест несвязного графа"""
        graph = AdjacencyList(directed=False, weighted=False)
        graph.add_edge(1, 2)
        graph.add_edge(3, 4)
        graph.add_vertex(5)  # Изолированная вершина
        
        self.assertFalse(Connectivity.is_connected(graph))
        components = Connectivity.find_connected_components(graph)
        self.assertEqual(len(components), 3)
    
    def test_empty_graph(self):
        """Тест пустого графа"""
        graph = AdjacencyList(directed=False, weighted=False)
        self.assertTrue(Connectivity.is_connected(graph))


class TestTopologicalSort(unittest.TestCase):
    """Тесты для топологической сортировки"""
    
    def test_topological_sort_simple(self):
        """Тест простой топологической сортировки"""
        graph = AdjacencyList(directed=True, weighted=False)
        # Граф: 1 -> 2 -> 3
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        result = TopologicalSort.topological_sort(graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        # Проверяем, что 1 идет перед 2, а 2 перед 3
        self.assertLess(result.index(1), result.index(2))
        self.assertLess(result.index(2), result.index(3))
    
    def test_topological_sort_complex(self):
        """Тест сложной топологической сортировки"""
        graph = AdjacencyList(directed=True, weighted=False)
        # Граф:  1 -> 2 -> 4
        #        1 -> 3 -> 4
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        
        result = TopologicalSort.topological_sort(graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
        self.assertLess(result.index(1), result.index(2))
        self.assertLess(result.index(1), result.index(3))
        self.assertLess(result.index(2), result.index(4))
        self.assertLess(result.index(3), result.index(4))
    
    def test_topological_sort_cycle(self):
        """Тест топологической сортировки графа с циклом"""
        graph = AdjacencyList(directed=True, weighted=False)
        # Граф с циклом: 1 -> 2 -> 3 -> 1
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)
        
        result = TopologicalSort.topological_sort(graph)
        self.assertIsNone(result)  # Граф с циклом не имеет топологического порядка
    
    def test_topological_sort_dfs(self):
        """Тест топологической сортировки через DFS"""
        graph = AdjacencyList(directed=True, weighted=False)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        result = TopologicalSort.topological_sort_dfs(graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertLess(result.index(1), result.index(2))
        self.assertLess(result.index(2), result.index(3))


if __name__ == '__main__':
    unittest.main()

