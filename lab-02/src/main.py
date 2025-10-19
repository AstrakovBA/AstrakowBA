"""
Главный файл для запуска анализа производительности структур данных.
Объединяет все компоненты: LinkedList, анализ производительности и решения задач.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from linked_list import LinkedList, Stack, Queue, Node
    from performance_analysis import PerformanceAnalyzer
    from task_solutions import TaskSolutions
except ImportError as e:
    print(f"Ошибка импорта модулей: {e}")
    print("Убедитесь, что все файлы находятся в папке src/modules/")
    sys.exit(1)


class DataStructureDemo:
    """Главный класс для демонстрации работы структур данных."""
    
    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.solutions = TaskSolutions()
    
    def run_linkedlist_demo(self):
        """Демонстрация работы LinkedList."""
        print("\n" + "="*60)
        print("ДЕМОНСТРАЦИЯ LINKED LIST")
        print("="*60)
        
        # Создаем связный список
        ll = LinkedList()
        
        print("1. Создание пустого списка:")
        print(f"   Пустой: {ll.is_empty()}")
        print(f"   Размер: {len(ll)}")
        
        print("\n2. Добавление элементов в начало (O(1)):")
        for i in range(1, 6):
            ll.insert_at_start(i)
            print(f"   Добавлен {i}: {ll}")
        
        print("\n3. Добавление элементов в конец (O(1) с хвостом):")
        for i in range(6, 11):
            ll.insert_at_end(i)
            print(f"   Добавлен {i}: размер = {len(ll)}")
        
        print(f"\n4. Обход списка (O(n)): {ll.traversal()}")
        
        print("\n5. Удаление из начала (O(1)):")
        for _ in range(3):
            removed = ll.delete_from_start()
            print(f"   Удален {removed}: {ll}")
        
        print("\n6. Поиск элементов:")
        for i in [5, 10, 15]:
            found = ll.search(i)
            print(f"   Поиск {i}: {'найден' if found else 'не найден'}")
        
        print(f"\n7. Итерация по списку:")
        for item in ll:
            print(f"   Элемент: {item}")
    
    def run_stack_demo(self):
        """Демонстрация работы стека."""
        print("\n" + "="*60)
        print("ДЕМОНСТРАЦИЯ СТЕКА (LIFO)")
        print("="*60)
        
        stack = Stack()
        
        print("1. Добавление элементов в стек:")
        for i in range(1, 6):
            stack.push(i)
            print(f"   Добавлен {i}, верхний элемент: {stack.peek()}")
        
        print(f"\n2. Размер стека: {stack.size()}")
        
        print("\n3. Извлечение элементов (LIFO):")
        while not stack.is_empty():
            popped = stack.pop()
            print(f"   Извлечен {popped}, верхний элемент: {stack.peek()}")
    
    def run_queue_demo(self):
        """Демонстрация работы очереди."""
        print("\n" + "="*60)
        print("ДЕМОНСТРАЦИЯ ОЧЕРЕДИ (FIFO)")
        print("="*60)
        
        queue = Queue()
        
        print("1. Добавление элементов в очередь:")
        for i in range(1, 6):
            queue.enqueue(i)
            print(f"   Добавлен {i}, первый: {queue.front()}, последний: {queue.rear()}")
        
        print(f"\n2. Размер очереди: {queue.size()}")
        
        print("\n3. Извлечение элементов (FIFO):")
        while not queue.is_empty():
            dequeued = queue.dequeue()
            print(f"   Извлечен {dequeued}, первый: {queue.front()}")
    
    def run_performance_analysis(self, sizes: List[int] = None):
        """Запуск анализа производительности."""
        if sizes is None:
            sizes = [100, 500, 1000, 2000, 5000]
        
        print("\n" + "="*60)
        print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*60)
        
        print(f"Тестируемые размеры: {sizes}")
        print("Внимание: Тестирование может занять некоторое время...")
        
        # Запускаем анализ
        results = self.analyzer.run_comprehensive_analysis(sizes)
        
        # Выводим результаты
        self.analyzer.print_comparison_table()
        self.analyzer.analyze_asymptotic_complexity()
        
        # Создаем графики в отдельных окнах
        try:
            self.analyzer.create_performance_plots("performance_analysis.png")
            print("\nГрафики производительности созданы в отдельных окнах и сохранены в папке docs:")
            print("- docs/insert_at_start.png - Вставка в начало")
            print("- docs/pop_from_start.png - Удаление из начала") 
            print("- docs/insert_at_end.png - Добавление в конец")
            print("- docs/traversal.png - Обход элементов")
            print("- docs/performance_analysis.png - Сводный график")
        except Exception as e:
            print(f"\nОшибка при создании графиков: {e}")
            print("Убедитесь, что установлен matplotlib: pip install matplotlib")
    
    def run_task_solutions(self):
        """Запуск решения задач."""
        print("\n" + "="*60)
        print("РЕШЕНИЕ ЗАДАЧ")
        print("="*60)
        
        # Демонстрируем все решения
        self.solutions.demonstrate_data_structures()
        
        # Сравниваем методы проверки палиндромов
        self._benchmark_palindrome_methods()
    
    def _benchmark_palindrome_methods(self):
        """Сравнение методов проверки палиндромов."""
        print("\n" + "="*60)
        print("СРАВНЕНИЕ МЕТОДОВ ПРОВЕРКИ ПАЛИНДРОМОВ")
        print("="*60)
        
        from collections import deque
        import timeit
        
        test_strings = [
            "racecar",
            "A man a plan a canal Panama",
            "Madam, I'm Adam",
            "Was it a car or a cat I saw?",
            "hello world this is not a palindrome",
            "1234567890987654321"
        ]
        
        def palindrome_with_deque(text):
            cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
            if not cleaned_text:
                return True
            char_deque = deque(cleaned_text)
            while len(char_deque) > 1:
                if char_deque.popleft() != char_deque.pop():
                    return False
            return True
        
        def palindrome_with_list(text):
            cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
            if not cleaned_text:
                return True
            char_list = list(cleaned_text)
            while len(char_list) > 1:
                if char_list.pop(0) != char_list.pop():
                    return False
            return True
        
        def palindrome_with_string(text):
            cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
            return cleaned_text == cleaned_text[::-1]
        
        print(f"{'Строка':<30} {'deque':<10} {'list':<10} {'string':<10}")
        print("-" * 60)
        
        for text in test_strings:
            deque_time = timeit.timeit(lambda: palindrome_with_deque(text), number=1000)
            list_time = timeit.timeit(lambda: palindrome_with_list(text), number=1000)
            string_time = timeit.timeit(lambda: palindrome_with_string(text), number=1000)
            
            print(f"{text[:27]:<30} {deque_time:<10.6f} {list_time:<10.6f} {string_time:<10.6f}")
    
    def create_summary_report(self):
        """Создание итогового отчета."""
        print("\n" + "="*60)
        print("ИТОГОВЫЙ ОТЧЕТ")
        print("="*60)
        
        print("\n1. РЕАЛИЗОВАННЫЕ СТРУКТУРЫ ДАННЫХ:")
        print("   ✓ LinkedList с методами:")
        print("     - insert_at_start: O(1)")
        print("     - insert_at_end: O(1) с хвостом")
        print("     - delete_from_start: O(1)")
        print("     - traversal: O(n)")
        print("     - search: O(n)")
        
        print("\n   ✓ Stack (на основе LinkedList):")
        print("     - push: O(1)")
        print("     - pop: O(1)")
        print("     - peek: O(1)")
        
        print("\n   ✓ Queue (на основе LinkedList):")
        print("     - enqueue: O(1)")
        print("     - dequeue: O(1)")
        print("     - front/rear: O(1)")
        
        print("\n2. АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
        print("   ✓ Сравнение list vs LinkedList для вставки в начало")
        print("   ✓ Сравнение list vs deque для удаления из начала")
        print("   ✓ Измерения с использованием timeit")
        print("   ✓ Графики производительности")
        
        print("\n3. РЕШЕННЫЕ ЗАДАЧИ:")
        print("   ✓ Проверка сбалансированности скобок (стек)")
        print("   ✓ Симуляция очереди печати (deque)")
        print("   ✓ Проверка палиндромов (deque)")
        
        print("\n4. КЛЮЧЕВЫЕ ВЫВОДЫ:")
        print("   • LinkedList превосходит list для операций вставки/удаления в начало")
        print("   • deque превосходит list для операций удаления из начала")
        print("   • deque оптимален для проверки палиндромов")
        print("   • Стек идеален для проверки скобок")
        print("   • Очередь эффективна для FIFO операций")
    
    def run_full_demo(self):
        """Запуск полной демонстрации."""
        print("ДЕМОНСТРАЦИЯ СТРУКТУР ДАННЫХ И АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("=" * 70)
        
        # 1. Демонстрация LinkedList
        self.run_linkedlist_demo()
        
        # 2. Демонстрация стека
        self.run_stack_demo()
        
        # 3. Демонстрация очереди
        self.run_queue_demo()
        
        # 4. Анализ производительности (с меньшими размерами для демонстрации)
        self.run_performance_analysis([100, 500, 1000])
        
        # 5. Решение задач
        self.run_task_solutions()
        
        # 6. Итоговый отчет
        self.create_summary_report()


def main():
    """Главная функция."""
    print()
    print("Модель: Infinix InBook Y3 Plus (YL512)")
    print("Процессор: 12th Gen Intel(R) Core(TM) i3-1215U")
    print("Видеочип: Intel(R) UHD Graphics")
    print("ОЗУ: 16 ГБ, тип: LPDDR4")
    print()

    demo = DataStructureDemo()
    
    try:
        # Запускаем полную демонстрацию
        demo.run_full_demo()
            
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("Попробуйте запустить программу снова.")


if __name__ == "__main__":
    main()
