"""
Практические задачи на рекурсию:
- Бинарный поиск
- Рекурсивный обход файловой системы (печать дерева)
- Ханойские башни
"""

from __future__ import annotations

import os
from typing import List, Optional, Sequence, Tuple


def binary_search_recursive(arr: Sequence[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
	"""Рекурсивный бинарный поиск. Возвращает индекс или -1, если не найдено.

	Предполагается, что массив `arr` отсортирован по неубыванию.

	Сложность по времени: O(log n)
	Максимальная глубина рекурсии: O(log n)
	"""
	if right is None:
		right = len(arr) - 1
	if left > right:
		return -1
	mid = left + (right - left) // 2
	if arr[mid] == target:
		return mid
	if arr[mid] > target:
		return binary_search_recursive(arr, target, left, mid - 1)
	return binary_search_recursive(arr, target, mid + 1, right)


def walk_filesystem_recursive(path: str, indent: str = "", is_last: bool = True) -> None:
	"""Печатает дерево каталогов и файлов, начиная с `path`.

	Пример вывода:
	root/
	├─ dir1/
	│  └─ file.txt
	└─ dir2/

	Сложность по времени: O(N), где N — количество файлов и директорий
	Максимальная глубина рекурсии: O(H), где H — высота дерева каталогов
	"""
	base_name = os.path.basename(os.path.abspath(path))
	prefix = "└─ " if is_last else "├─ "
	print((indent + prefix) + (base_name + ("/" if os.path.isdir(path) else "")))

	if not os.path.isdir(path):
		return

	entries = []
	try:
		entries = sorted(os.listdir(path))
	except PermissionError:
		print(indent + ("   " if is_last else "│  ") + "[доступ запрещён]")
		return

	for i, name in enumerate(entries):
		child_path = os.path.join(path, name)
		child_is_last = i == len(entries) - 1
		child_indent = indent + ("   " if is_last else "│  ")
		walk_filesystem_recursive(child_path, child_indent, child_is_last)


def max_filesystem_depth(path: str) -> int:
	"""Возвращает максимальную глубину вложенности каталогов, начиная с `path`.

	Определение: путь из корня `path` до самого глубокого листа (директории или файла).

	Сложность по времени: O(N), где N — количество узлов (файлы+директории)
	Максимальная глубина рекурсии: O(H)
	"""
	if not os.path.isdir(path):
		return 1
	max_child_depth = 1
	try:
		entries = os.listdir(path)
	except PermissionError:
		return 1
	for name in entries:
		child_path = os.path.join(path, name)
		max_child_depth = max(max_child_depth, 1 + max_filesystem_depth(child_path))
	return max_child_depth


def hanoi(n: int, source: str, target: str, auxiliary: str, moves: Optional[List[Tuple[str, str]]] = None) -> List[Tuple[str, str]]:
	"""Рекурсивное решение задачи Ханойских башен.

	Возвращает список перемещений вида (откуда, куда).

	Сложность по времени: O(2^n)
	Максимальная глубина рекурсии: O(n)
	"""
	if n <= 0:
		return [] if moves is None else moves
	if moves is None:
		moves = []
	# Переносим n-1 дисков на вспомогательный стержень
	hanoi(n - 1, source, auxiliary, target, moves)
	# Переносим самый большой диск на целевой стержень
	moves.append((source, target))
	# Переносим n-1 дисков со вспомогательного на целевой
	hanoi(n - 1, auxiliary, target, source, moves)
	return moves


__all__ = [
	"binary_search_recursive",
	"walk_filesystem_recursive",
	"max_filesystem_depth",
	"hanoi",
]


