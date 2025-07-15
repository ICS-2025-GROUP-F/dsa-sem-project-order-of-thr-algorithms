from db import get_connection

def get_next_product_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        last_id = result[0]
        number = int(last_id[1:]) + 1
        return f"P{number}"
    return "P1000"

def add_product(pid, name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", (pid, name, price))
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    rows = cursor.fetchall()
    conn.close()
    return {pid: {"name": name, "price": price} for pid, name, price in rows}
