"""
Скрипт для запуска всех unit-тестов.
"""

import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Находим все тесты
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Загружаем тесты из всех тестовых файлов
    test_files = [
        'tests.test_hash_functions',
        'tests.test_hash_table_chaining',
        'tests.test_hash_table_open_addressing'
    ]
    
    for test_file in test_files:
        try:
            tests = loader.loadTestsFromName(test_file)
            suite.addTests(tests)
        except Exception as e:
            print(f"Предупреждение: не удалось загрузить тесты из {test_file}: {e}")
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем код выхода
    sys.exit(0 if result.wasSuccessful() else 1)


