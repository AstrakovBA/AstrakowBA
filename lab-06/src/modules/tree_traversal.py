"""
Модуль для реализации различных методов обхода бинарного дерева.

Методы обхода:
    - In-order (левый -> корень -> правый): элементы в отсортированном порядке
    - Pre-order (корень -> левый -> правый): корень перед поддеревьями
    - Post-order (левый -> правый -> корень): корень после поддеревьев
"""

from src.modules.binary_search_tree import TreeNode


def in_order_recursive(node, result=None):
    """
    Рекурсивный in-order обход дерева.
    
    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов (создается автоматически)
        
    Returns:
        list: Список значений узлов в порядке in-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    """
    if result is None:
        result = []
    
    if node is not None:
        in_order_recursive(node.left, result)
        result.append(node.value)
        in_order_recursive(node.right, result)
    
    return result


def pre_order_recursive(node, result=None):
    """
    Рекурсивный pre-order обход дерева.
    
    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов (создается автоматически)
        
    Returns:
        list: Список значений узлов в порядке pre-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    """
    if result is None:
        result = []
    
    if node is not None:
        result.append(node.value)
        pre_order_recursive(node.left, result)
        pre_order_recursive(node.right, result)
    
    return result


def post_order_recursive(node, result=None):
    """
    Рекурсивный post-order обход дерева.
    
    Args:
        node: Корень дерева/поддерева
        result: Список для сохранения результатов (создается автоматически)
        
    Returns:
        list: Список значений узлов в порядке post-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    """
    if result is None:
        result = []
    
    if node is not None:
        post_order_recursive(node.left, result)
        post_order_recursive(node.right, result)
        result.append(node.value)
    
    return result


def in_order_iterative(root):
    """
    Итеративный in-order обход дерева с использованием стека.
    
    Args:
        root: Корень дерева
        
    Returns:
        list: Список значений узлов в порядке in-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    Пространственная сложность: O(h), где h - высота дерева
    """
    result = []
    stack = []
    current = root
    
    while current is not None or len(stack) > 0:
        # Дойти до самого левого узла
        while current is not None:
            stack.append(current)
            current = current.left
        
        # Извлечь узел из стека и обработать
        current = stack.pop()
        result.append(current.value)
        
        # Перейти к правому поддереву
        current = current.right
    
    return result


def pre_order_iterative(root):
    """
    Итеративный pre-order обход дерева с использованием стека.
    
    Args:
        root: Корень дерева
        
    Returns:
        list: Список значений узлов в порядке pre-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    Пространственная сложность: O(h), где h - высота дерева
    """
    if root is None:
        return []
    
    result = []
    stack = [root]
    
    while len(stack) > 0:
        current = stack.pop()
        result.append(current.value)
        
        # Добавляем правый узел первым, чтобы левый обрабатывался первым
        if current.right is not None:
            stack.append(current.right)
        if current.left is not None:
            stack.append(current.left)
    
    return result


def post_order_iterative(root):
    """
    Итеративный post-order обход дерева с использованием стека.
    
    Args:
        root: Корень дерева
        
    Returns:
        list: Список значений узлов в порядке post-order обхода
        
    Временная сложность: O(n), где n - количество узлов
    Пространственная сложность: O(h), где h - высота дерева
    """
    if root is None:
        return []
    
    result = []
    stack = [root]
    last_visited = None
    
    while len(stack) > 0:
        current = stack[-1]
        
        # Если текущий узел - лист или правый ребенок уже обработан
        if (current.left is None and current.right is None) or \
           (current.right is not None and current.right == last_visited):
            result.append(current.value)
            stack.pop()
            last_visited = current
        else:
            # Добавляем правый и левый узлы в стек
            if current.right is not None:
                stack.append(current.right)
            if current.left is not None:
                stack.append(current.left)
    
    return result


def print_in_order(node):
    """Печать элементов дерева в порядке in-order обхода."""
    result = in_order_recursive(node)
    print("In-order:", result)
    return result


def print_pre_order(node):
    """Печать элементов дерева в порядке pre-order обхода."""
    result = pre_order_recursive(node)
    print("Pre-order:", result)
    return result


def print_post_order(node):
    """Печать элементов дерева в порядке post-order обхода."""
    result = post_order_recursive(node)
    print("Post-order:", result)
    return result

