"""
Модуль для генерации тестовых данных различных типов.

Генерирует массивы целых чисел разных размеров и типов упорядоченности:
- random: случайные числа
- sorted: уже отсортированные
- reversed: отсортированные в обратном порядке
- almost_sorted: почти отсортированные (95% упорядочено, 5% перемешано)
"""

import random
import os
from pathlib import Path


def generate_random_data(size, min_val=0, max_val=10000):
    """
    Генерирует массив случайных целых чисел.
    
    Args:
        size: размер массива
        min_val: минимальное значение (по умолчанию 0)
        max_val: максимальное значение (по умолчанию 10000)
    
    Returns:
        list: массив случайных целых чисел
    """
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_data(size, min_val=0, max_val=10000):
    """
    Генерирует уже отсортированный массив.
    
    Args:
        size: размер массива
        min_val: минимальное значение
        max_val: максимальное значение
    
    Returns:
        list: отсортированный массив
    """
    arr = generate_random_data(size, min_val, max_val)
    arr.sort()
    return arr


def generate_reversed_data(size, min_val=0, max_val=10000):
    """
    Генерирует массив, отсортированный в обратном порядке.
    
    Args:
        size: размер массива
        min_val: минимальное значение
        max_val: максимальное значение
    
    Returns:
        list: массив, отсортированный по убыванию
    """
    arr = generate_sorted_data(size, min_val, max_val)
    arr.reverse()
    return arr


def generate_almost_sorted_data(size, disorder_percent=5, min_val=0, max_val=10000):
    """
    Генерирует почти отсортированный массив.
    
    Args:
        size: размер массива
        disorder_percent: процент беспорядка (по умолчанию 5%)
        min_val: минимальное значение
        max_val: максимальное значение
    
    Returns:
        list: почти отсортированный массив
    """
    arr = generate_sorted_data(size, min_val, max_val)
    
    # Вычисляем количество элементов для перемешивания
    num_swaps = int(size * disorder_percent / 100)
    
    # Выполняем случайные обмены
    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    
    return arr


def save_data_to_file(data, filepath):
    """
    Сохраняет массив в текстовый файл (одно число на строку).
    
    Args:
        data: список чисел для сохранения
        filepath: путь к файлу для сохранения
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        for num in data:
            f.write(f"{num}\n")


def load_data_from_file(filepath):
    """
    Загружает массив из текстового файла.
    
    Args:
        filepath: путь к файлу
    
    Returns:
        list: загруженный массив целых чисел
    """
    with open(filepath, 'r') as f:
        return [int(line.strip()) for line in f.readlines()]


def generate_all_datasets(sizes=[100, 1000, 5000, 10000], data_dir="src/data"):
    """
    Генерирует все наборы тестовых данных всех типов и размеров.
    
    Args:
        sizes: список размеров массивов для генерации
        data_dir: директория для сохранения файлов
    """
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    
    data_types = {
        'random': generate_random_data,
        'sorted': generate_sorted_data,
        'reversed': generate_reversed_data,
        'almost_sorted': generate_almost_sorted_data
    }
    
    print("Генерация тестовых данных...")
    
    for size in sizes:
        print(f"  Размер: {size}")
        for data_type, generator_func in data_types.items():
            print(f"    Тип: {data_type}")
            data = generator_func(size)
            filename = f"{data_type}_{size}.txt"
            filepath = data_path / filename
            save_data_to_file(data, str(filepath))
            print(f"      Сохранено: {filepath}")
    
    print("Генерация завершена!")


if __name__ == "__main__":
    # Генерируем данные при запуске модуля напрямую
    generate_all_datasets()


