"""
Рекурсивные алгоритмы: факториал, числа Фибоначчи, быстрое возведение в степень.

Комментарии содержат время выполнения и максимальную глубину рекурсии.
"""

from __future__ import annotations

from typing import Optional


def factorial(n: int) -> int:
	"""Вычисляет n! рекурсивно.

	Сложность по времени: O(n)
	Максимальная глубина рекурсии: O(n)
	"""
	if n < 0:
		raise ValueError("n должно быть неотрицательным")
	if n in (0, 1):
		return 1
	return n * factorial(n - 1)


def fibonacci(n: int) -> int:
	"""Наивная рекурсивная функция для n-го числа Фибоначчи.

	Определение: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)

	Сложность по времени: O(phi^n) ~ экспоненциальная
	Максимальная глубина рекурсии: O(n)
	"""
	if n < 0:
		raise ValueError("n должно быть неотрицательным")
	if n < 2:
		return n
	return fibonacci(n - 1) + fibonacci(n - 2)


def fast_pow(base: float, exponent: int) -> float:
	"""Быстрое возведение base в степень exponent с разложением по степеням двойки.

	Используется деление степени на 2 (Exponentiation by Squaring).

	Сложность по времени: O(log n)
	Максимальная глубина рекурсии: O(log n)
	"""
	if exponent < 0:
		# Переводим в положительную степень: a^(-n) = 1 / a^n
		return 1.0 / fast_pow(base, -exponent)
	if exponent == 0:
		return 1.0
	if exponent == 1:
		return float(base)
	if exponent % 2 == 0:
		# (a^2)^(n/2)
		return fast_pow(base * base, exponent // 2)
	# a * a^(n-1)
	return float(base) * fast_pow(base, exponent - 1)


__all__ = ["factorial", "fibonacci", "fast_pow"]



