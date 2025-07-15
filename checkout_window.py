import tkinter as tk
from tkinter import messagebox
from checkout_data import perform_checkout, get_history
from product_data import get_all_products

def open_checkout_window():
    window = tk.Toplevel()
    window.title("Checkout & History")
    window.geometry("500x500")

    tk.Button(window, text="Checkout", command=lambda: handle_checkout()).pack(pady=10)
    total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 12, "bold"))
    total_label.pack()

    tk.Label(window, text="Order History").pack(pady=10)
    history_listbox = tk.Listbox(window, width=60)
    history_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def handle_checkout():
        items, total = perform_checkout()
        if total == 0:
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
            return

        total_label.config(text=f"Total: ${total:.2f}")
        update_history()
        messagebox.showinfo("Checkout Complete", f"Order placed. Total: ${total:.2f}")

    def update_history():
        history_listbox.delete(0, tk.END)
        product_catalog = get_all_products()
        orders = get_history()

        for order in orders:
            history_listbox.insert(tk.END, f"Order #{order['id']} - ${order['total']:.2f} on {order['timestamp']}")
            for pid, qty in order['items']:
                product = product_catalog.get(pid, {"name": "[Unknown Product]", "price": 0})
                item_total = product['price'] * qty
                history_listbox.insert(tk.END, f"  • {product['name']} x{qty} - ${item_total:.2f}")
            history_listbox.insert(tk.END, "")

    update_history()
