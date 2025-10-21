from __future__ import annotations

from pathlib import Path  # O(1)
from typing import Dict, List, Tuple  # O(1)

import matplotlib.pyplot as plt  # O(1)

from modules.search_comparison import (  # O(1)
    load_sorted_arrays_from_dir,
    benchmark_algorithms,
)


def ensure_data_dir() -> Path:  # O(1)
    base = Path(__file__).resolve().parent  # O(1)
    return base / "data"  # O(1)


def ensure_docs_dir() -> Path:  # O(1)
    root = Path(__file__).resolve().parent.parent  # O(1)
    out = root / "docs"  # O(1)
    out.mkdir(parents=True, exist_ok=True)  # O(1)
    return out  # O(1)


def plot_results(results: Dict[str, List[Tuple[int, float]]], output_dir: Path) -> None:  # O(S)
    sizes = [s for s, _ in results["linear"]]  # O(S)
    linear_times = [t for _, t in results["linear"]]  # O(S)
    binary_times = [t for _, t in results["binary"]]  # O(S)
    # Перевод в микросекунды для наглядности малых значений
    linear_us = [t * 1e6 for t in linear_times]  # O(S)
    binary_us = [t * 1e6 for t in binary_times]  # O(S)

    # Линейная шкала (обычная)
    plt.figure(figsize=(8, 5))  # O(1)
    plt.plot(sizes, linear_us, marker="o", label="Линейный поиск (O(n))")  # O(S)
    plt.plot(sizes, binary_us, marker="s", label="Бинарный поиск (O(log n))")  # O(S)
    plt.xlabel("Размер массива")  # O(1)
    plt.ylabel("Среднее время на один поиск (мкс)")  # O(1)
    plt.title("Поисковые алгоритмы: время vs размер массива")  # O(1)
    plt.legend()  # O(1)
    plt.grid(True, which="both", linestyle=":", linewidth=0.8)  # O(1)
    plt.tight_layout()  # O(1)
    plt.savefig(output_dir / "search_times_linear.png", dpi=200)  # O(1)

    # Логарифмическая шкала по оси Y
    plt.figure(figsize=(8, 5))  # O(1)
    plt.plot(sizes, linear_us, marker="o", label="Линейный поиск (O(n))")  # O(S)
    plt.plot(sizes, binary_us, marker="s", label="Бинарный поиск (O(log n))")  # O(S)
    plt.xlabel("Размер массива")  # O(1)
    plt.ylabel("Среднее время на один поиск (мкс)")  # O(1)
    plt.title("Поисковые алгоритмы: время vs размер (логарифмическая шкала по Y)")  # O(1)
    plt.yscale("log")  # O(1)
    plt.legend()  # O(1)
    plt.grid(True, which="both", linestyle=":", linewidth=0.8)  # O(1)
    plt.tight_layout()  # O(1)
    plt.savefig(output_dir / "search_times_logy.png", dpi=200)  # O(1)

    # Дополнительный график: log-log, подчёркивает наклоны для O(n) и O(log n)
    plt.figure(figsize=(8, 5))  # O(1)
    plt.plot(sizes, linear_us, marker="o", label="Линейный поиск (O(n))")  # O(S)
    plt.plot(sizes, binary_us, marker="s", label="Бинарный поиск (O(log n))")  # O(S)
    plt.xlabel("Размер массива")  # O(1)
    plt.ylabel("Среднее время на один поиск (мкс) [лог]")  # O(1)
    plt.title("Поисковые алгоритмы: время vs размер (log-log)")  # O(1)
    plt.xscale("log")  # O(1)
    plt.yscale("log")  # O(1)
    plt.legend()  # O(1)
    plt.grid(True, which="both", linestyle=":", linewidth=0.8)  # O(1)
    plt.tight_layout()  # O(1)
    plt.savefig(output_dir / "search_times_loglog.png", dpi=200)  # O(1)

    plt.show()  # O(1)


def main() -> None:  # O(1)
    print("Модель: Infinix InBook Y3 Plus (YL512)")
    print("Процессор: 12th Gen Intel(R) Core(TM) i3-1215U")
    print("Видеочип: Intel(R) UHD Graphics")
    print("ОЗУ: 16 ГБ, тип: LPDDR4")
    data_dir = ensure_data_dir()  # O(1)
    arrays_by_size = load_sorted_arrays_from_dir(data_dir)  # O(k + total_n)
    results = benchmark_algorithms(arrays_by_size, repeats=11)  # O(S * R * (n + log n))
    output_dir = ensure_docs_dir()  # O(1)
    plot_results(results, output_dir)  # O(S)


if __name__ == "__main__":  # O(1)
    main()  # O(1)


