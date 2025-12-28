"""
Модуль с реализацией классических жадных алгоритмов.
"""

from typing import List, Tuple, Dict
from collections import Counter, deque
import heapq


def interval_scheduling(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Задача о выборе заявок (Interval Scheduling).
    
    Выбирает максимальное количество непересекающихся интервалов.
    Жадный выбор: сортировка по времени окончания и выбор следующего
    рано заканчивающегося непересекающегося интервала.
    
    Args:
        intervals: Список интервалов в формате (начало, конец)
    
    Returns:
        Список выбранных интервалов
    
    Временная сложность: O(n log n) из-за сортировки
    """
    if not intervals:
        return []
    
    # Сортируем по времени окончания
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    
    selected = [sorted_intervals[0]]
    last_end = sorted_intervals[0][1]
    
    for start, end in sorted_intervals[1:]:
        if start >= last_end:  # Интервал не пересекается
            selected.append((start, end))
            last_end = end
    
    return selected


def fractional_knapsack(items: List[Tuple[float, float]], capacity: float) -> Tuple[float, List[Tuple[float, float]]]:
    """
    Непрерывный рюкзак (Fractional Knapsack).
    
    Максимизирует стоимость содержимого рюкзака, если можно брать
    дробные части предметов.
    Жадный выбор: сортировка по удельной стоимости (цена/вес) и
    взятие большего количества лучших предметов.
    
    Args:
        items: Список предметов в формате (вес, стоимость)
        capacity: Вместимость рюкзака
    
    Returns:
        Кортеж (максимальная стоимость, список взятых предметов в формате (вес, стоимость))
    
    Временная сложность: O(n log n) из-за сортировки
    """
    if not items or capacity <= 0:
        return 0.0, []
    
    # Вычисляем удельную стоимость и сортируем по убыванию
    items_with_ratio = [(value / weight, weight, value) for weight, value in items]
    items_with_ratio.sort(reverse=True, key=lambda x: x[0])
    
    total_value = 0.0
    remaining_capacity = capacity
    selected_items = []
    
    for ratio, weight, value in items_with_ratio:
        if remaining_capacity <= 0:
            break
        
        if weight <= remaining_capacity:
            # Берем весь предмет
            total_value += value
            remaining_capacity -= weight
            selected_items.append((weight, value))
        else:
            # Берем дробную часть
            fraction = remaining_capacity / weight
            total_value += value * fraction
            selected_items.append((remaining_capacity, value * fraction))
            remaining_capacity = 0
    
    return total_value, selected_items


class HuffmanNode:
    """Узел дерева Хаффмана."""
    
    def __init__(self, char: str = None, freq: int = 0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies: Dict[str, int]) -> HuffmanNode:
    """
    Построение дерева Хаффмана для заданных частот символов.
    
    Args:
        frequencies: Словарь частот символов
    
    Returns:
        Корневой узел дерева Хаффмана
    
    Временная сложность: O(n log n), где n - количество уникальных символов
    """
    if not frequencies:
        return None
    
    if len(frequencies) == 1:
        char = list(frequencies.keys())[0]
        return HuffmanNode(char=char, freq=frequencies[char])
    
    # Создаем приоритетную очередь (мин-кучу)
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, HuffmanNode(char=char, freq=freq))
    
    # Строим дерево
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(
            freq=left.freq + right.freq,
            left=left,
            right=right
        )
        heapq.heappush(heap, merged)
    
    return heap[0]


def build_huffman_codes(root: HuffmanNode, code: str = "", codes: Dict[str, str] = None) -> Dict[str, str]:
    """
    Построение кодов Хаффмана из дерева.
    
    Args:
        root: Корневой узел дерева
        code: Текущий код (для рекурсии)
        codes: Словарь кодов (для рекурсии)
    
    Returns:
        Словарь символов и их кодов
    """
    if codes is None:
        codes = {}
    
    if root is None:
        return codes
    
    # Если это лист
    if root.char is not None:
        if code:
            codes[root.char] = code
        else:
            codes[root.char] = "0"  # Случай одного символа
    
    build_huffman_codes(root.left, code + "0", codes)
    build_huffman_codes(root.right, code + "1", codes)
    
    return codes


def huffman_encode(text: str) -> Tuple[Dict[str, str], str]:
    """
    Кодирование текста алгоритмом Хаффмана.
    
    Args:
        text: Входной текст
    
    Returns:
        Кортеж (словарь кодов, закодированная строка)
    """
    if not text:
        return {}, ""
    
    # Подсчет частот
    frequencies = dict(Counter(text))
    
    # Построение дерева
    root = build_huffman_tree(frequencies)
    
    # Построение кодов
    codes = build_huffman_codes(root)
    
    # Кодирование
    encoded = "".join(codes[char] for char in text)
    
    return codes, encoded


def huffman_decode(encoded: str, codes: Dict[str, str]) -> str:
    """
    Декодирование текста по кодам Хаффмана.
    
    Args:
        encoded: Закодированная строка
        codes: Словарь кодов
    
    Returns:
        Декодированный текст
    """
    if not encoded or not codes:
        return ""
    
    # Создаем обратный словарь
    reverse_codes = {v: k for k, v in codes.items()}
    
    decoded = []
    current_code = ""
    
    for bit in encoded:
        current_code += bit
        if current_code in reverse_codes:
            decoded.append(reverse_codes[current_code])
            current_code = ""
    
    return "".join(decoded)


def coin_change_greedy(amount: int, coins: List[int]) -> Tuple[int, List[int]]:
    """
    Задача о минимальном количестве монет для выдачи сдачи (жадный алгоритм).
    
    ВАЖНО: Работает корректно только для канонических систем монет
    (например, стандартная система: 1, 5, 10, 25, 50, 100).
    
    Args:
        amount: Сумма для выдачи
        coins: Список номиналов монет (должен быть отсортирован по убыванию)
    
    Returns:
        Кортеж (минимальное количество монет, список использованных монет)
    
    Временная сложность: O(n), где n - количество различных номиналов
    """
    if amount <= 0:
        return 0, []
    
    # Сортируем монеты по убыванию
    sorted_coins = sorted(coins, reverse=True)
    
    result = []
    remaining = amount
    
    for coin in sorted_coins:
        count = remaining // coin
        if count > 0:
            result.extend([coin] * count)
            remaining -= coin * count
        
        if remaining == 0:
            break
    
    if remaining > 0:
        raise ValueError(f"Невозможно выдать сумму {amount} с помощью данных монет")
    
    return len(result), result


def prim_mst(graph: Dict[str, List[Tuple[str, int]]]) -> List[Tuple[str, str, int]]:
    """
    Алгоритм Прима для нахождения минимального остовного дерева.
    
    Args:
        graph: Граф в формате {вершина: [(сосед, вес), ...]}
    
    Returns:
        Список рёбер минимального остовного дерева в формате (вершина1, вершина2, вес)
    
    Временная сложность: O(E log V), где E - количество рёбер, V - количество вершин
    """
    if not graph:
        return []
    
    # Выбираем первую вершину
    start_vertex = list(graph.keys())[0]
    
    # Множества для отслеживания включенных вершин
    included = set()
    mst_edges = []
    
    # Приоритетная очередь для рёбер: (вес, вершина1, вершина2)
    edges_heap = []
    
    # Начинаем с начальной вершины
    included.add(start_vertex)
    
    # Добавляем все рёбра из начальной вершины
    for neighbor, weight in graph[start_vertex]:
        heapq.heappush(edges_heap, (weight, start_vertex, neighbor))
    
    while edges_heap and len(included) < len(graph):
        weight, u, v = heapq.heappop(edges_heap)
        
        # Пропускаем, если обе вершины уже включены
        if v in included:
            continue
        
        # Добавляем ребро в MST
        included.add(v)
        mst_edges.append((u, v, weight))
        
        # Добавляем рёбра из новой вершины
        if v in graph:
            for neighbor, edge_weight in graph[v]:
                if neighbor not in included:
                    heapq.heappush(edges_heap, (edge_weight, v, neighbor))
    
    return mst_edges

