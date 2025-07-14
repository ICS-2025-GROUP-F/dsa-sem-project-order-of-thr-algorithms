import tkinter as tk
from tkinter import messagebox
from checkout_data import perform_checkout, get_history
from cart_data import get_cart
from cart_data import clear_cart  # ✅ import this instead
  # needed to clear it

def open_checkout_window():
    window = tk.Toplevel()
    window.title("Checkout & History")
    window.geometry("500x500")

    # --- Checkout Section ---
    tk.Button(window, text="Checkout", command=lambda: handle_checkout()).pack(pady=10)
    total_label = tk.Label(window, text="Total: $0.00", font=("Arial", 12, "bold"))
    total_label.pack()

    # --- History Display ---
    tk.Label(window, text="Order History").pack(pady=10)
    history_listbox = tk.Listbox(window, width=60)
    history_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def handle_checkout():
        if not get_cart():
            messagebox.showinfo("Empty Cart", "Your cart is empty.")
            return
        items, total = perform_checkout()
        clear_cart()
        total_label.config(text=f"Total: ${total:.2f}")
        update_history()
        messagebox.showinfo("Checkout Complete", f"Order placed. Total: ${total:.2f}")

    def update_history():
        history_listbox.delete(0, tk.END)
        for i, order in enumerate(get_history(), 1):
            history_listbox.insert(tk.END, f"Order {i}: ${order['total']:.2f}")
            for item in order['items']:
                history_listbox.insert(tk.END, f"   - {item}")
            history_listbox.insert(tk.END, "")  # spacer

    update_history()
