"""
Анализ производительности различных структур данных.
Сравнение list vs LinkedList для операций вставки и list vs deque для операций очереди.
"""

import timeit
import time
from collections import deque
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np

from linked_list import LinkedList, Stack, Queue


class PerformanceAnalyzer:
    """Класс для анализа производительности различных структур данных."""
    
    def __init__(self):
        self.results = {}
    
    def measure_list_insert_at_start(self, n: int) -> float:
        """Измерение времени вставки n элементов в начало list. O(n) на каждую операцию."""
        def test():
            lst = []
            for i in range(n):
                lst.insert(0, i)
            return lst
        
        return timeit.timeit(test, number=1)
    
    def measure_linkedlist_insert_at_start(self, n: int) -> float:
        """Измерение времени вставки n элементов в начало LinkedList. O(1) на каждую операцию."""
        def test():
            ll = LinkedList()
            for i in range(n):
                ll.insert_at_start(i)
            return ll
        
        return timeit.timeit(test, number=1)
    
    def measure_list_pop_from_start(self, n: int) -> float:
        """Измерение времени удаления n элементов из начала list. O(n) на каждую операцию."""
        def test():
            lst = list(range(n))
            for _ in range(n):
                lst.pop(0)
            return lst
        
        return timeit.timeit(test, number=1)
    
    def measure_deque_pop_from_start(self, n: int) -> float:
        """Измерение времени удаления n элементов из начала deque. O(1) на каждую операцию."""
        def test():
            dq = deque(range(n))
            for _ in range(n):
                dq.popleft()
            return dq
        
        return timeit.timeit(test, number=1)
    
    def measure_list_append(self, n: int) -> float:
        """Измерение времени добавления n элементов в конец list. O(1) на каждую операцию."""
        def test():
            lst = []
            for i in range(n):
                lst.append(i)
            return lst
        
        return timeit.timeit(test, number=1)
    
    def measure_linkedlist_insert_at_end(self, n: int) -> float:
        """Измерение времени добавления n элементов в конец LinkedList. O(1) на каждую операцию."""
        def test():
            ll = LinkedList()
            for i in range(n):
                ll.insert_at_end(i)
            return ll
        
        return timeit.timeit(test, number=1)
    
    def measure_list_traversal(self, n: int) -> float:
        """Измерение времени обхода list. O(n)"""
        def test():
            lst = list(range(n))
            for item in lst:
                pass
            return lst
        
        return timeit.timeit(test, number=1)
    
    def measure_linkedlist_traversal(self, n: int) -> float:
        """Измерение времени обхода LinkedList. O(n)"""
        def test():
            ll = LinkedList()
            for i in range(n):
                ll.insert_at_end(i)
            ll.traversal()
            return ll
        
        return timeit.timeit(test, number=1)
    
    def run_comprehensive_analysis(self, sizes: List[int]) -> Dict[str, Dict[int, float]]:
        """
        Проведение комплексного анализа производительности.
        
        Args:
            sizes: Список размеров для тестирования
            
        Returns:
            Словарь с результатами измерений
        """
        print("Начинаем анализ производительности...")
        
        results = {
            'list_insert_start': {},
            'linkedlist_insert_start': {},
            'list_pop_start': {},
            'deque_pop_start': {},
            'list_append': {},
            'linkedlist_insert_end': {},
            'list_traversal': {},
            'linkedlist_traversal': {}
        }
        
        for size in sizes:
            print(f"Тестируем размер: {size}")
            
            # Вставка в начало
            try:
                results['list_insert_start'][size] = self.measure_list_insert_at_start(size)
                print(f"  list.insert(0): {results['list_insert_start'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании list.insert(0): {e}")
                results['list_insert_start'][size] = float('inf')
            
            try:
                results['linkedlist_insert_start'][size] = self.measure_linkedlist_insert_at_start(size)
                print(f"  LinkedList.insert_at_start: {results['linkedlist_insert_start'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании LinkedList.insert_at_start: {e}")
                results['linkedlist_insert_start'][size] = float('inf')
            
            # Удаление из начала
            try:
                results['list_pop_start'][size] = self.measure_list_pop_from_start(size)
                print(f"  list.pop(0): {results['list_pop_start'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании list.pop(0): {e}")
                results['list_pop_start'][size] = float('inf')
            
            try:
                results['deque_pop_start'][size] = self.measure_deque_pop_from_start(size)
                print(f"  deque.popleft(): {results['deque_pop_start'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании deque.popleft(): {e}")
                results['deque_pop_start'][size] = float('inf')
            
            # Добавление в конец
            try:
                results['list_append'][size] = self.measure_list_append(size)
                print(f"  list.append(): {results['list_append'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании list.append(): {e}")
                results['list_append'][size] = float('inf')
            
            try:
                results['linkedlist_insert_end'][size] = self.measure_linkedlist_insert_at_end(size)
                print(f"  LinkedList.insert_at_end: {results['linkedlist_insert_end'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании LinkedList.insert_at_end: {e}")
                results['linkedlist_insert_end'][size] = float('inf')
            
            # Обход
            try:
                results['list_traversal'][size] = self.measure_list_traversal(size)
                print(f"  list traversal: {results['list_traversal'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании list traversal: {e}")
                results['list_traversal'][size] = float('inf')
            
            try:
                results['linkedlist_traversal'][size] = self.measure_linkedlist_traversal(size)
                print(f"  LinkedList traversal: {results['linkedlist_traversal'][size]:.6f}s")
            except Exception as e:
                print(f"  Ошибка при тестировании LinkedList traversal: {e}")
                results['linkedlist_traversal'][size] = float('inf')
            
            print()
        
        self.results = results
        return results
    
    def print_comparison_table(self):
        """Вывод таблицы сравнения результатов."""
        if not self.results:
            print("Результаты не найдены. Сначала запустите анализ.")
            return
        
        print("\n" + "="*80)
        print("ТАБЛИЦА СРАВНЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*80)
        
        # Получаем все размеры
        all_sizes = set()
        for operation_results in self.results.values():
            all_sizes.update(operation_results.keys())
        all_sizes = sorted(all_sizes)
        
        # Заголовок таблицы
        print(f"{'Размер':<8} {'list.insert(0)':<15} {'LL.insert_start':<15} {'list.pop(0)':<15} {'deque.popleft()':<15}")
        print("-" * 80)
        
        # Данные
        for size in all_sizes:
            list_insert = self.results['list_insert_start'].get(size, 'N/A')
            ll_insert = self.results['linkedlist_insert_start'].get(size, 'N/A')
            list_pop = self.results['list_pop_start'].get(size, 'N/A')
            deque_pop = self.results['deque_pop_start'].get(size, 'N/A')
            
            print(f"{size:<8} {list_insert:<15} {ll_insert:<15} {list_pop:<15} {deque_pop:<15}")
    
    def create_performance_plots(self, save_path: str = "performance_plots.png"):
        """
        Создание графиков производительности в отдельных окнах.
        
        Args:
            save_path: Путь для сохранения графиков
        """
        if not self.results:
            print("Результаты не найдены. Сначала запустите анализ.")
            return
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import os
        except ImportError:
            print("Matplotlib не установлен. Графики не могут быть созданы.")
            return
        
        # Создаем папку docs если её нет
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
            print(f"Создана папка: {docs_dir}")
        
        # Получаем все размеры
        all_sizes = set()
        for operation_results in self.results.values():
            all_sizes.update(operation_results.keys())
        all_sizes = sorted(all_sizes)
        
        if not all_sizes:
            print("Нет данных для построения графиков.")
            return
        
        sizes = all_sizes
        
        # График 1: Вставка в начало
        plt.figure(1, figsize=(10, 6))
        list_insert_times = [self.results['list_insert_start'].get(s, 0) for s in sizes]
        ll_insert_times = [self.results['linkedlist_insert_start'].get(s, 0) for s in sizes]
        
        plt.plot(sizes, list_insert_times, 'r-o', label='list.insert(0)', linewidth=2, markersize=6)
        plt.plot(sizes, ll_insert_times, 'b-s', label='LinkedList.insert_at_start', linewidth=2, markersize=6)
        plt.xlabel('Количество элементов', fontsize=12)
        plt.ylabel('Время (секунды)', fontsize=12)
        plt.title('Сравнение производительности: Вставка в начало', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.tight_layout()
        insert_start_path = os.path.join(docs_dir, 'insert_at_start.png')
        plt.savefig(insert_start_path, dpi=300, bbox_inches='tight')
        print(f"График 'Вставка в начало' сохранен в файл: {insert_start_path}")
        plt.show()
        
        # График 2: Удаление из начала
        plt.figure(2, figsize=(10, 6))
        list_pop_times = [self.results['list_pop_start'].get(s, 0) for s in sizes]
        deque_pop_times = [self.results['deque_pop_start'].get(s, 0) for s in sizes]
        
        plt.plot(sizes, list_pop_times, 'r-o', label='list.pop(0)', linewidth=2, markersize=6)
        plt.plot(sizes, deque_pop_times, 'g-^', label='deque.popleft()', linewidth=2, markersize=6)
        plt.xlabel('Количество элементов', fontsize=12)
        plt.ylabel('Время (секунды)', fontsize=12)
        plt.title('Сравнение производительности: Удаление из начала', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.tight_layout()
        pop_start_path = os.path.join(docs_dir, 'pop_from_start.png')
        plt.savefig(pop_start_path, dpi=300, bbox_inches='tight')
        print(f"График 'Удаление из начала' сохранен в файл: {pop_start_path}")
        plt.show()
        
        # График 3: Добавление в конец
        plt.figure(3, figsize=(10, 6))
        list_append_times = [self.results['list_append'].get(s, 0) for s in sizes]
        ll_insert_end_times = [self.results['linkedlist_insert_end'].get(s, 0) for s in sizes]
        
        plt.plot(sizes, list_append_times, 'r-o', label='list.append()', linewidth=2, markersize=6)
        plt.plot(sizes, ll_insert_end_times, 'b-s', label='LinkedList.insert_at_end', linewidth=2, markersize=6)
        plt.xlabel('Количество элементов', fontsize=12)
        plt.ylabel('Время (секунды)', fontsize=12)
        plt.title('Сравнение производительности: Добавление в конец', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.tight_layout()
        insert_end_path = os.path.join(docs_dir, 'insert_at_end.png')
        plt.savefig(insert_end_path, dpi=300, bbox_inches='tight')
        print(f"График 'Добавление в конец' сохранен в файл: {insert_end_path}")
        plt.show()
        
        # График 4: Обход
        plt.figure(4, figsize=(10, 6))
        list_traversal_times = [self.results['list_traversal'].get(s, 0) for s in sizes]
        ll_traversal_times = [self.results['linkedlist_traversal'].get(s, 0) for s in sizes]
        
        plt.plot(sizes, list_traversal_times, 'r-o', label='list traversal', linewidth=2, markersize=6)
        plt.plot(sizes, ll_traversal_times, 'b-s', label='LinkedList traversal', linewidth=2, markersize=6)
        plt.xlabel('Количество элементов', fontsize=12)
        plt.ylabel('Время (секунды)', fontsize=12)
        plt.title('Сравнение производительности: Обход элементов', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.tight_layout()
        traversal_path = os.path.join(docs_dir, 'traversal.png')
        plt.savefig(traversal_path, dpi=300, bbox_inches='tight')
        print(f"График 'Обход элементов' сохранен в файл: {traversal_path}")
        plt.show()
        
        # Создаем сводный график с подграфиками
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Сводный анализ производительности структур данных', fontsize=16, fontweight='bold')
        
        # График 1: Вставка в начало
        ax1 = axes[0, 0]
        ax1.plot(sizes, list_insert_times, 'r-o', label='list.insert(0)', linewidth=2)
        ax1.plot(sizes, ll_insert_times, 'b-s', label='LinkedList.insert_at_start', linewidth=2)
        ax1.set_xlabel('Количество элементов')
        ax1.set_ylabel('Время (секунды)')
        ax1.set_title('Вставка в начало')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # График 2: Удаление из начала
        ax2 = axes[0, 1]
        ax2.plot(sizes, list_pop_times, 'r-o', label='list.pop(0)', linewidth=2)
        ax2.plot(sizes, deque_pop_times, 'g-^', label='deque.popleft()', linewidth=2)
        ax2.set_xlabel('Количество элементов')
        ax2.set_ylabel('Время (секунды)')
        ax2.set_title('Удаление из начала')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_yscale('log')
        
        # График 3: Добавление в конец
        ax3 = axes[1, 0]
        ax3.plot(sizes, list_append_times, 'r-o', label='list.append()', linewidth=2)
        ax3.plot(sizes, ll_insert_end_times, 'b-s', label='LinkedList.insert_at_end', linewidth=2)
        ax3.set_xlabel('Количество элементов')
        ax3.set_ylabel('Время (секунды)')
        ax3.set_title('Добавление в конец')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_yscale('log')
        
        # График 4: Обход
        ax4 = axes[1, 1]
        ax4.plot(sizes, list_traversal_times, 'r-o', label='list traversal', linewidth=2)
        ax4.plot(sizes, ll_traversal_times, 'b-s', label='LinkedList traversal', linewidth=2)
        ax4.set_xlabel('Количество элементов')
        ax4.set_ylabel('Время (секунды)')
        ax4.set_title('Обход элементов')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')
        
        plt.tight_layout()
        summary_path = os.path.join(docs_dir, save_path)
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        print(f"Сводный график сохранен в файл: {summary_path}")
        plt.show()
        
        print("\nВсе графики созданы и сохранены в папке docs:")
        print(f"- {insert_start_path} - Вставка в начало")
        print(f"- {pop_start_path} - Удаление из начала") 
        print(f"- {insert_end_path} - Добавление в конец")
        print(f"- {traversal_path} - Обход элементов")
        print(f"- {summary_path} - Сводный график")
    
    def analyze_asymptotic_complexity(self):
        """Анализ асимптотической сложности на основе результатов."""
        print("\n" + "="*60)
        print("АНАЛИЗ АСИМПТОТИЧЕСКОЙ СЛОЖНОСТИ")
        print("="*60)
        
        if not self.results:
            print("Результаты не найдены.")
            return
        
        # Анализ вставки в начало
        print("\n1. ВСТАВКА В НАЧАЛО:")
        print("   list.insert(0): O(n) на каждую операцию")
        print("   LinkedList.insert_at_start: O(1) на каждую операцию")
        
        sizes = sorted(self.results['list_insert_start'].keys())
        if len(sizes) >= 2:
            # Вычисляем отношение времени для разных размеров
            small_size = sizes[0]
            large_size = sizes[-1]
            
            list_ratio = (self.results['list_insert_start'][large_size] / 
                         self.results['list_insert_start'][small_size])
            ll_ratio = (self.results['linkedlist_insert_start'][large_size] / 
                       self.results['linkedlist_insert_start'][small_size])
            
            print(f"   Отношение времени для размеров {small_size} -> {large_size}:")
            print(f"   list: {list_ratio:.2f}x (ожидается квадратичное)")
            print(f"   LinkedList: {ll_ratio:.2f}x (ожидается линейное)")
        
        print("\n2. УДАЛЕНИЕ ИЗ НАЧАЛА:")
        print("   list.pop(0): O(n) на каждую операцию")
        print("   deque.popleft(): O(1) на каждую операцию")
        
        if len(sizes) >= 2:
            list_pop_ratio = (self.results['list_pop_start'][large_size] / 
                             self.results['list_pop_start'][small_size])
            deque_pop_ratio = (self.results['deque_pop_start'][large_size] / 
                              self.results['deque_pop_start'][small_size])
            
            print(f"   Отношение времени для размеров {small_size} -> {large_size}:")
            print(f"   list: {list_pop_ratio:.2f}x (ожидается квадратичное)")
            print(f"   deque: {deque_pop_ratio:.2f}x (ожидается линейное)")
        
        print("\n3. ДОБАВЛЕНИЕ В КОНЕЦ:")
        print("   list.append(): O(1) на каждую операцию")
        print("   LinkedList.insert_at_end: O(1) на каждую операцию")
        
        if len(sizes) >= 2:
            list_append_ratio = (self.results['list_append'][large_size] / 
                                self.results['list_append'][small_size])
            ll_insert_end_ratio = (self.results['linkedlist_insert_end'][large_size] / 
                                  self.results['linkedlist_insert_end'][small_size])
            
            print(f"   Отношение времени для размеров {small_size} -> {large_size}:")
            print(f"   list: {list_append_ratio:.2f}x (ожидается линейное)")
            print(f"   LinkedList: {ll_insert_end_ratio:.2f}x (ожидается линейное)")


def main():
    """Основная функция для запуска анализа производительности."""
    print("Анализ производительности структур данных")
    print("=" * 50)
    
    # Создаем анализатор
    analyzer = PerformanceAnalyzer()
    
    # Размеры для тестирования (начинаем с малых значений для демонстрации)
    test_sizes = [100, 500, 1000, 2000, 5000]
    
    print(f"Тестируемые размеры: {test_sizes}")
    print("Внимание: Тестирование может занять некоторое время...")
    
    # Запускаем анализ
    results = analyzer.run_comprehensive_analysis(test_sizes)
    
    # Выводим результаты
    analyzer.print_comparison_table()
    analyzer.analyze_asymptotic_complexity()
    
    # Создаем графики
    try:
        analyzer.create_performance_plots("performance_analysis.png")
    except Exception as e:
        print(f"Ошибка при создании графиков: {e}")
        print("Убедитесь, что установлен matplotlib: pip install matplotlib")


if __name__ == "__main__":
    main()
