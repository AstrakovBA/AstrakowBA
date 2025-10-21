"""
Реализация связного списка (LinkedList) для демонстрации принципов его работы.
Включает класс Node и класс LinkedList с основными операциями.
"""

from typing import Any, Optional


class Node:
    """Узел связного списка."""
    
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None
    
    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """Реализация связного списка с основными операциями."""
    
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0
    
    def is_empty(self) -> bool:
        """Проверка на пустоту списка. O(1)"""
        return self.head is None
    
    def insert_at_start(self, data: Any) -> None:
        """
        Вставка элемента в начало списка.
        Асимптотическая сложность: O(1)
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1
    
    def insert_at_end(self, data: Any) -> None:
        """
        Вставка элемента в конец списка.
        Асимптотическая сложность: O(1) с хвостом, O(n) без хвоста
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def delete_from_start(self) -> Optional[Any]:
        """
        Удаление элемента из начала списка.
        Асимптотическая сложность: O(1)
        """
        if self.is_empty():
            return None
        
        data = self.head.data
        self.head = self.head.next
        
        # Если список стал пустым, обновляем tail
        if self.head is None:
            self.tail = None
        
        self.size -= 1
        return data
    
    def delete_from_end(self) -> Optional[Any]:
        """
        Удаление элемента из конца списка.
        Асимптотическая сложность: O(n)
        """
        if self.is_empty():
            return None
        
        if self.head == self.tail:  # Один элемент
            data = self.head.data
            self.head = None
            self.tail = None
            self.size = 0
            return data
        
        # Находим предпоследний элемент
        current = self.head
        while current.next != self.tail:
            current = current.next
        
        data = self.tail.data
        self.tail = current
        self.tail.next = None
        self.size -= 1
        return data
    
    def traversal(self) -> list:
        """
        Обход всех элементов списка.
        Асимптотическая сложность: O(n)
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    
    def search(self, data: Any) -> bool:
        """
        Поиск элемента в списке.
        Асимптотическая сложность: O(n)
        """
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def get_size(self) -> int:
        """
        Получение размера списка.
        Асимптотическая сложность: O(1)
        """
        return self.size
    
    def __len__(self) -> int:
        """Возвращает размер списка. O(1)"""
        return self.size
    
    def __repr__(self) -> str:
        """Строковое представление списка. O(n)"""
        if self.is_empty():
            return "LinkedList([])"
        
        elements = self.traversal()
        return f"LinkedList({elements})"
    
    def __iter__(self):
        """Итератор по элементам списка. O(n)"""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next


# Дополнительные методы для демонстрации работы как стека и очереди

class Stack:
    """Реализация стека на основе связного списка."""
    
    def __init__(self):
        self.linked_list = LinkedList()
    
    def push(self, data: Any) -> None:
        """Добавление элемента в стек. O(1)"""
        self.linked_list.insert_at_start(data)
    
    def pop(self) -> Optional[Any]:
        """Удаление элемента из стека. O(1)"""
        return self.linked_list.delete_from_start()
    
    def peek(self) -> Optional[Any]:
        """Просмотр верхнего элемента стека. O(1)"""
        if self.linked_list.is_empty():
            return None
        return self.linked_list.head.data
    
    def is_empty(self) -> bool:
        """Проверка на пустоту стека. O(1)"""
        return self.linked_list.is_empty()
    
    def size(self) -> int:
        """Размер стека. O(1)"""
        return self.linked_list.get_size()


class Queue:
    """Реализация очереди на основе связного списка."""
    
    def __init__(self):
        self.linked_list = LinkedList()
    
    def enqueue(self, data: Any) -> None:
        """Добавление элемента в очередь. O(1)"""
        self.linked_list.insert_at_end(data)
    
    def dequeue(self) -> Optional[Any]:
        """Удаление элемента из очереди. O(1)"""
        return self.linked_list.delete_from_start()
    
    def front(self) -> Optional[Any]:
        """Просмотр первого элемента очереди. O(1)"""
        if self.linked_list.is_empty():
            return None
        return self.linked_list.head.data
    
    def rear(self) -> Optional[Any]:
        """Просмотр последнего элемента очереди. O(1)"""
        if self.linked_list.is_empty():
            return None
        return self.linked_list.tail.data
    
    def is_empty(self) -> bool:
        """Проверка на пустоту очереди. O(1)"""
        return self.linked_list.is_empty()
    
    def size(self) -> int:
        """Размер очереди. O(1)"""
        return self.linked_list.get_size()


if __name__ == "__main__":
    # Демонстрация работы LinkedList
    print("=== Демонстрация LinkedList ===")
    ll = LinkedList()
    
    # Вставка элементов
    ll.insert_at_start(1)
    ll.insert_at_start(2)
    ll.insert_at_end(3)
    ll.insert_at_end(4)
    
    print(f"Список после вставки: {ll}")
    print(f"Размер: {len(ll)}")
    
    # Обход
    print(f"Элементы: {ll.traversal()}")
    
    # Удаление
    print(f"Удален из начала: {ll.delete_from_start()}")
    print(f"Удален из конца: {ll.delete_from_end()}")
    print(f"Список после удаления: {ll}")
    
    # Демонстрация стека
    print("\n=== Демонстрация Stack ===")
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Верхний элемент: {stack.peek()}")
    print(f"Извлечен: {stack.pop()}")
    print(f"Верхний элемент: {stack.peek()}")
    
    # Демонстрация очереди
    print("\n=== Демонстрация Queue ===")
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(f"Первый элемент: {queue.front()}")
    print(f"Последний элемент: {queue.rear()}")
    print(f"Извлечен: {queue.dequeue()}")
    print(f"Первый элемент: {queue.front()}")

