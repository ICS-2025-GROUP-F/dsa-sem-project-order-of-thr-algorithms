import tkinter as tk
from product_data import get_all_products

def open_search_window():
    window = tk.Toplevel()
    window.title("Search & Inventory")
    window.geometry("500x450")

    # --- Widgets ---
    tk.Label(window, text="Search by Product Name or ID").pack(pady=5)
    search_entry = tk.Entry(window, width=40)
    search_entry.pack()

    result_listbox = tk.Listbox(window, width=60)
    result_listbox.pack(pady=10)

    # --- Functions ---
    def search_products():
        term = search_entry.get().strip().lower()
        result_listbox.delete(0, tk.END)
        all_products = get_all_products()

        if not term:
            for pid, data in all_products.items():
                result_listbox.insert(tk.END, f"{pid}: {data['name']} - ${data['price']:.2f}")
        else:
            found = False
            for pid, data in all_products.items():
                if term in pid.lower() or term in data["name"].lower():
                    result_listbox.insert(tk.END, f"{pid}: {data['name']} - ${data['price']:.2f}")
                    found = True
            if not found:
                result_listbox.insert(tk.END, "No products found.")

    def show_all():
        search_entry.delete(0, tk.END)
        search_products()

    # --- Buttons ---
    tk.Button(window, text="Search", command=search_products).pack(pady=5)
    tk.Button(window, text="Show All", command=show_all).pack(pady=5)

    # --- Load all by default ---
    show_all()
