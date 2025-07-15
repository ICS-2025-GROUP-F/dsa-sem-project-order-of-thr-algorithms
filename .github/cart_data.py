from collections import defaultdict

cart_stack = []
cart_items = defaultdict(int)

def add_to_cart(pid):
    cart_stack.append(pid)
    cart_items[pid] += 1

def undo_last():
    if cart_stack:
        last_pid = cart_stack.pop()
        cart_items[last_pid] -= 1
        if cart_items[last_pid] <= 0:
            del cart_items[last_pid]
        return last_pid
    return None

def remove_product(pid):
    if pid in cart_items:
        del cart_items[pid]

def get_cart():
    return dict(cart_items)

def calculate_total(product_catalog):
    total = 0
    for pid, qty in cart_items.items():
        if pid in product_catalog:
            total += product_catalog[pid]["price"] * qty
    return total

def clear_cart():
    cart_stack.clear()
    cart_items.clear()