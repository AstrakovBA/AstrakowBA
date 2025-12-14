"""
Модуль с реализацией классических алгоритмов динамического программирования.
"""

from functools import lru_cache
from typing import List, Tuple, Dict, Optional


# ==================== ЧИСЛА ФИБОНАЧЧИ ====================

def fibonacci_naive(n: int) -> int:
    """
    Наивная рекурсивная реализация чисел Фибоначчи.
    
    Временная сложность: O(2^n)
    Пространственная сложность: O(n) (глубина стека)
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoized(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    Рекурсивная реализация с мемоизацией (нисходящий подход).
    
    Временная сложность: O(n)
    Пространственная сложность: O(n)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru_cache(n: int) -> int:
    """
    Рекурсивная реализация с использованием декоратора lru_cache.
    
    Временная сложность: O(n)
    Пространственная сложность: O(n)
    """
    if n <= 1:
        return n
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)


def fibonacci_bottom_up(n: int) -> int:
    """
    Итеративная реализация (восходящий подход).
    
    Временная сложность: O(n)
    Пространственная сложность: O(1)
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ==================== ЗАДАЧА О РЮКЗАКЕ (0-1 KNAPSACK) ====================

def knapsack_01_bottom_up(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    Решение задачи о рюкзаке 0-1 восходящим подходом.
    
    Args:
        weights: веса предметов
        values: стоимости предметов
        capacity: вместимость рюкзака
    
    Returns:
        Tuple[максимальная стоимость, список индексов выбранных предметов]
    
    Временная сложность: O(n * W), где n - количество предметов, W - вместимость
    Пространственная сложность: O(n * W)
    """
    n = len(weights)
    # dp[i][w] - максимальная стоимость для первых i предметов с вместимостью w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Заполняем таблицу
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Не берем предмет i
            dp[i][w] = dp[i - 1][w]
            # Пытаемся взять предмет i
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    # Восстановление решения
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    selected_items.reverse()
    return dp[n][capacity], selected_items


def knapsack_01_get_table(weights: List[int], values: List[int], capacity: int) -> List[List[int]]:
    """
    Получить таблицу ДП для задачи о рюкзаке (для визуализации).
    """
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    return dp


# ==================== НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS) ====================

def lcs_bottom_up(s1: str, s2: str) -> Tuple[int, str]:
    """
    Нахождение наибольшей общей подпоследовательности восходящим подходом.
    
    Args:
        s1, s2: входные строки
    
    Returns:
        Tuple[длина LCS, сама подпоследовательность]
    
    Временная сложность: O(m * n), где m и n - длины строк
    Пространственная сложность: O(m * n)
    """
    m, n = len(s1), len(s2)
    # dp[i][j] - длина LCS для s1[0:i] и s2[0:j]
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Заполняем таблицу
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Восстановление подпоследовательности
    lcs_string = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_string.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    lcs_string.reverse()
    return dp[m][n], ''.join(lcs_string)


def lcs_get_table(s1: str, s2: str) -> List[List[int]]:
    """
    Получить таблицу ДП для LCS (для визуализации).
    """
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp


# ==================== РАССТОЯНИЕ ЛЕВЕНШТЕЙНА ====================

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Вычисление расстояния Левенштейна (редакционного расстояния).
    
    Args:
        s1, s2: входные строки
    
    Returns:
        Минимальное количество операций для преобразования s1 в s2
    
    Временная сложность: O(m * n)
    Пространственная сложность: O(m * n)
    """
    m, n = len(s1), len(s2)
    # dp[i][j] - расстояние между s1[0:i] и s2[0:j]
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Базовые случаи
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Заполняем таблицу
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # удаление
                    dp[i][j - 1],      # вставка
                    dp[i - 1][j - 1]   # замена
                )
    
    return dp[m][n]


def levenshtein_get_table(s1: str, s2: str) -> List[List[int]]:
    """
    Получить таблицу ДП для расстояния Левенштейна (для визуализации).
    """
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )
    
    return dp


# ==================== РАЗМЕН МОНЕТ ====================

def coin_change_min_coins(coins: List[int], amount: int) -> int:
    """
    Минимальное количество монет для размена суммы.
    
    Args:
        coins: номиналы монет
        amount: сумма для размена
    
    Returns:
        Минимальное количество монет или -1, если размен невозможен
    
    Временная сложность: O(amount * len(coins))
    Пространственная сложность: O(amount)
    """
    # dp[i] - минимальное количество монет для суммы i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Количество способов размена суммы.
    
    Args:
        coins: номиналы монет
        amount: сумма для размена
    
    Returns:
        Количество способов размена
    
    Временная сложность: O(amount * len(coins))
    Пространственная сложность: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


# ==================== НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS) ====================

def longest_increasing_subsequence(arr: List[int]) -> Tuple[int, List[int]]:
    """
    Нахождение наибольшей возрастающей подпоследовательности.
    
    Args:
        arr: входной массив
    
    Returns:
        Tuple[длина LIS, сама подпоследовательность]
    
    Временная сложность: O(n^2)
    Пространственная сложность: O(n)
    """
    n = len(arr)
    if n == 0:
        return 0, []
    
    # dp[i] - длина LIS, заканчивающейся на arr[i]
    dp = [1] * n
    # parent[i] - индекс предыдущего элемента в LIS
    parent = [-1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Находим максимальную длину и её индекс
    max_len = max(dp)
    max_idx = dp.index(max_len)
    
    # Восстановление подпоследовательности
    lis = []
    idx = max_idx
    while idx != -1:
        lis.append(arr[idx])
        idx = parent[idx]
    lis.reverse()
    
    return max_len, lis


def longest_increasing_subsequence_optimized(arr: List[int]) -> Tuple[int, List[int]]:
    """
    Оптимизированная версия LIS с бинарным поиском.
    
    Временная сложность: O(n * log(n))
    Пространственная сложность: O(n)
    """
    n = len(arr)
    if n == 0:
        return 0, []
    
    # tail[i] - наименьший последний элемент LIS длины i+1
    tail = []
    # parent[i] - индекс предыдущего элемента
    parent = [-1] * n
    # indices[i] - индекс элемента в исходном массиве для tail[i]
    indices = []
    
    def binary_search(x: int) -> int:
        """Бинарный поиск позиции для вставки x"""
        left, right = 0, len(tail) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[tail[mid]] < x:
                left = mid + 1
            else:
                right = mid - 1
        return left
    
    for i in range(n):
        pos = binary_search(arr[i])
        if pos == len(tail):
            tail.append(i)
        else:
            tail[pos] = i
        
        if pos > 0:
            parent[i] = tail[pos - 1]
        indices.append(pos)
    
    # Восстановление подпоследовательности
    max_len = len(tail)
    lis = []
    idx = tail[-1]
    while idx != -1:
        lis.append(arr[idx])
        idx = parent[idx]
    lis.reverse()
    
    return max_len, lis

