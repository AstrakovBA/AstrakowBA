"""
Модуль для проведения экспериментов по производительности хеш-таблиц.
"""

import time
import random
import string
from typing import Dict, List, Tuple
from src.modules.hash_table_chaining import HashTableChaining
from src.modules.hash_table_open_addressing import HashTableOpenAddressing


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку заданной длины."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_test_data(num_keys: int) -> List[str]:
    """Генерирует список случайных ключей для тестирования."""
    return [generate_random_string() for _ in range(num_keys)]


def measure_insert_time(table, keys: List[str]) -> float:
    """Измеряет время вставки всех ключей."""
    start_time = time.perf_counter()
    for i, key in enumerate(keys):
        table.insert(key, f"value_{i}")
    end_time = time.perf_counter()
    return end_time - start_time


def measure_search_time(table, keys: List[str]) -> float:
    """Измеряет время поиска всех ключей."""
    start_time = time.perf_counter()
    for key in keys:
        table.get(key)
    end_time = time.perf_counter()
    return end_time - start_time


def measure_delete_time(table, keys: List[str]) -> float:
    """Измеряет время удаления всех ключей."""
    start_time = time.perf_counter()
    for key in keys:
        table.delete(key)
    end_time = time.perf_counter()
    return end_time - start_time


def calculate_table_size_for_load_factor(load_factor: float, num_keys: int, 
                                         is_open_addressing: bool = False,
                                         probing_method: str = 'linear') -> int:
    """
    Вычисляет размер таблицы для достижения заданного коэффициента заполнения.
    
    Args:
        load_factor: Желаемый коэффициент заполнения
        num_keys: Количество ключей для вставки
        is_open_addressing: True для открытой адресации (требует больше места из-за коллизий)
        probing_method: Метод пробирования ('linear' или 'double') - влияет на запас
        
    Returns:
        Размер таблицы
    """
    base_size = int(num_keys / load_factor) + 1
    
    # Для открытой адресации добавляем запас, так как из-за коллизий
    # может потребоваться больше места для пробирования
    if is_open_addressing:
        # Линейное пробирование более склонно к кластеризации,
        # поэтому требует больше запаса, особенно при высоких коэффициентах заполнения
        if probing_method == 'linear':
            if load_factor >= 0.9:
                # При коэффициенте 0.9 и линейном пробировании кластеризация очень сильная
                # Нужен большой запас (минимум 2x, но лучше больше)
                base_size = int(base_size * 2.0)  # 100% запас для очень высоких коэффициентов
            elif load_factor >= 0.7:
                base_size = int(base_size * 1.5)  # 50% запас для высоких коэффициентов
            else:
                base_size = int(base_size * 1.2)  # 20% запас для остальных
        else:  # double hashing
            # Двойное хеширование лучше распределяет элементы
            if load_factor >= 0.9:
                base_size = int(base_size * 1.5)  # 50% запас для очень высоких коэффициентов
            elif load_factor >= 0.7:
                base_size = int(base_size * 1.3)  # 30% запас для высоких коэффициентов
            else:
                base_size = int(base_size * 1.1)  # 10% запас для остальных
    
    return base_size


def experiment_chaining(
    load_factors: List[float],
    num_keys: int,
    hash_function: str = 'djb2',
    num_runs: int = 5
) -> Dict[str, List[float]]:
    """
    Проводит эксперимент для хеш-таблицы с методом цепочек.
    
    Для корректного сравнения используем фиксированный размер таблицы
    и варьируем количество элементов для достижения нужного коэффициента заполнения.
    
    Args:
        load_factors: Список коэффициентов заполнения для тестирования
        num_keys: Базовое количество ключей (используется для расчета размера таблицы)
        hash_function: Используемая хеш-функция
        num_runs: Количество запусков для усреднения
        
    Returns:
        Словарь с результатами: insert_times, search_times, delete_times, collisions
    """
    results = {
        'load_factors': load_factors,
        'insert_times': [],
        'search_times': [],
        'delete_times': [],
        'collisions': [],
        'avg_chain_lengths': []
    }
    
    # Используем фиксированный размер таблицы для всех коэффициентов заполнения
    # Базовый размер рассчитываем для максимального коэффициента заполнения
    base_table_size = calculate_table_size_for_load_factor(max(load_factors), num_keys)
    
    for lf in load_factors:
        # Вычисляем количество элементов для достижения нужного коэффициента заполнения
        # при фиксированном размере таблицы
        actual_num_keys = int(base_table_size * lf)
        
        insert_times = []
        search_times = []
        delete_times = []
        collisions_list = []
        avg_chain_lengths = []
        
        for run in range(num_runs):
            table = HashTableChaining(
                initial_size=base_table_size,
                load_factor_threshold=1.0,  # Отключаем автоматическое рехеширование
                hash_function=hash_function
            )
            
            keys = generate_test_data(actual_num_keys)
            
            # Измеряем вставку
            insert_time = measure_insert_time(table, keys)
            insert_times.append(insert_time)
            
            # Получаем статистику после вставки
            stats = table.get_statistics()
            collisions_list.append(stats['collisions'])
            avg_chain_lengths.append(stats['avg_chain_length'])
            
            # Перемешиваем ключи для более реалистичного поиска
            random.shuffle(keys)
            
            # Измеряем поиск
            search_time = measure_search_time(table, keys)
            search_times.append(search_time)
            
            # Измеряем удаление
            delete_time = measure_delete_time(table, keys)
            delete_times.append(delete_time)
        
        # Усредняем результаты
        results['insert_times'].append(sum(insert_times) / num_runs)
        results['search_times'].append(sum(search_times) / num_runs)
        results['delete_times'].append(sum(delete_times) / num_runs)
        results['collisions'].append(sum(collisions_list) / num_runs)
        results['avg_chain_lengths'].append(sum(avg_chain_lengths) / num_runs)
    
    return results


def experiment_open_addressing(
    load_factors: List[float],
    num_keys: int,
    probing_method: str = 'linear',
    hash_function: str = 'djb2',
    num_runs: int = 5
) -> Dict[str, List[float]]:
    """
    Проводит эксперимент для хеш-таблицы с открытой адресацией.
    
    Для корректного сравнения используем фиксированный размер таблицы
    и варьируем количество элементов для достижения нужного коэффициента заполнения.
    
    Args:
        load_factors: Список коэффициентов заполнения для тестирования
        num_keys: Базовое количество ключей (используется для расчета размера таблицы)
        probing_method: Метод пробирования ('linear' или 'double')
        hash_function: Используемая хеш-функция
        num_runs: Количество запусков для усреднения
        
    Returns:
        Словарь с результатами: insert_times, search_times, delete_times, collisions
    """
    results = {
        'load_factors': load_factors,
        'insert_times': [],
        'search_times': [],
        'delete_times': [],
        'collisions': [],
        'max_probe_distances': [],
        'avg_probe_distances': [],
        'table_sizes': [],
        'table_size_bytes': []
    }
    
    # Используем фиксированный размер таблицы для всех коэффициентов заполнения
    # Базовый размер рассчитываем для максимального коэффициента заполнения
    # Для открытой адресации добавляем запас (учитываем метод пробирования)
    max_lf = max(load_factors)
    base_table_size = calculate_table_size_for_load_factor(
        max_lf, num_keys, is_open_addressing=True, probing_method=probing_method
    )
    
    for lf in load_factors:
        # Вычисляем количество элементов для достижения нужного коэффициента заполнения
        # при фиксированном размере таблицы
        actual_num_keys = int(base_table_size * lf)
        
        insert_times = []
        search_times = []
        delete_times = []
        collisions_list = []
        max_probe_distances = []
        avg_probe_distances = []
        
        for run in range(num_runs):
            table = HashTableOpenAddressing(
                initial_size=base_table_size,
                load_factor_threshold=1.0,  # Отключаем автоматическое рехеширование
                hash_function=hash_function,
                probing_method=probing_method
            )
            
            keys = generate_test_data(actual_num_keys)
            
            # Измеряем вставку
            try:
                insert_time = measure_insert_time(table, keys)
                insert_times.append(insert_time)
                
                # Получаем статистику после вставки
                stats = table.get_statistics()
                collisions_list.append(stats['collisions'])
                max_probe_distances.append(stats.get('max_probe_distance', 0))
                avg_probe_distances.append(stats.get('avg_probe_distance', 0))
                
                # Перемешиваем ключи для более реалистичного поиска
                random.shuffle(keys)
                
                # Измеряем поиск
                search_time = measure_search_time(table, keys)
                search_times.append(search_time)
                
                # Измеряем удаление
                delete_time = measure_delete_time(table, keys)
                delete_times.append(delete_time)
                
            except RuntimeError as e:
                # Если таблица переполнена, пропускаем этот запуск
                print(f"  Предупреждение: таблица переполнена при load_factor={lf}, run={run+1}")
                print(f"    Размер таблицы: {base_table_size}, Попытка вставить: {actual_num_keys}")
                continue
        
        # Усредняем результаты (только если есть успешные запуски)
        if insert_times:
            results['insert_times'].append(sum(insert_times) / len(insert_times))
            results['search_times'].append(sum(search_times) / len(search_times))
            results['delete_times'].append(sum(delete_times) / len(delete_times))
            results['collisions'].append(sum(collisions_list) / len(collisions_list))
            results['max_probe_distances'].append(sum(max_probe_distances) / len(max_probe_distances) if max_probe_distances else 0)
            results['avg_probe_distances'].append(sum(avg_probe_distances) / len(avg_probe_distances) if avg_probe_distances else 0)
            results['table_sizes'].append(base_table_size)
            # Приблизительный размер в байтах (каждый слот - указатель на объект, примерно 8 байт на 64-битной системе)
            # Плюс сами данные (ключ + значение), но для оценки используем только размер таблицы
            results['table_size_bytes'].append(base_table_size * 8)  # Примерная оценка
        else:
            # Если все запуски провалились, добавляем нули
            print(f"  Ошибка: все запуски провалились при load_factor={lf}")
            print(f"    Размер таблицы: {base_table_size}, Попытка вставить: {actual_num_keys}")
            results['insert_times'].append(0.0)
            results['search_times'].append(0.0)
            results['delete_times'].append(0.0)
            results['collisions'].append(0.0)
            results['max_probe_distances'].append(0.0)
            results['avg_probe_distances'].append(0.0)
            results['table_sizes'].append(base_table_size)
            results['table_size_bytes'].append(base_table_size * 8)
    
    return results


def experiment_hash_function_quality(
    num_keys: int = 1000,
    table_size: int = 1000
) -> Dict[str, Dict[str, int]]:
    """
    Исследует влияние качества хеш-функции на количество коллизий.
    
    Args:
        num_keys: Количество ключей для тестирования
        table_size: Размер таблицы
        
    Returns:
        Словарь с результатами для каждой хеш-функции
    """
    hash_functions = ['simple', 'polynomial', 'djb2']
    results = {}
    
    for hash_func in hash_functions:
        # Используем метод цепочек для подсчета коллизий
        table = HashTableChaining(
            initial_size=table_size,
            load_factor_threshold=1.0,
            hash_function=hash_func
        )
        
        keys = generate_test_data(num_keys)
        for i, key in enumerate(keys):
            table.insert(key, f"value_{i}")
        
        stats = table.get_statistics()
        results[hash_func] = {
            'collisions': stats['collisions'],
            'max_chain_length': stats['max_chain_length'],
            'avg_chain_length': stats['avg_chain_length'],
            'empty_slots': stats['empty_slots']
        }
    
    return results


def run_all_experiments(num_keys: int = 10000) -> Dict:
    """
    Запускает все эксперименты.
    
    Args:
        num_keys: Количество ключей для тестирования
        
    Returns:
        Словарь со всеми результатами экспериментов
    """
    load_factors = [0.1, 0.5, 0.7, 0.9]
    
    print("Запуск экспериментов...")
    print(f"Количество ключей: {num_keys}")
    print(f"Коэффициенты заполнения: {load_factors}")
    
    all_results = {}
    
    # Эксперимент 1: Метод цепочек с разными хеш-функциями
    print("\n1. Эксперимент: Метод цепочек (DJB2)")
    all_results['chaining_djb2'] = experiment_chaining(
        load_factors, num_keys, hash_function='djb2'
    )
    
    print("2. Эксперимент: Метод цепочек (Polynomial)")
    all_results['chaining_polynomial'] = experiment_chaining(
        load_factors, num_keys, hash_function='polynomial'
    )
    
    print("3. Эксперимент: Метод цепочек (Simple)")
    all_results['chaining_simple'] = experiment_chaining(
        load_factors, num_keys, hash_function='simple'
    )
    
    # Эксперимент 2: Открытая адресация с линейным пробированием
    print("4. Эксперимент: Открытая адресация (линейное пробирование)")
    all_results['open_linear'] = experiment_open_addressing(
        load_factors, num_keys, probing_method='linear'
    )
    
    # Эксперимент 3: Открытая адресация с двойным хешированием
    print("5. Эксперимент: Открытая адресация (двойное хеширование)")
    all_results['open_double'] = experiment_open_addressing(
        load_factors, num_keys, probing_method='double'
    )
    
    # Эксперимент 4: Качество хеш-функций
    print("6. Эксперимент: Качество хеш-функций")
    all_results['hash_quality'] = experiment_hash_function_quality(
        num_keys=num_keys, table_size=1000
    )
    
    print("\nВсе эксперименты завершены!")
    return all_results

