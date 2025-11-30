"""
Модуль с реализацией различных хеш-функций для строковых ключей.
"""


def simple_hash(key: str, table_size: int) -> int:
    """
    Простая хеш-функция: сумма кодов символов.
    
    Особенности:
    - Быстрая в вычислении
    - Плохое распределение для похожих строк (анаграммы дают одинаковый хеш)
    - Подвержена коллизиям для строк с одинаковыми символами
    
    Временная сложность: O(n), где n - длина строки
    
    Args:
        key: Строковый ключ
        table_size: Размер хеш-таблицы
        
    Returns:
        Хеш-значение в диапазоне [0, table_size-1]
    """
    hash_value = 0
    for char in key:
        hash_value += ord(char)
    return hash_value % table_size


def polynomial_hash(key: str, table_size: int, base: int = 31) -> int:
    """
    Полиномиальная хеш-функция (rolling hash).
    
    Особенности:
    - Хорошее распределение для строк
    - Учитывает порядок символов
    - Меньше коллизий по сравнению с простой суммой
    - Используется в алгоритме Рабина-Карпа
    
    Временная сложность: O(n), где n - длина строки
    
    Args:
        key: Строковый ключ
        table_size: Размер хеш-таблицы
        base: Основание полинома (по умолчанию 31)
        
    Returns:
        Хеш-значение в диапазоне [0, table_size-1]
    """
    hash_value = 0
    for char in key:
        hash_value = (hash_value * base + ord(char)) % table_size
    return hash_value


def djb2_hash(key: str, table_size: int) -> int:
    """
    Хеш-функция DJB2 (Daniel J. Bernstein).
    
    Особенности:
    - Очень хорошее распределение
    - Широко используется в реальных приложениях
    - Магическое число 33 было выбрано эмпирически
    - Хорошо работает с различными типами данных
    
    Временная сложность: O(n), где n - длина строки
    
    Args:
        key: Строковый ключ
        table_size: Размер хеш-таблицы
        
    Returns:
        Хеш-значение в диапазоне [0, table_size-1]
    """
    hash_value = 5381  # Начальное значение (магическое число)
    for char in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # hash * 33 + char
    return abs(hash_value) % table_size


