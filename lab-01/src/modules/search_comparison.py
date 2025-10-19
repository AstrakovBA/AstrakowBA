from __future__ import annotations

from time import perf_counter  # O(1)
from pathlib import Path  # O(1)
from typing import Callable, List, Tuple, Dict  # O(1)


def linear_search(arr: List[int], target: int) -> int:  # O(1)
    """Вернуть индекс целевого элемента в массиве или -1, если не найден."""  # O(1)
    for index, value in enumerate(arr):  # O(n) за n итераций; одна итерация O(1)
        if value == target:  # O(1)
            return index  # O(1)
    return -1  # O(1)
    # Итоговая сложность: O(n) по времени, O(1) по дополнительной памяти


def binary_search(arr: List[int], target: int) -> int:  # O(1)
    """Вернуть индекс целевого элемента в отсортированном массиве или -1, если не найден."""  # O(1)
    left = 0  # O(1)
    right = len(arr) - 1  # O(1)
    while left <= right:  # O(log n) итераций; тело цикла O(1)
        mid = (left + right) // 2  # O(1)
        mid_value = arr[mid]  # O(1)
        if mid_value == target:  # O(1)
            return mid  # O(1)
        if mid_value < target:  # O(1)
            left = mid + 1  # O(1)
        else:  # O(1)
            right = mid - 1  # O(1)
    return -1  # O(1)
    # Итоговая сложность: O(log n) по времени, O(1) по дополнительной памяти


def load_sorted_arrays_from_dir(data_dir: Path) -> Dict[int, List[int]]:  # O(k + total_n)
    """Загрузить отсортированные массивы целых из текстовых файлов; вернуть {размер: массив}.

    Поддерживаются форматы:
    - по одному числу на строку (напр., "42")
    - несколько чисел через пробелы в одной строке (напр., "1 2 3")
    - числа с суффиксом .0 (напр., "-10.0"), конвертируются в int
    """  # O(1)
    arrays_by_size: Dict[int, List[int]] = {}  # O(1)
    for file_path in sorted(data_dir.glob("numbers_*_*.txt")):  # O(k log k) на сортировку; обход O(k)
        numbers: List[int] = []  # O(1)
        with file_path.open("r", encoding="utf-8") as f:  # O(1)
            for line in f:  # O(m) строк
                stripped = line.strip()  # O(1)
                if not stripped:  # O(1)
                    continue  # O(1)
                for token in stripped.split():  # O(t) токенов в строке
                    try:  # O(1)
                        numbers.append(int(token))  # O(1)
                    except ValueError:  # O(1)
                        try:  # O(1)
                            numbers.append(int(float(token)))  # O(1)
                        except ValueError:  # O(1)
                            # Пропускаем нечисловые токены
                            continue  # O(1)
        size = len(numbers)  # O(1)
        numbers.sort()  # O(m log m) (гарантируем сортировку для бинарного поиска)
        arrays_by_size[size] = numbers  # O(1)
    return arrays_by_size  # O(1)


def pick_targets(arr: List[int]) -> Tuple[int, int, int, int]:  # O(1)
    """Выбрать первый, средний, последний и отсутствующий элементы как цели поиска."""  # O(1)
    first = arr[0]  # O(1)
    middle = arr[len(arr) // 2]  # O(1)
    last = arr[-1]  # O(1)
    absent = last + 1  # O(1)
    return first, middle, last, absent  # O(1)


def time_function(
    func: Callable[[List[int], int], int],
    arr: List[int],
    target: int,
    repeats: int = 5,
    min_duration: float = 0.01,
    max_loops: int = 1_000_000,
) -> float:  # O(repeats * loops)
    """Вернуть среднее время одного вызова (сек.) с адаптивным числом повторов внутри измерения.

    Алгоритм подбирает число вызовов в одном замере так, чтобы длительность была не менее
    min_duration, и усредняет время на один вызов. Это снижает погрешность для очень быстрых функций.
    """  # O(1)

    # Небольшой прогрев для стабильности
    for _ in range(10):  # O(1)
        _ = func(arr, target)  # O(T(n))

    # Экспоненциальный подбор количества вызовов
    loops = 1  # O(1)
    while loops <= max_loops:  # O(log max_loops)
        start = perf_counter()  # O(1)
        for _ in range(loops):  # O(loops)
            _ = func(arr, target)  # O(T(n))
        elapsed = perf_counter() - start  # O(1)
        if elapsed >= min_duration:  # O(1)
            break  # O(1)
        loops *= 2  # O(1)

    # Основные повторы с выбранным числом вызовов
    total = 0.0  # O(1)
    for _ in range(repeats):  # O(repeats)
        start = perf_counter()  # O(1)
        for _ in range(loops):  # O(loops)
            _ = func(arr, target)  # O(T(n))
        total += perf_counter() - start  # O(1)

    avg_per_call = (total / repeats) / max(1, loops)  # O(1)
    return avg_per_call  # O(1)


def benchmark_algorithms(
    arrays_by_size: Dict[int, List[int]],
    repeats: int = 9,
    min_duration: float = 0.01,
) -> Dict[str, List[Tuple[int, float]]]:  # O(S * R * (n + log n))
    """
    Для каждого размера массива измерить среднее время для линейного и бинарного
    поиска по четырём целям (первый, средний, последний, отсутствующий). Вернуть
    структуру вида:
    {
      "linear": [(size, avg_seconds), ...],
      "binary": [(size, avg_seconds), ...]
    }
    """  # O(1)
    linear_results: List[Tuple[int, float]] = []  # O(1)
    binary_results: List[Tuple[int, float]] = []  # O(1)
    for size in sorted(arrays_by_size.keys()):  # O(S log S)
        arr = arrays_by_size[size]  # O(1)
        t_first, t_middle, t_last, t_absent = pick_targets(arr)  # O(1)
        targets = (t_first, t_middle, t_last, t_absent)  # O(1)

        # Замер линейного поиска
        lin_times = [
            time_function(linear_search, arr, t, repeats=repeats, min_duration=min_duration)
            for t in targets
        ]  # O(4 * repeats * n)
        linear_results.append((size, sum(lin_times) / len(lin_times)))  # O(1)

        # Замер бинарного поиска
        bin_times = [
            time_function(binary_search, arr, t, repeats=repeats, min_duration=min_duration)
            for t in targets
        ]  # O(4 * repeats * log n)
        binary_results.append((size, sum(bin_times) / len(bin_times)))  # O(1)

    return {"linear": linear_results, "binary": binary_results}  # O(1)


