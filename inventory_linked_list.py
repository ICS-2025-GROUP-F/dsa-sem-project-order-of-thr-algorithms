from typing import Optional

class Node:
    def __init__(self, product):
        self.product = product
        self.next: Optional[Node] = None

class InventoryLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0  # Keep track of the number of products

    def insert_product(self, product):
        """
        Insert a new product into the inventory
        Time Complexity: O(1) - insertion at the beginning
        """
        new_node = Node(product)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
        return True

    def search_product(self, search_term, search_by='name'):
        """
        Search for a product by name, category, or id
        Time Complexity: O(n) - need to traverse the entire list
        """
        current = self.head
        results = []

        while current:
            if search_by == 'name' and search_term.lower() in current.product.name.lower():
                results.append(current.product)
            elif search_by == 'category' and search_term.lower() == current.product.category.lower():
                results.append(current.product)
            elif search_by == 'id' and search_term == current.product.id:
                return current.product
            current = current.next

        return results if search_by != 'id' else None

    def update_stock(self, product_id, quantity):
        """
        Update the stock quantity for a specific product
        Time Complexity: O(n) - need to find the product first
        """
        current = self.head

        while current:
            if current.product.id == product_id:
                current.product.stock = quantity
                return True
            current = current.next
        return False

    def delete_product(self, product_id):
        """
        Remove a product from the inventory
        Time Complexity: O(n) - need to find the product first
        """
        if not self.head:
            return False

        if self.head.product.id == product_id:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.product.id == product_id:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def get_stock(self, product_id):
        """
        Get the current stock level of a product
        Time Complexity: O(n) - need to find the product first
        """
        current = self.head

        while current:
            if current.product.id == product_id:
                return current.product.stock
            current = current.next
        return None

    def get_all_products(self):
        """
        Get all products in the inventory
        Time Complexity: O(n)
        """
        products = []
        current = self.head
        while current:
            products.append(current.product)
            current = current.next
        return products

    def size(self):
        """
        Return the number of products in the inventory
        Time Complexity: O(1)
        """
        return self._size