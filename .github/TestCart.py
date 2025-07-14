import unittest
from CartManager import CartManager


class TestCartManager(unittest.TestCase):
    def setUp(self):
        self.cart = CartManager()

    def test_add_item_valid(self):
        self.assertTrue(self.cart.add_item("Apple", 0.99, 2))

    # ... (other test cases as shown previously)


if __name__ == "__main__":
    unittest.main()