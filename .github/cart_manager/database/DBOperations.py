import sqlite3
from typing import List, Dict, Optional


class DBOperations:
    def __init__(self, db_name='cart_manager.db'):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL,
                    stock INTEGER,
                    priority INTEGER DEFAULT 3
                )
            ''')

            # Cart items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INTEGER PRIMARY KEY,
                    product_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            conn.commit()

    def add_product(self, product: Dict) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, category, price, stock, priority)
                VALUES (?, ?, ?, ?, ?)
            ''', (product['name'], product['category'], product['price'],
                  product['stock'], product.get('priority', 3)))
            product_id = cursor.lastrowid
            conn.commit()
        return product_id

    def get_product(self, product_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'category': row[2],
                    'price': row[3],
                    'stock': row[4],
                    'priority': row[5]
                }
        return None

    def update_product(self, product_id: int, updates: Dict) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET name = ?, category = ?, price = ?, stock = ?, priority = ?
                WHERE id = ?
            ''', (updates['name'], updates['category'], updates['price'],
                  updates['stock'], updates.get('priority', 3), product_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_products(self) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products')
            return [{
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'price': row[3],
                'stock': row[4],
                'priority': row[5]
            } for row in cursor.fetchall()]

    def add_to_cart(self, product_id: int, quantity: int = 1) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Check if product already in cart
            cursor.execute('''
                SELECT id, quantity FROM cart_items WHERE product_id = ?
            ''', (product_id,))
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[1] + quantity
                cursor.execute('''
                    UPDATE cart_items SET quantity = ? WHERE id = ?
                ''', (new_quantity, existing_item[0]))
                item_id = existing_item[0]
            else:
                cursor.execute('''
                    INSERT INTO cart_items (product_id, quantity)
                    VALUES (?, ?)
                ''', (product_id, quantity))
                item_id = cursor.lastrowid

            conn.commit()
        return item_id

    def remove_from_cart(self, product_id: int, quantity: int = 1) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Get current quantity
            cursor.execute('''
                SELECT id, quantity FROM cart_items WHERE product_id = ?
            ''', (product_id,))
            existing_item = cursor.fetchone()

            if not existing_item:
                return False

            if existing_item[1] <= quantity:
                # Remove the item completely
                cursor.execute('''
                    DELETE FROM cart_items WHERE id = ?
                ''', (existing_item[0],))
            else:
                # Reduce quantity
                new_quantity = existing_item[1] - quantity
                cursor.execute('''
                    UPDATE cart_items SET quantity = ? WHERE id = ?
                ''', (new_quantity, existing_item[0]))

            conn.commit()
            return True

    def get_cart_items(self) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ci.id, p.id, p.name, p.price, ci.quantity 
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
            ''')
            return [{
                'cart_item_id': row[0],
                'product_id': row[1],
                'name': row[2],
                'price': row[3],
                'quantity': row[4]
            } for row in cursor.fetchall()]

    def clear_cart(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cart_items')
            conn.commit()