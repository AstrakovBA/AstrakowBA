from __future__ import annotations

import os
import time
from typing import List

import matplotlib.pyplot as plt

from modules.recursion import factorial, fibonacci, fast_pow
from modules.memoization import compare_naive_vs_memo, fibonacci_memo
from modules.recursion_tasks import (
	binary_search_recursive,
	walk_filesystem_recursive,
	max_filesystem_depth,
	hanoi,
)


def ensure_docs_dir() -> str:
	"""Гарантирует наличие директории docs и возвращает путь."""
	root = os.path.dirname(os.path.dirname(__file__))
	docs_path = os.path.join(root, "docs")
	os.makedirs(docs_path, exist_ok=True)
	return docs_path


def plot_fib_timing(ns: List[int], times_naive: List[float], times_memo: List[float], save_path: str) -> None:
	"""Строит и сохраняет график времени вычисления Фибоначчи."""
	plt.figure(figsize=(8, 5))
	plt.plot(ns, times_naive, marker="o", label="Наивная рекурсия")
	plt.plot(ns, times_memo, marker="o", label="Мемоизация")
	plt.xlabel("n")
	plt.ylabel("Время, с")
	plt.title("Сравнение времени вычисления Фибоначчи")
	# Логарифмические шкалы по обеим осям
	plt.xscale("log")
	plt.yscale("log")
	plt.grid(True)
	plt.legend()
	plt.tight_layout()
	plt.savefig(save_path, dpi=150)
	print(f"График сохранён: {save_path}")
	plt.show()


def measure_fibonacci_series(ns: List[int]) -> None:
	"""Замеряет время вычисления Фибоначчи для набора n, строит график."""
	docs = ensure_docs_dir()
	save_path = os.path.join(docs, "fib_timing.png")

	times_naive: List[float] = []
	times_memo: List[float] = []

	for n in ns:
		# Наивная
		start = time.perf_counter()
		_ = fibonacci(n)
		times_naive.append(time.perf_counter() - start)
		# Мемоизированная (очистка кэша внутри compare вызова нам не нужна здесь)
		from modules.memoization import fibonacci_memo as fib_memo
		fib_memo.cache_clear()
		start = time.perf_counter()
		_ = fib_memo(n)
		times_memo.append(time.perf_counter() - start)

	plot_fib_timing(ns, times_naive, times_memo, save_path)


def demo_tasks(base_path: str) -> None:
	"""Демонстрирует практические задачи: бинарный поиск, обход ФС, Ханойские башни."""
	print("\n=== Бинарный поиск ===")
	arr = list(range(0, 51, 5))
	print("Массив:", arr)
	target = 25
	idx = binary_search_recursive(arr, target)
	print(f"Искомое {target}, индекс: {idx}")

	print("\n=== Обход файловой системы ===")
	print("Корень:", base_path)
	walk_filesystem_recursive(base_path, indent="", is_last=True)
	depth = max_filesystem_depth(base_path)
	print(f"Макс. глубина: {depth}")

	print("\n=== Ханойские башни ===")
	moves = hanoi(4, "A", "C", "B")
	for i, (src, dst) in enumerate(moves, start=1):
		print(f"Шаг {i}: {src} -> {dst}")
	print(f"Всего шагов: {len(moves)}")


def main() -> None:
	print()
	print("Модель: Infinix InBook Y3 Plus (YL512)")
	print("Процессор: 12th Gen Intel(R) Core(TM) i3-1215U")
	print("Видеочип: Intel(R) UHD Graphics")
	print("ОЗУ: 16 ГБ, тип: LPDDR4")
	print()
	print("=== Базовые рекурсивные алгоритмы ===")
	print("factorial(5) =", factorial(5))
	print("fibonacci(10) =", fibonacci(10))
	print("fast_pow(2, 10) =", fast_pow(2, 10))

	print("\n=== Сравнение на n=35 (вызовы и время) ===")
	comp = compare_naive_vs_memo(35)
	print("Наивная:", comp["naive"])  # (calls, seconds)
	print("Мемоизация:", comp["memo"])  # (calls, seconds)

	print("\n=== Серия замеров и график ===")
	# Подберите ns в пределах разумного, чтобы не ждать слишком долго
	measure_fibonacci_series([5, 10, 15, 20, 25, 30, 32, 34])

	# Демонстрация практических задач
	root = os.path.dirname(os.path.dirname(__file__))
	demo_tasks(root)


if __name__ == "__main__":
	main()


