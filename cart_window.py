import tkinter as tk
from tkinter import messagebox
from cart_data import add_to_cart, undo_last, remove_cart_item, get_cart
from product_data import get_all_products

def open_cart_window():
    window = tk.Toplevel()
    window.title("Cart Manager")
    window.geometry("500x450")

    tk.Label(window, text="Enter Product ID").pack(pady=5)
    pid_entry = tk.Entry(window)
    pid_entry.pack()

    cart_listbox = tk.Listbox(window, width=60)
    cart_listbox.pack(pady=10)

    total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 12, "bold"))
    total_label.pack(pady=5)

    def refresh_cart():
        cart_listbox.delete(0, tk.END)
        total = 0
        products = get_all_products()
        cart = get_cart()

        for pid, qty in cart.items():
            prod = products.get(pid)
            if prod:
                price = prod["price"] * qty
                total += price
                cart_listbox.insert(tk.END, f"{pid}: {prod['name']} x{qty} - ksh{price:.2f}")
            else:
                cart_listbox.insert(tk.END, f"{pid}: [Unknown Product] x{qty}")
        total_label.config(text=f"Total: ksh{total:.2f}")

    def handle_add():
        pid = pid_entry.get().strip()
        if pid in get_all_products():
            add_to_cart(pid)
            pid_entry.delete(0, tk.END)
            refresh_cart()
        else:
            messagebox.showerror("Not Found", "Product ID not found.")

    def handle_undo():
        if undo_last():
            refresh_cart()
        else:
            messagebox.showinfo("Undo", "Nothing to undo.")

    def handle_remove():
        selection = cart_listbox.curselection()
        if selection:
            selected = cart_listbox.get(selection[0])
            pid = selected.split(":")[0]
            remove_cart_item(pid)
            refresh_cart()
        else:
            messagebox.showinfo("No Selection", "Select an item to remove.")

    tk.Button(window, text="Add to Cart", command=handle_add).pack(pady=5)
    tk.Button(window, text="Undo Last", command=handle_undo).pack(pady=5)
    tk.Button(window, text="Remove Selected", command=handle_remove).pack(pady=5)

    refresh_cart()
