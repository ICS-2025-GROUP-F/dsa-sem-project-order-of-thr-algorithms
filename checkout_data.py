from db import get_connection
from cart_data import get_cart, clear_cart
from product_data import get_all_products

def perform_checkout():
    cart = get_cart()
    catalog = get_all_products()
    total = 0

    for pid, qty in cart.items():
        if pid in catalog:
            total += catalog[pid]["price"] * qty

    if total == 0:
        return [], 0

    conn = get_connection()
    cursor = conn.cursor()

    # Create new order
    cursor.execute("INSERT INTO orders (total) VALUES (?)", (total,))
    order_id = cursor.lastrowid

    # Add items
    for pid, qty in cart.items():
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (order_id, pid, qty))

    conn.commit()
    conn.close()

    summary = [f"{catalog[pid]['name']} x{qty} - ${catalog[pid]['price'] * qty:.2f}" for pid, qty in cart.items()]
    clear_cart()

    return summary, total

def get_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, total, timestamp FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    history = []
    for order_id, total, timestamp in orders:
        cursor.execute("SELECT product_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
        items = cursor.fetchall()
        history.append({
            "id": order_id,
            "total": total,
            "timestamp": timestamp,
            "items": items
        })

    conn.close()
    return history
