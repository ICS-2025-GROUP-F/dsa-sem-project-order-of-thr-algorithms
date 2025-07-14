from Stack import Stack
from CartItem import CartItem


class CartManager:
    """Manages shopping cart operations using Stack"""

    def __init__(self):
        self._cart = Stack()

    def add_item(self, name: str, price: float, quantity: int = 1) -> bool:
        """
        Add product to cart
        Returns:
            True if successful, False if invalid
        """
        try:
            new_item = CartItem(name, price, quantity)

            # Check for existing item to merge quantities
            existing_item = self._find_existing_item(new_item)
            if existing_item:
                existing_item.quantity += new_item.quantity
            else:
                self._cart.push(new_item)
            return True
        except ValueError:
            return False

    def _find_existing_item(self, target: CartItem) -> CartItem | None:
        """Find matching item in cart (same name and price)"""
        temp_stack = Stack()
        found_item = None

        # Search through stack
        while not self._cart.is_empty():
            item = self._cart.pop()
            if item == target:
                found_item = item
                break
            temp_stack.push(item)

        # Restore stack
        while not temp_stack.is_empty():
            self._cart.push(temp_stack.pop())

        return found_item

    def remove_item(self, name: str) -> bool:
        """
        Remove specific item from cart
        Returns:
            True if found and removed, False otherwise
        """
        temp_stack = Stack()
        removed = False

        while not self._cart.is_empty():
            item = self._cart.pop()
            if item.name.lower() == name.lower():
                removed = True
                break
            temp_stack.push(item)

        # Restore remaining items
        while not temp_stack.is_empty():
            self._cart.push(temp_stack.pop())

        return removed

    def update_quantity(self, name: str, new_quantity: int) -> bool:
        """Update quantity of specific item"""
        try:
            item = self._find_item_by_name(name)
            if item:
                item.quantity = new_quantity
                return True
            return False
        except ValueError:
            return False

    def _find_item_by_name(self, name: str) -> CartItem | None:
        """Find item by name without removing from stack"""
        temp_stack = Stack()
        found_item = None

        while not self._cart.is_empty():
            item = self._cart.pop()
            if item.name.lower() == name.lower():
                found_item = item
                temp_stack.push(item)  # Put it back
                break
            temp_stack.push(item)

        # Restore stack
        while not temp_stack.is_empty():
            self._cart.push(temp_stack.pop())

        return found_item

    def get_all_items(self) -> list[CartItem]:
        """Return all items in cart (most recent first)"""
        return list(reversed(self._cart.get_all_items()))

    def clear_cart(self):
        """Remove all items from cart"""
        self._cart.clear()

    def total_items(self) -> int:
        """Total number of items (counting quantities)"""
        return sum(item.quantity for item in self._cart.get_all_items())

    def subtotal(self) -> float:
        """Calculate total cost of all items"""
        return sum(item.total_price() for item in self._cart.get_all_items())

    def is_empty(self) -> bool:
        return self._cart.is_empty()