from product import Product

from inventory_linked_list import InventoryLinkedList

# Create an inventory instance
inventory = InventoryLinkedList()

# Create some products
product1 = Product("P001", "Laptop", "Electronics", 999.99, 10)
product2 = Product("P002", "Headphones", "Electronics", 99.99, 20)
product3 = Product("P003", "Mouse", "Electronics", 29.99, 30)

# Insert products into inventory
inventory.insert_product(product1)
inventory.insert_product(product2)
inventory.insert_product(product3)

# Search for products
electronics = inventory.search_product("Electronics", search_by='category')
if electronics is not None:
	print("Electronics products:", [p.name for p in electronics])
else:
	print("Electronics products: []")

# Update stock
inventory.update_stock("P001", 15)

# Get stock level
laptop_stock = inventory.get_stock("P001")
print(f"Laptop stock: {laptop_stock}")

# Delete a product
inventory.delete_product("P002")

# Get all remaining products
all_products = inventory.get_all_products()
print("Remaining products:", [p.name for p in all_products])