from __future__ import annotations  # O(1)

import sys  # O(1)
from pathlib import Path  # O(1)


def sum_from_file(file_path: str) -> float:  # O(1)
    """Читает числа из файла, кратко выводит содержимое и возвращает их сумму."""  # O(1)
    path: Path = Path(file_path)  # O(1)

    print(f"Чтение чисел из файла: {path}")  # O(1)
    if not path.exists():  # O(1)
        raise FileNotFoundError(f"Файл не найден: {path}")  # O(1)

    with path.open("r", encoding="utf-8") as f:  # O(1)
        content: str = f.read()  # O(n), где n — длина файла

    preview_len: int = 100  # O(1)
    preview: str = content[:preview_len]  # O(1), так как длина среза — константа
    print("Краткое содержимое (первые 100 символов):", preview)  # O(1)

    # Нормализуем разделители, чтобы корректно парсить числа как по пробелам, так и по запятым.
    normalized: str = content.replace(",", " ")  # O(n)
    tokens: list[str] = normalized.split()  # O(n)

    numbers: list[float] = []  # O(1)
    for token in tokens:  # O(m), где m — число токенов (m <= n)
        try:  # O(1)
            number: float = float(token)  # O(1)
            numbers.append(number)  # O(1) амортизированно
        except ValueError:  # O(1)
            # Пропускаем неточные токены (текст, пустые значения и т.п.)
            pass  # O(1)

    total: float = sum(numbers)  # O(m)
    print(f"Сумма чисел: {total}")  # O(1)
    return total  # O(1)

    # Общая асимптотическая сложность функции: O(n),
    # где n — размер входного файла (байт/символов),
    # так как операции чтения, нормализации и разбиения — линейные,
    # а суммирование пропорционально количеству корректно распознанных чисел (m <= n).


if __name__ == "__main__":  # O(1)
    if len(sys.argv) < 2:  # O(1)
        print("Использование: python -m src.modules.sum_analysis <путь_к_файлу>")  # O(1)
        sys.exit(1)  # O(1)

    input_path: str = sys.argv[1]  # O(1)
    try:  # O(1)
        sum_from_file(input_path)  # O(n)
    except Exception as exc:  # O(1)
        print(f"Ошибка: {exc}")  # O(1)
        sys.exit(2)  # O(1)

