from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from modules.sum_analysis import sum_from_file
from modules.benchmark_sum import benchmark_sum, plot_results


def print_hardware_info() -> None:
    # Вывод данных о железе
    print("Модель: Infinix InBook Y3 Plus (YL512)")
    print("Процессор: 12th Gen Intel(R) Core(TM) i3-1215U")
    print("Видеочип: Intel(R) UHD Graphics")
    print("ОЗУ: 16 ГБ, тип: LPDDR4")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    results_dir = base_dir.parent / "docs"
    report_path = base_dir.parent / "ОТЧЕТ.md"

    # Печать информации о железе
    print_hardware_info()

    # Используем уже подготовленные файлы данных
    files = sorted(data_dir.glob("numbers_*.txt"))
    if not files:
        print("Нет входных файлов в папке 'src/data'. Ожидаются файлы вида numbers_*.txt")
        return

    # Бенчмарк
    sizes_measured, times_mean, times_std = benchmark_sum(files, runs=9)

    # Построение графика
    plot_path = results_dir / "sum_benchmark.png"
    plot_results(sizes_measured, times_mean, plot_path, stds=times_std)

    # Вывод кратких результатов
    print("Размеры:", sizes_measured)
    print("Время (сек), среднее:", times_mean)
    print("Стандартное отклонение (сек):", times_std)
    print("График сохранен в:", plot_path)

    # Добавляем результаты в отчет
    try:
        report_lines = [
            "\n",
            "## Результаты суммирования и эмпирический анализ\n",
            "- Теоретическая сложность: O(n)\n",
            f"- Размеры данных: {sizes_measured}\n",
            f"- Время (сек), среднее: {times_mean}\n",
            f"- Стандартное отклонение (сек): {times_std}\n",
            "- График: см. ниже\n",
            "\n",
            "![Зависимость времени от размера](docs/sum_benchmark.png)\n",
        ]
        with report_path.open("a", encoding="utf-8") as f:
            f.writelines(report_lines)
    except Exception as exc:
        print("Не удалось записать результаты в отчет:", exc)


if __name__ == "__main__":
    main()