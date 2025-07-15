from cart_data import get_cart, clear_cart
from product_data import get_all_products

checkout_history = []

def perform_checkout():
    cart = get_cart()
    catalog = get_all_products()
    items = []
    total = 0

    for pid, qty in cart.items():
        if pid in catalog:
            product = catalog[pid]
            items.append(f"{product['name']} x{qty} - ${product['price'] * qty:.2f}")
            total += product['price'] * qty

    if total > 0:
        checkout_history.append({
            "items": items,
            "total": total
        })
        clear_cart()

    return items, total

def get_history():
    return checkout_history
