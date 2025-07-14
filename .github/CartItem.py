class CartItem:
    """Represents an individual product in the shopping cart"""

    def __init__(self, name: str, price: float, quantity: int = 1):
        """
        Initialize a cart item

        Args:
            name: Product name (non-empty string)
            price: Unit price (positive number)
            quantity: Quantity (positive integer, default=1)

        Raises:
            ValueError: If validation fails
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be a non-empty string")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        self._name = name.strip()
        self._price = float(price)
        self._quantity = quantity

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Quantity must be a positive integer")
        self._quantity = value

    def total_price(self) -> float:
        return self._price * self._quantity

    def __eq__(self, other) -> bool:
        if not isinstance(other, CartItem):
            return False
        return self._name.lower() == other.name.lower() and self._price == other.price

    def __repr__(self) -> str:
        return f"CartItem({self._name!r}, {self._price}, {self._quantity})"

    def __str__(self) -> str:
        return f"{self._name} (${self._price:.2f} × {self._quantity})"