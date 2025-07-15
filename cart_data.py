import sqlite3
from db import get_connection

def add_to_cart(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE product_id = ?", (product_id,))
    else:
        cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (product_id, 1))

    conn.commit()
    conn.close()

def get_cart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, quantity FROM cart")
    rows = cursor.fetchall()
    conn.close()
    return dict(rows)

def remove_cart_item(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

def undo_last():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT product_id FROM cart ORDER BY added_at DESC LIMIT 1")
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    pid = row[0]
    cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (pid,))
    qty = cursor.fetchone()[0]

    if qty > 1:
        cursor.execute("UPDATE cart SET quantity = quantity - 1 WHERE product_id = ?", (pid,))
    else:
        cursor.execute("DELETE FROM cart WHERE product_id = ?", (pid,))

    conn.commit()
    conn.close()
    return pid

def clear_cart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart")
    conn.commit()
    conn.close()
