import tkinter as tk
from tkinter import messagebox
from product_data import add_product, delete_product, get_all_products

def open_product_window():
    window = tk.Toplevel()
    window.title("Product Manager")
    window.geometry("450x400")

    # --- UI Components ---
    tk.Label(window, text="Product Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Price").grid(row=1, column=0, padx=10, pady=5)
    price_entry = tk.Entry(window)
    price_entry.grid(row=1, column=1)

    product_listbox = tk.Listbox(window, width=50)
    product_listbox.grid(row=3, column=0, columnspan=2, pady=10)

    def refresh_product_list():
        product_listbox.delete(0, tk.END)
        for pid, data in get_all_products().items():
            product_listbox.insert(tk.END, f"{pid}: {data['name']} - ${data['price']:.2f}")

    def handle_add():
        name = name_entry.get()
        try:
            price = float(price_entry.get())
            if name:
                add_product(name, price)
                name_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                refresh_product_list()
            else:
                messagebox.showwarning("Missing Info", "Enter a product name.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number.")

    def handle_delete():
        selection = product_listbox.curselection()
        if selection:
            selected = product_listbox.get(selection[0])
            pid = selected.split(":")[0]
            delete_product(pid)
            refresh_product_list()
        else:
            messagebox.showinfo("No Selection", "Select a product to delete.")

    tk.Button(window, text="Add Product", command=handle_add).grid(row=2, column=0, pady=10)
    tk.Button(window, text="Delete Selected", command=handle_delete).grid(row=2, column=1, pady=10)

    refresh_product_list()
