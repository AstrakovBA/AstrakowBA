"""
Мемоизация для вычисления чисел Фибоначчи и сравнение производительности.
"""

from __future__ import annotations

import time
from functools import lru_cache
from typing import Callable, Dict, Tuple


# Счётчик рекурсивных вызовов для наивной реализации
naive_calls_counter: int = 0


def fibonacci_naive(n: int) -> int:
	"""Наивная рекурсия Фибоначчи с подсчётом вызовов для эксперимента.

	Сложность по времени: экспоненциальная (~O(phi^n))
	Глубина рекурсии: O(n)
	"""
	global naive_calls_counter
	naive_calls_counter += 1
	if n < 0:
		raise ValueError("n должно быть неотрицательным")
	if n < 2:
		return n
	return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


# Счётчик вызовов для мемоизированной реализации
memo_calls_counter: int = 0


@lru_cache(maxsize=None)
def fibonacci_memo(n: int) -> int:
	"""Мемоизированная рекурсия Фибоначчи (через LRU cache).

	Сложность по времени: O(n)
	Глубина рекурсии: O(n)
	Доп. память под кэш: O(n)
	"""
	global memo_calls_counter
	memo_calls_counter += 1
	if n < 0:
		raise ValueError("n должно быть неотрицательным")
	if n < 2:
		return n
	return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


def compare_naive_vs_memo(n: int = 35) -> Dict[str, Tuple[int, float]]:
	"""Сравнивает количество вызовов и время работы наивной и мемо-версии.

	Возвращает словарь вида:
	{
		"naive": (calls, seconds),
		"memo": (calls, seconds)
	}
	"""
	global naive_calls_counter, memo_calls_counter
	# Наивная версия
	naive_calls_counter = 0
	start = time.perf_counter()
	_ = fibonacci_naive(n)
	naive_time = time.perf_counter() - start

	# Мемоизированная версия (сброс кэша перед запуском)
	fibonacci_memo.cache_clear()
	memo_calls_counter = 0
	start = time.perf_counter()
	_ = fibonacci_memo(n)
	memo_time = time.perf_counter() - start

	return {
		"naive": (naive_calls_counter, naive_time),
		"memo": (memo_calls_counter, memo_time),
	}


__all__ = [
	"fibonacci_naive",
	"fibonacci_memo",
	"compare_naive_vs_memo",
]



