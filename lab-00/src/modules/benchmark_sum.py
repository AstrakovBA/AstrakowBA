from __future__ import annotations  # O(1)

from pathlib import Path  # O(1)
from typing import Iterable, Sequence  # O(1)
import statistics  # O(1)
import io  # O(1)
from contextlib import redirect_stdout  # O(1)

import matplotlib.pyplot as plt  # type: ignore  # O(1)

from .sum_analysis import sum_from_file  # O(1)
from .timing_utils import time_call  # O(1)


def benchmark_sum(files: Iterable[Path], runs: int = 7) -> tuple[list[int], list[float], list[float]]:  # O(total_n * runs)
    # Копим результаты по уникальным размерам, чтобы убрать зигзаги от разных категорий файлов
    size_to_durations: dict[int, list[float]] = {}  # O(1)
    for path in files:  # O(f)
        # Размер оцениваем как количество чисел в файле
        text = path.read_text(encoding="utf-8")  # O(n)
        num_tokens = len(text.replace(",", " ").split())  # O(n)

        for _ in range(max(1, runs)):  # O(runs)
            # Глушим вывод sum_from_file во время замера, чтобы избежать шума от print
            sink = io.StringIO()  # O(1)
            with redirect_stdout(sink):  # O(1)
                _, duration = time_call(sum_from_file, str(path))  # O(n)
            size_to_durations.setdefault(num_tokens, []).append(duration)  # O(1)

    # Формируем усреднённые результаты по возрастанию размера
    sizes_sorted = sorted(size_to_durations.keys())  # O(u log u)
    means: list[float] = []  # O(1)
    stds: list[float] = []  # O(1)
    for sz in sizes_sorted:  # O(u)
        durations = size_to_durations[sz]  # O(1)
        mean_val = statistics.fmean(durations) if durations else 0.0  # O(k)
        std_val = statistics.pstdev(durations) if len(durations) > 1 else 0.0  # O(k)
        means.append(mean_val)  # O(1)
        stds.append(std_val)  # O(1)

    return sizes_sorted, means, stds  # O(1)


def plot_results(sizes: Sequence[int], times: Sequence[float], out_path: Path, stds: Sequence[float] | None = None) -> None:  # O(p)
    plt.figure(figsize=(8, 5))  # O(1)

    # sizes уже отсортированы и агрегированы по уникальным размерам
    sizes_sorted = list(sizes)  # O(p)
    times_sorted = list(times)  # O(p)
    stds_sorted = list(stds) if stds is not None else None  # O(p)

    if stds_sorted is not None:
        plt.errorbar(
            sizes_sorted,
            times_sorted,
            yerr=stds_sorted,
            fmt="-o",
            color="tab:blue",
            ecolor="tab:blue",
            elinewidth=1.0,
            capsize=3,
            markersize=5,
            markerfacecolor="white",
            markeredgewidth=1.2,
            label="Среднее ±σ",
        )  # O(p)
    else:
        plt.plot(
            sizes_sorted,
            times_sorted,
            color="tab:blue",
            linewidth=1.8,
            marker="o",
            markersize=5,
            markerfacecolor="white",
            markeredgewidth=1.2,
            label="Время выполнения",
        )  # O(p)
    plt.xlabel("Размер входных данных (число элементов)")  # O(1)
    plt.ylabel("Время (сек)")  # O(1)
    plt.title("Зависимость времени выполнения суммирования от размера входных данных")  # O(1)
    plt.grid(True, alpha=0.3)  # O(1)
    plt.legend()  # O(1)
    out_path.parent.mkdir(parents=True, exist_ok=True)  # O(1)
    plt.tight_layout()  # O(1)
    plt.savefig(out_path, dpi=150)  # O(1)
    plt.close()  # O(1)

