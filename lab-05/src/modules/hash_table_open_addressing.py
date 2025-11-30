"""
Модуль с реализацией хеш-таблицы с открытой адресацией.
Поддерживает линейное пробирование и двойное хеширование.
"""

from typing import Optional, Tuple, List
from src.modules.hash_functions import simple_hash, polynomial_hash, djb2_hash


class HashTableOpenAddressing:
    """
    Хеш-таблица с открытой адресацией.
    
    Поддерживает два метода разрешения коллизий:
    - Линейное пробирование: h(k, i) = (h1(k) + i) mod m
    - Двойное хеширование: h(k, i) = (h1(k) + i * h2(k)) mod m
    
    Временная сложность:
    - Вставка: O(1) среднее, O(n) худшее (при высокой заполненности)
    - Поиск: O(1) среднее, O(n) худшее
    - Удаление: O(1) среднее, O(n) худшее
    
    Args:
        initial_size: Начальный размер таблицы
        load_factor_threshold: Порог коэффициента заполнения для рехеширования
        hash_function: Используемая хеш-функция
        probing_method: Метод пробирования ('linear' или 'double')
    """
    
    HASH_FUNCTIONS = {
        'simple': simple_hash,
        'polynomial': polynomial_hash,
        'djb2': djb2_hash
    }
    
    # Специальные значения для слотов
    EMPTY = None
    DELETED = object()  # Маркер удаленного элемента
    
    def __init__(self, initial_size: int = 16, load_factor_threshold: float = 0.75,
                 hash_function: str = 'djb2', probing_method: str = 'linear'):
        if initial_size <= 0:
            raise ValueError("Размер таблицы должен быть положительным")
        if not 0 < load_factor_threshold <= 1:
            raise ValueError("Порог коэффициента заполнения должен быть в диапазоне (0, 1]")
        if hash_function not in self.HASH_FUNCTIONS:
            raise ValueError(f"Неизвестная хеш-функция: {hash_function}")
        if probing_method not in ['linear', 'double']:
            raise ValueError("Метод пробирования должен быть 'linear' или 'double'")
        
        self.size = initial_size
        self.load_factor_threshold = load_factor_threshold
        self.hash_func = self.HASH_FUNCTIONS[hash_function]
        self.probing_method = probing_method
        self.table: List[Optional[Tuple[str, any]]] = [self.EMPTY] * self.size
        self.count = 0  # Количество элементов (без учета DELETED)
        self.deleted_count = 0  # Количество удаленных элементов
    
    def _hash1(self, key: str) -> int:
        """Первичная хеш-функция."""
        return self.hash_func(key, self.size)
    
    def _hash2(self, key: str) -> int:
        """Вторичная хеш-функция для двойного хеширования."""
        # Используем другую хеш-функцию или модифицированную версию
        # Важно: h2(k) не должно быть 0 и должно быть взаимно простым с размером
        hash_value = 0
        for char in key:
            hash_value = hash_value * 31 + ord(char)
        # Делаем нечетным и взаимно простым с размером
        hash_value = abs(hash_value) % (self.size - 1)
        return hash_value + 1  # Гарантируем, что не 0
    
    def _probe(self, key: str, attempt: int) -> int:
        """
        Вычисляет индекс для пробирования.
        
        Args:
            key: Ключ
            attempt: Номер попытки (начинается с 0)
            
        Returns:
            Индекс в таблице
        """
        h1 = self._hash1(key)
        
        if self.probing_method == 'linear':
            return (h1 + attempt) % self.size
        else:  # double hashing
            h2 = self._hash2(key)
            return (h1 + attempt * h2) % self.size
    
    def _load_factor(self) -> float:
        """Вычисляет текущий коэффициент заполнения."""
        return (self.count + self.deleted_count) / self.size if self.size > 0 else 0
    
    def _resize(self):
        """Увеличивает размер таблицы и перехеширует все элементы."""
        old_table = self.table
        old_size = self.size
        
        # Увеличиваем размер в 2 раза
        self.size *= 2
        self.table = [self.EMPTY] * self.size
        old_count = self.count
        self.count = 0
        self.deleted_count = 0
        
        # Перехешируем все элементы (игнорируем DELETED)
        for slot in old_table:
            if slot is not self.EMPTY and slot is not self.DELETED:
                key, value = slot
                self.insert(key, value)
    
    def insert(self, key: str, value: any) -> None:
        """
        Вставляет или обновляет элемент в таблице.
        
        Args:
            key: Ключ
            value: Значение
        """
        # Проверяем необходимость рехеширования перед вставкой
        if self._load_factor() > self.load_factor_threshold:
            self._resize()
        
        attempt = 0
        first_deleted_index = None
        
        while attempt < self.size:
            index = self._probe(key, attempt)
            slot = self.table[index]
            
            if slot is self.EMPTY:
                # Нашли пустой слот
                if first_deleted_index is not None:
                    # Используем ранее найденный удаленный слот
                    self.table[first_deleted_index] = (key, value)
                    self.count += 1
                    self.deleted_count -= 1
                else:
                    self.table[index] = (key, value)
                    self.count += 1
                return
            elif slot is self.DELETED:
                # Запоминаем первый удаленный слот
                if first_deleted_index is None:
                    first_deleted_index = index
            else:
                # Слот занят
                k, v = slot
                if k == key:
                    # Обновляем существующий элемент
                    self.table[index] = (key, value)
                    return
            
            attempt += 1
        
        # Если дошли сюда, таблица переполнена (не должно произойти после рехеширования)
        raise RuntimeError("Хеш-таблица переполнена")
    
    def get(self, key: str) -> Optional[any]:
        """
        Получает значение по ключу.
        
        Args:
            key: Ключ
            
        Returns:
            Значение или None, если ключ не найден
        """
        attempt = 0
        
        while attempt < self.size:
            index = self._probe(key, attempt)
            slot = self.table[index]
            
            if slot is self.EMPTY:
                # Дошли до пустого слота, ключ не найден
                return None
            elif slot is not self.DELETED:
                k, v = slot
                if k == key:
                    return v
            
            attempt += 1
        
        return None
    
    def delete(self, key: str) -> bool:
        """
        Удаляет элемент по ключу (помечает слот как DELETED).
        
        Args:
            key: Ключ
            
        Returns:
            True, если элемент был удален, False если не найден
        """
        attempt = 0
        
        while attempt < self.size:
            index = self._probe(key, attempt)
            slot = self.table[index]
            
            if slot is self.EMPTY:
                # Дошли до пустого слота, ключ не найден
                return False
            elif slot is not self.DELETED:
                k, v = slot
                if k == key:
                    # Помечаем как удаленный
                    self.table[index] = self.DELETED
                    self.count -= 1
                    self.deleted_count += 1
                    return True
            
            attempt += 1
        
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
            - deleted_count: количество удаленных элементов
            - load_factor: коэффициент заполнения
            - empty_slots: количество пустых слотов
            - collisions: оценка количества коллизий (попытки > 0)
            - max_probe_distance: максимальное расстояние пробирования
            - avg_probe_distance: среднее расстояние пробирования
        """
        empty_slots = sum(1 for slot in self.table if slot is self.EMPTY)
        
        # Подсчитываем коллизии и расстояние пробирования
        collisions = 0
        probe_distances = []
        
        for i, slot in enumerate(self.table):
            if slot is not self.EMPTY and slot is not self.DELETED:
                key, _ = slot
                primary_index = self._hash1(key)
                
                # Вычисляем расстояние пробирования (количество попыток)
                if self.probing_method == 'linear':
                    # Для линейного пробирования расстояние = разница индексов
                    distance = (i - primary_index) % self.size
                else:  # double hashing
                    # Для двойного хеширования вычисляем количество попыток
                    # h(k, i) = (h1(k) + i * h2(k)) mod m
                    # i = ((index - h1(k)) mod m) / h2(k)
                    h2 = self._hash2(key)
                    if h2 == 0:
                        distance = 0
                    else:
                        # Вычисляем количество попыток, необходимое для достижения этого индекса
                        diff = (i - primary_index) % self.size
                        if diff == 0:
                            distance = 0
                        else:
                            # Приблизительное количество попыток
                            distance = diff // h2 if h2 > 0 else 0
                            # Если не делится нацело, округляем вверх
                            if diff % h2 != 0:
                                distance += 1
                
                probe_distances.append(distance)
                
                if i != primary_index:
                    collisions += 1
        
        max_probe = max(probe_distances) if probe_distances else 0
        avg_probe = sum(probe_distances) / len(probe_distances) if probe_distances else 0
        
        return {
            'size': self.size,
            'count': self.count,
            'deleted_count': self.deleted_count,
            'load_factor': self._load_factor(),
            'empty_slots': empty_slots,
            'collisions': collisions,
            'max_probe_distance': max_probe,
            'avg_probe_distance': avg_probe
        }

