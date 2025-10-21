from __future__ import annotations  # O(1)

import time  # O(1)
import functools  # O(1)
from typing import Callable, TypeVar, Any, ParamSpec  # O(1)


P = ParamSpec("P")  # O(1)
R = TypeVar("R")  # O(1)


def measure_time(func: Callable[P, R]) -> Callable[P, tuple[R, float]]:  # O(1)
    """Декоратор: измеряет время выполнения функции и возвращает (результат, секунды)."""  # O(1)

    @functools.wraps(func)  # O(1)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[R, float]:  # O(1)
        start: float = time.perf_counter()  # O(1)
        result: R = func(*args, **kwargs)  # O(1) + тело func
        duration: float = time.perf_counter() - start  # O(1)
        return result, duration  # O(1)

    return wrapper  # O(1)


def time_call(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> tuple[R, float]:  # O(1)
    """Функция-обёртка: однократный замер времени вызова func."""  # O(1)
    start: float = time.perf_counter()  # O(1)
    result: R = func(*args, **kwargs)  # O(1) + тело func
    duration: float = time.perf_counter() - start  # O(1)
    return result, duration  # O(1)


