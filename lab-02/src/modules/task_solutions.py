"""
Решение задач с использованием различных структур данных.
Включает проверку сбалансированности скобок, симуляцию очереди печати и проверку палиндромов.
"""

from collections import deque
from typing import List, Dict, Any, Optional
import random
import time
from linked_list import Stack, Queue


class TaskSolutions:
    """Класс с решениями различных задач."""
    
    @staticmethod
    def check_balanced_brackets(expression: str) -> bool:
        """
        Проверка сбалансированности скобок с использованием стека.
        
        Args:
            expression: Строка с выражением для проверки
            
        Returns:
            True если скобки сбалансированы, False иначе
            
        Асимптотическая сложность: O(n)
        """
        if not expression:
            return True
        
        # Создаем стек для хранения открывающих скобок
        stack = Stack()
        
        # Словарь соответствия закрывающих и открывающих скобок
        bracket_pairs = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        
        # Множество открывающих скобок
        opening_brackets = {'(', '[', '{'}
        
        for char in expression:
            if char in opening_brackets:
                # Если встретили открывающую скобку, добавляем в стек
                stack.push(char)
            elif char in bracket_pairs:
                # Если встретили закрывающую скобку
                if stack.is_empty():
                    # Если стек пуст, значит нет соответствующей открывающей скобки
                    return False
                
                # Извлекаем последнюю открывающую скобку
                last_opening = stack.pop()
                
                # Проверяем соответствие
                if last_opening != bracket_pairs[char]:
                    return False
        
        # Если стек пуст, все скобки сбалансированы
        return stack.is_empty()
    
    @staticmethod
    def print_queue_simulation(num_documents: int = 10) -> Dict[str, Any]:
        """
        Симуляция обработки задач в очереди печати с использованием deque.
        
        Args:
            num_documents: Количество документов для печати
            
        Returns:
            Словарь с результатами симуляции
            
        Асимптотическая сложность: O(n) где n - количество документов
        """
        print(f"\n=== Симуляция очереди печати ({num_documents} документов) ===")
        
        # Создаем очередь печати
        print_queue = deque()
        
        # Генерируем документы для печати
        documents = []
        for i in range(num_documents):
            doc = {
                'id': i + 1,
                'name': f'Документ_{i + 1}',
                'pages': random.randint(1, 10),
                'priority': random.choice(['Низкий', 'Средний', 'Высокий']),
                'timestamp': time.time()
            }
            documents.append(doc)
            print_queue.append(doc)
        
        print(f"В очередь добавлено {len(documents)} документов")
        
        # Статистика
        stats = {
            'total_documents': num_documents,
            'processed_documents': 0,
            'total_pages': 0,
            'processing_times': [],
            'priority_stats': {'Низкий': 0, 'Средний': 0, 'Высокий': 0}
        }
        
        # Обрабатываем документы
        print("\nОбработка документов:")
        print("-" * 60)
        
        while print_queue:
            # Извлекаем документ из очереди (FIFO)
            current_doc = print_queue.popleft()
            
            # Симулируем время печати (0.1 сек на страницу)
            processing_time = current_doc['pages'] * 0.1
            time.sleep(processing_time)  # В реальном коде это была бы печать
            
            # Обновляем статистику
            stats['processed_documents'] += 1
            stats['total_pages'] += current_doc['pages']
            stats['processing_times'].append(processing_time)
            stats['priority_stats'][current_doc['priority']] += 1
            
            print(f"Печатается: {current_doc['name']} "
                  f"({current_doc['pages']} стр., "
                  f"{current_doc['priority']} приоритет, "
                  f"{processing_time:.1f}с)")
        
        # Выводим итоговую статистику
        print("\n" + "=" * 60)
        print("ИТОГОВАЯ СТАТИСТИКА:")
        print(f"Обработано документов: {stats['processed_documents']}")
        print(f"Общее количество страниц: {stats['total_pages']}")
        print(f"Среднее время обработки: {sum(stats['processing_times']) / len(stats['processing_times']):.2f}с")
        print(f"Общее время обработки: {sum(stats['processing_times']):.2f}с")
        
        print("\nСтатистика по приоритетам:")
        for priority, count in stats['priority_stats'].items():
            print(f"  {priority}: {count} документов")
        
        return stats
    
    @staticmethod
    def is_palindrome(text: str) -> bool:
        """
        Проверка, является ли строка палиндромом с использованием deque.
        
        Args:
            text: Строка для проверки
            
        Returns:
            True если строка является палиндромом, False иначе
            
        Асимптотическая сложность: O(n)
        """
        if not text:
            return True
        
        # Очищаем строку от пробелов и приводим к нижнему регистру
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        
        if not cleaned_text:
            return True
        
        # Создаем deque из символов строки
        char_deque = deque(cleaned_text)
        
        # Сравниваем символы с обоих концов
        while len(char_deque) > 1:
            # Извлекаем символы с обоих концов
            left_char = char_deque.popleft()  # O(1)
            right_char = char_deque.pop()     # O(1)
            
            # Если символы не совпадают, строка не является палиндромом
            if left_char != right_char:
                return False
        
        # Если все символы совпали, строка является палиндромом
        return True
    
    @staticmethod
    def advanced_palindrome_check(text: str) -> Dict[str, Any]:
        """
        Расширенная проверка палиндромов с дополнительной информацией.
        
        Args:
            text: Строка для проверки
            
        Returns:
            Словарь с результатами анализа
        """
        result = {
            'original_text': text,
            'cleaned_text': '',
            'is_palindrome': False,
            'length': 0,
            'processing_time': 0,
            'method': 'deque'
        }
        
        start_time = time.time()
        
        # Очищаем текст
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        result['cleaned_text'] = cleaned_text
        result['length'] = len(cleaned_text)
        
        if not cleaned_text:
            result['is_palindrome'] = True
            result['processing_time'] = time.time() - start_time
            return result
        
        # Проверяем палиндром с помощью deque
        char_deque = deque(cleaned_text)
        
        while len(char_deque) > 1:
            left_char = char_deque.popleft()
            right_char = char_deque.pop()
            
            if left_char != right_char:
                result['is_palindrome'] = False
                result['processing_time'] = time.time() - start_time
                return result
        
        result['is_palindrome'] = True
        result['processing_time'] = time.time() - start_time
        return result
    
    @staticmethod
    def demonstrate_data_structures():
        """Демонстрация работы различных структур данных."""
        print("\n" + "="*60)
        print("ДЕМОНСТРАЦИЯ РАБОТЫ СТРУКТУР ДАННЫХ")
        print("="*60)
        
        # 1. Демонстрация стека для проверки скобок
        print("\n1. ПРОВЕРКА СБАЛАНСИРОВАННОСТИ СКОБОК:")
        test_expressions = [
            "()",
            "()[]{}",
            "([{}])",
            "([)]",
            "((()))",
            "{[()]}",
            "{[()]",
            "{[()]}()",
            "a + b * (c - d)",
            "if (x > 0) { return x; }"
        ]
        
        for expr in test_expressions:
            is_balanced = TaskSolutions.check_balanced_brackets(expr)
            status = "✓ Сбалансированы" if is_balanced else "✗ Не сбалансированы"
            print(f"  '{expr}' -> {status}")
        
        # 2. Демонстрация палиндромов
        print("\n2. ПРОВЕРКА ПАЛИНДРОМОВ:")
        test_strings = [
            "racecar",
            "A man a plan a canal Panama",
            "Madam, I'm Adam",
            "Was it a car or a cat I saw?",
            "hello",
            "12321",
            "А роза упала на лапу Азора",
            "",
            "a",
            "ab"
        ]
        
        for text in test_strings:
            result = TaskSolutions.advanced_palindrome_check(text)
            status = "✓ Палиндром" if result['is_palindrome'] else "✗ Не палиндром"
            print(f"  '{text}' -> {status}")
            if result['cleaned_text']:
                print(f"    Очищенный текст: '{result['cleaned_text']}'")
        
        # 3. Демонстрация очереди печати
        print("\n3. СИМУЛЯЦИЯ ОЧЕРЕДИ ПЕЧАТИ:")
        TaskSolutions.print_queue_simulation(5)  # Меньше документов для демонстрации


def benchmark_palindrome_methods():
    """Сравнение различных методов проверки палиндромов."""
    print("\n" + "="*60)
    print("СРАВНЕНИЕ МЕТОДОВ ПРОВЕРКИ ПАЛИНДРОМОВ")
    print("="*60)
    
    test_strings = [
        "racecar",
        "A man a plan a canal Panama",
        "Madam, I'm Adam",
        "Was it a car or a cat I saw?",
        "hello world this is not a palindrome",
        "1234567890987654321"
    ]
    
    def palindrome_with_deque(text):
        """Проверка палиндрома с помощью deque."""
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        if not cleaned_text:
            return True
        
        char_deque = deque(cleaned_text)
        while len(char_deque) > 1:
            if char_deque.popleft() != char_deque.pop():
                return False
        return True
    
    def palindrome_with_list(text):
        """Проверка палиндрома с помощью list."""
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        if not cleaned_text:
            return True
        
        char_list = list(cleaned_text)
        while len(char_list) > 1:
            if char_list.pop(0) != char_list.pop():
                return False
        return True
    
    def palindrome_with_string(text):
        """Проверка палиндрома с помощью строковых операций."""
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        return cleaned_text == cleaned_text[::-1]
    
    print(f"{'Строка':<30} {'deque':<10} {'list':<10} {'string':<10}")
    print("-" * 60)
    
    for text in test_strings:
        # Измеряем время для каждого метода
        import timeit
        
        deque_time = timeit.timeit(lambda: palindrome_with_deque(text), number=1000)
        list_time = timeit.timeit(lambda: palindrome_with_list(text), number=1000)
        string_time = timeit.timeit(lambda: palindrome_with_string(text), number=1000)
        
        print(f"{text[:27]:<30} {deque_time:<10.6f} {list_time:<10.6f} {string_time:<10.6f}")


def main():
    """Основная функция для демонстрации решений задач."""
    print("Решение задач с использованием структур данных")
    print("=" * 50)
    
    # Создаем экземпляр класса решений
    solutions = TaskSolutions()
    
    # Демонстрируем все структуры данных
    solutions.demonstrate_data_structures()
    
    # Сравниваем методы проверки палиндромов
    benchmark_palindrome_methods()
    
    print("\n" + "="*60)
    print("АНАЛИЗ АСИМПТОТИЧЕСКОЙ СЛОЖНОСТИ РЕШЕНИЙ:")
    print("="*60)
    print("1. Проверка скобок: O(n) - один проход по строке")
    print("2. Очередь печати: O(n) - обработка каждого документа")
    print("3. Проверка палиндрома:")
    print("   - deque: O(n) - сравнение с обоих концов")
    print("   - list: O(n²) - pop(0) имеет сложность O(n)")
    print("   - string: O(n) - сравнение строк")
    print("\nВывод: deque и string методы наиболее эффективны для проверки палиндромов.")


if __name__ == "__main__":
    main()

