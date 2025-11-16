"""
Модуль с реализацией хеш-таблицы методом цепочек.
"""

from typing import Optional, Callable, List, Tuple
from src.modules.hash_functions import simple_hash, polynomial_hash, djb2_hash


class HashTableChaining:
    """
    Хеш-таблица с методом цепочек (chaining).
    
    Каждый слот таблицы содержит список (цепочку) элементов с одинаковым хешем.
    При коллизии новый элемент добавляется в конец цепочки.
    
    Временная сложность:
    - Вставка: O(1) среднее, O(n) худшее (если все элементы в одной цепочке)
    - Поиск: O(1) среднее, O(n) худшее
    - Удаление: O(1) среднее, O(n) худшее
    
    Args:
        initial_size: Начальный размер таблицы
        load_factor_threshold: Порог коэффициента заполнения для рехеширования
        hash_function: Используемая хеш-функция
    """
    
    HASH_FUNCTIONS = {
        'simple': simple_hash,
        'polynomial': polynomial_hash,
        'djb2': djb2_hash
    }
    
    def __init__(self, initial_size: int = 16, load_factor_threshold: float = 0.75,
                 hash_function: str = 'djb2'):
        if initial_size <= 0:
            raise ValueError("Размер таблицы должен быть положительным")
        if not 0 < load_factor_threshold <= 1:
            raise ValueError("Порог коэффициента заполнения должен быть в диапазоне (0, 1]")
        if hash_function not in self.HASH_FUNCTIONS:
            raise ValueError(f"Неизвестная хеш-функция: {hash_function}")
        
        self.size = initial_size
        self.load_factor_threshold = load_factor_threshold
        self.hash_func = self.HASH_FUNCTIONS[hash_function]
        self.table: List[List[Tuple[str, any]]] = [[] for _ in range(self.size)]
        self.count = 0  # Количество элементов
    
    def _hash(self, key: str) -> int:
        """Вычисляет хеш для ключа."""
        return self.hash_func(key, self.size)
    
    def _load_factor(self) -> float:
        """Вычисляет текущий коэффициент заполнения."""
        return self.count / self.size if self.size > 0 else 0
    
    def _resize(self):
        """Увеличивает размер таблицы и перехеширует все элементы."""
        old_table = self.table
        old_size = self.size
        
        # Увеличиваем размер в 2 раза
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        # Перехешируем все элементы
        for chain in old_table:
            for key, value in chain:
                self.insert(key, value)
    
    def insert(self, key: str, value: any) -> None:
        """
        Вставляет или обновляет элемент в таблице.
        
        Args:
            key: Ключ
            value: Значение
        """
        index = self._hash(key)
        chain = self.table[index]
        
        # Проверяем, существует ли уже такой ключ
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)  # Обновляем значение
                return
        
        # Добавляем новый элемент
        chain.append((key, value))
        self.count += 1
        
        # Проверяем необходимость рехеширования
        if self._load_factor() > self.load_factor_threshold:
            self._resize()
    
    def get(self, key: str) -> Optional[any]:
        """
        Получает значение по ключу.
        
        Args:
            key: Ключ
            
        Returns:
            Значение или None, если ключ не найден
        """
        index = self._hash(key)
        chain = self.table[index]
        
        for k, v in chain:
            if k == key:
                return v
        
        return None
    
    def delete(self, key: str) -> bool:
        """
        Удаляет элемент по ключу.
        
        Args:
            key: Ключ
            
        Returns:
            True, если элемент был удален, False если не найден
        """
        index = self._hash(key)
        chain = self.table[index]
        
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self.count -= 1
                return True
        
        return False
    
    def contains(self, key: str) -> bool:
        """
        Проверяет наличие ключа в таблице.
        
        Args:
            key: Ключ
            
        Returns:
            True, если ключ существует, False иначе
        """
        return self.get(key) is not None
    
    def get_statistics(self) -> dict:
        """
        Возвращает статистику о таблице.
        
        Returns:
            Словарь со статистикой:
            - size: размер таблицы
            - count: количество элементов
            - load_factor: коэффициент заполнения
            - max_chain_length: максимальная длина цепочки
            - avg_chain_length: средняя длина цепочки
            - empty_slots: количество пустых слотов
            - collisions: общее количество коллизий
        """
        chain_lengths = [len(chain) for chain in self.table]
        max_chain = max(chain_lengths) if chain_lengths else 0
        avg_chain = sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0
        empty_slots = sum(1 for chain in self.table if len(chain) == 0)
        
        # Коллизии = элементы в цепочках длиной > 1
        collisions = sum(max(0, len(chain) - 1) for chain in self.table)
        
        return {
            'size': self.size,
            'count': self.count,
            'load_factor': self._load_factor(),
            'max_chain_length': max_chain,
            'avg_chain_length': avg_chain,
            'empty_slots': empty_slots,
            'collisions': collisions
        }


