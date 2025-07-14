class Stack:
    """Basic stack implementation using list"""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add item to top of stack"""
        self._items.append(item)

    def pop(self):
        """Remove and return top item"""
        return self._items.pop() if not self.is_empty() else None

    def peek(self):
        """Return top item without removal"""
        return self._items[-1] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self):
        """Empty the stack"""
        self._items = []

    def get_all_items(self) -> list:
        """Return all items (top to bottom)"""
        return self._items.copy()