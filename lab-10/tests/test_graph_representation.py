"""
Unit-тесты для представлений графов.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.graph_representation import AdjacencyMatrix, AdjacencyList


class TestAdjacencyMatrix(unittest.TestCase):
    """Тесты для матрицы смежности"""
    
    def setUp(self):
        """Инициализация тестовых графов"""
        self.graph_undirected = AdjacencyMatrix(directed=False, weighted=False)
        self.graph_directed = AdjacencyMatrix(directed=True, weighted=True)
    
    def test_add_vertex(self):
        """Тест добавления вершин"""
        self.graph_undirected.add_vertex(1)
        self.graph_undirected.add_vertex(2)
        self.assertEqual(self.graph_undirected.get_vertex_count(), 2)
        self.assertIn(1, self.graph_undirected.get_vertices())
        self.assertIn(2, self.graph_undirected.get_vertices())
    
    def test_add_edge_undirected(self):
        """Тест добавления рёбер в неориентированном графе"""
        self.graph_undirected.add_edge(1, 2)
        self.assertTrue(self.graph_undirected.has_edge(1, 2))
        self.assertTrue(self.graph_undirected.has_edge(2, 1))  # Неориентированный
        
    def test_add_edge_directed(self):
        """Тест добавления рёбер в ориентированном графе"""
        self.graph_directed.add_edge(1, 2, 5.0)
        self.assertTrue(self.graph_directed.has_edge(1, 2))
        self.assertFalse(self.graph_directed.has_edge(2, 1))  # Ориентированный
        
    def test_add_weighted_edge(self):
        """Тест добавления взвешенного ребра"""
        self.graph_directed.add_edge(1, 2, 3.5)
        self.assertEqual(self.graph_directed.get_weight(1, 2), 3.5)
    
    def test_remove_edge(self):
        """Тест удаления ребра"""
        self.graph_undirected.add_edge(1, 2)
        self.graph_undirected.remove_edge(1, 2)
        self.assertFalse(self.graph_undirected.has_edge(1, 2))
        self.assertFalse(self.graph_undirected.has_edge(2, 1))
    
    def test_get_neighbors(self):
        """Тест получения соседей"""
        self.graph_undirected.add_edge(1, 2)
        self.graph_undirected.add_edge(1, 3)
        neighbors = self.graph_undirected.get_neighbors(1)
        neighbor_vertices = [n for n, w in neighbors]
        self.assertIn(2, neighbor_vertices)
        self.assertIn(3, neighbor_vertices)
        self.assertEqual(len(neighbors), 2)


class TestAdjacencyList(unittest.TestCase):
    """Тесты для списка смежности"""
    
    def setUp(self):
        """Инициализация тестовых графов"""
        self.graph_undirected = AdjacencyList(directed=False, weighted=False)
        self.graph_directed = AdjacencyList(directed=True, weighted=True)
    
    def test_add_vertex(self):
        """Тест добавления вершин"""
        self.graph_undirected.add_vertex(1)
        self.graph_undirected.add_vertex(2)
        self.assertEqual(self.graph_undirected.get_vertex_count(), 2)
    
    def test_add_edge_undirected(self):
        """Тест добавления рёбер в неориентированном графе"""
        self.graph_undirected.add_edge(1, 2)
        self.assertTrue(self.graph_undirected.has_edge(1, 2))
        self.assertTrue(self.graph_undirected.has_edge(2, 1))
    
    def test_add_edge_directed(self):
        """Тест добавления рёбер в ориентированном графе"""
        self.graph_directed.add_edge(1, 2, 5.0)
        self.assertTrue(self.graph_directed.has_edge(1, 2))
        self.assertFalse(self.graph_directed.has_edge(2, 1))
    
    def test_add_weighted_edge(self):
        """Тест добавления взвешенного ребра"""
        self.graph_directed.add_edge(1, 2, 3.5)
        self.assertEqual(self.graph_directed.get_weight(1, 2), 3.5)
    
    def test_remove_edge(self):
        """Тест удаления ребра"""
        self.graph_undirected.add_edge(1, 2)
        self.graph_undirected.remove_edge(1, 2)
        self.assertFalse(self.graph_undirected.has_edge(1, 2))
    
    def test_get_neighbors(self):
        """Тест получения соседей"""
        self.graph_undirected.add_edge(1, 2)
        self.graph_undirected.add_edge(1, 3)
        neighbors = self.graph_undirected.get_neighbors(1)
        neighbor_vertices = [n for n, w in neighbors]
        self.assertIn(2, neighbor_vertices)
        self.assertIn(3, neighbor_vertices)
        self.assertEqual(len(neighbors), 2)


if __name__ == '__main__':
    unittest.main()

