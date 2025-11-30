"""
Главный модуль для запуска экспериментов и создания визуализаций.
"""

import json
from src.experiments import run_all_experiments
from src.visualization import create_all_visualizations
import os


def save_results(results: dict, filename: str = 'experiment_results.json'):
    """Сохраняет результаты экспериментов в JSON файл."""
    # Конвертируем результаты в JSON-совместимый формат
    json_results = {}
    for key, value in results.items():
        if isinstance(value, dict):
            json_results[key] = {}
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    # Конвертируем numpy типы в Python типы
                    json_results[key][sub_key] = [float(x) if isinstance(x, (int, float)) else x for x in sub_value]
                elif isinstance(sub_value, dict):
                    json_results[key][sub_key] = {
                        k: float(v) if isinstance(v, (int, float)) else v
                        for k, v in sub_value.items()
                    }
                else:
                    json_results[key][sub_key] = float(sub_value) if isinstance(sub_value, (int, float)) else sub_value
        else:
            json_results[key] = value
    
    filepath = os.path.join('docs', filename)
    os.makedirs('docs', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в {filepath}")


def main():
    """Главная функция для запуска всех экспериментов."""
    print("=" * 60)
    print("ЭКСПЕРИМЕНТАЛЬНОЕ ИССЛЕДОВАНИЕ ХЕШ-ТАБЛИЦ")
    print("=" * 60)
    
    # Количество ключей для экспериментов
    # Можно уменьшить для более быстрого выполнения
    num_keys = 10000
    
    # Запускаем все эксперименты
    results = run_all_experiments(num_keys=num_keys)
    
    # Сохраняем результаты
    save_results(results)
    
    # Создаем визуализации
    create_all_visualizations(results)
    
    # Выводим краткую сводку
    print("\n" + "=" * 60)
    print("КРАТКАЯ СВОДКА РЕЗУЛЬТАТОВ")
    print("=" * 60)
    
    if 'hash_quality' in results:
        print("\nКачество хеш-функций (количество коллизий):")
        for func, stats in results['hash_quality'].items():
            print(f"  {func:12s}: {stats['collisions']:6d} коллизий, "
                  f"макс. цепочка: {stats['max_chain_length']:3d}, "
                  f"сред. цепочка: {stats['avg_chain_length']:.2f}")
    
    # Диагностика для открытой адресации
    print("\n" + "-" * 60)
    print("ДИАГНОСТИКА ОТКРЫТОЙ АДРЕСАЦИИ")
    print("-" * 60)
    
    for method_name, method_key in [("Линейное пробирование", "open_linear"), 
                                      ("Двойное хеширование", "open_double")]:
        if method_key in results:
            method_results = results[method_key]
            print(f"\n{method_name}:")
            if 'max_probe_distances' in method_results and 'table_size_bytes' in method_results:
                for i, lf in enumerate(method_results['load_factors']):
                    max_probe = method_results['max_probe_distances'][i]
                    avg_probe = method_results['avg_probe_distances'][i]
                    table_size = method_results['table_sizes'][i]
                    table_bytes = method_results['table_size_bytes'][i]
                    table_kb = table_bytes / 1024
                    table_mb = table_kb / 1024
                    
                    print(f"  Коэффициент заполнения {lf:.1f}:")
                    print(f"    Размер таблицы: {table_size:,} слотов ({table_mb:.2f} MB)")
                    print(f"    Макс. расстояние пробирования: {max_probe:.1f}")
                    print(f"    Сред. расстояние пробирования: {avg_probe:.2f}")
                    
                    # Проверка на возможные проблемы
                    if max_probe > table_size * 0.1:
                        print(f"    ⚠️  ВНИМАНИЕ: Очень большое расстояние пробирования!")
                    if table_mb > 1.0:
                        print(f"    ⚠️  ВНИМАНИЕ: Таблица может не помещаться в L1/L2 кэш!")
    
    print("\nВсе результаты и графики сохранены в папке docs/")
    print("=" * 60)


if __name__ == '__main__':
    main()

