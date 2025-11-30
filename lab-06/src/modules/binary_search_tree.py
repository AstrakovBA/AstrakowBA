"""
Модуль для реализации бинарного дерева поиска (BST).

Классы:
    TreeNode: Узел бинарного дерева
    BinarySearchTree: Бинарное дерево поиска с основными операциями
"""


class TreeNode:
    """Узел бинарного дерева поиска."""
    
    def __init__(self, value):
        """
        Инициализация узла.
        
        Args:
            value: Значение узла
        """
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Бинарное дерево поиска (BST).
    
    Свойства BST:
    - Все значения в левом поддереве меньше значения узла
    - Все значения в правом поддереве больше значения узла
    - Левое и правое поддеревья также являются BST
    """
    
    def __init__(self):
        """Инициализация пустого дерева."""
        self.root = None
    
    def insert(self, value):
        """
        Вставка значения в дерево.
        
        Args:
            value: Значение для вставки
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева (линейный список)
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        self.root = self._insert_recursive(self.root, value)
    
    def insert_iterative(self, value):
        """
        Итеративная вставка значения в дерево (для больших деревьев).
        
        Args:
            value: Значение для вставки
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        if self.root is None:
            self.root = TreeNode(value)
            return
        
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = TreeNode(value)
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = TreeNode(value)
                    return
                current = current.right
            else:
                # Значение уже существует
                return
    
    def _insert_recursive(self, node, value):
        """Рекурсивная вставка значения."""
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        # Если значение уже существует, ничего не делаем
        
        return node
    
    def search(self, value):
        """
        Поиск значения в дереве.
        
        Args:
            value: Значение для поиска
            
        Returns:
            TreeNode или None: Узел с искомым значением или None
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        """Рекурсивный поиск значения."""
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value):
        """
        Удаление значения из дерева.
        
        Args:
            value: Значение для удаления
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        """Рекурсивное удаление значения."""
        if node is None:
            return node
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Узел найден, нужно его удалить
            # Случай 1: Узел без детей или с одним ребенком
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Случай 2: Узел с двумя детьми
            # Находим минимальное значение в правом поддереве
            min_node = self.find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)
        
        return node
    
    def find_min(self, node=None):
        """
        Поиск узла с минимальным значением в поддереве.
        
        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)
            
        Returns:
            TreeNode: Узел с минимальным значением
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        if node is None:
            node = self.root
        
        if node is None:
            return None
        
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def find_max(self, node=None):
        """
        Поиск узла с максимальным значением в поддереве.
        
        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)
            
        Returns:
            TreeNode: Узел с максимальным значением
            
        Временная сложность:
            - Худший случай: O(n) - для вырожденного дерева
            - Средний случай: O(log n) - для сбалансированного дерева
        """
        if node is None:
            node = self.root
        
        if node is None:
            return None
        
        current = node
        while current.right is not None:
            current = current.right
        return current
    
    def is_valid_bst(self):
        """
        Проверка, является ли дерево корректным BST.
        
        Returns:
            bool: True если дерево является корректным BST, False иначе
            
        Временная сложность:
            - Худший случай: O(n) - нужно проверить все узлы
            - Средний случай: O(n)
        """
        return self._is_valid_bst_recursive(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst_recursive(self, node, min_val, max_val):
        """Рекурсивная проверка корректности BST."""
        if node is None:
            return True
        
        if node.value <= min_val or node.value >= max_val:
            return False
        
        return (self._is_valid_bst_recursive(node.left, min_val, node.value) and
                self._is_valid_bst_recursive(node.right, node.value, max_val))
    
    def height(self, node=None):
        """
        Вычисление высоты дерева/поддерева.
        
        Args:
            node: Корень поддерева (по умолчанию - корень всего дерева)
            
        Returns:
            int: Высота дерева/поддерева (-1 для пустого дерева)
            
        Временная сложность:
            - Худший случай: O(n) - нужно обойти все узлы
            - Средний случай: O(n)
        """
        if node is None:
            node = self.root
        
        return self._height_recursive(node)
    
    def _height_recursive(self, node):
        """Рекурсивное вычисление высоты поддерева."""
        if node is None:
            return -1
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return max(left_height, right_height) + 1
    
    def size(self):
        """
        Подсчет количества узлов в дереве.
        
        Returns:
            int: Количество узлов
            
        Временная сложность: O(n)
        """
        return self._size_recursive(self.root)
    
    def _size_recursive(self, node):
        """Рекурсивный подсчет узлов."""
        if node is None:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)
    
    def is_empty(self):
        """Проверка, пусто ли дерево."""
        return self.root is None
    
    def visualize(self):
        """
        Текстовая визуализация дерева с отступами.
        
        Returns:
            str: Строковое представление дерева
        """
        if self.root is None:
            return "Дерево пусто"
        
        lines = []
        self._visualize_recursive(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _visualize_recursive(self, node, prefix, is_last, lines):
        """Рекурсивная визуализация узла с отступами."""
        if node is None:
            return
        
        # Добавляем текущий узел
        marker = "└── " if is_last else "├── "
        lines.append(prefix + marker + str(node.value))
        
        # Обновляем префикс для дочерних узлов
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Обрабатываем детей
        children = []
        if node.left is not None:
            children.append((node.left, False))
        if node.right is not None:
            children.append((node.right, True))
        
        for i, (child, is_last_child) in enumerate(children):
            self._visualize_recursive(child, new_prefix, is_last_child, lines)
    
    def to_bracket_notation(self):
        """
        Представление дерева в скобочной нотации.
        
        Returns:
            str: Строковое представление в скобочной нотации
        """
        return self._to_bracket_recursive(self.root)
    
    def _to_bracket_recursive(self, node):
        """Рекурсивное преобразование в скобочную нотацию."""
        if node is None:
            return "()"
        
        left_str = self._to_bracket_recursive(node.left)
        right_str = self._to_bracket_recursive(node.right)
        
        return f"({node.value}{left_str}{right_str})"

