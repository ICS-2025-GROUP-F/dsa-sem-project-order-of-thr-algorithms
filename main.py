import tkinter as tk
from db import initialize_database
from product_window import open_product_window
from cart_window import open_cart_window
from search_window import open_search_window
from checkout_window import open_checkout_window

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple E-Commerce UI")
        self.geometry("600x400")
        initialize_database()
        self.init_ui()

    def init_ui(self):
        tk.Label(self, text="E-Commerce System", font=("Arial", 18, "bold")).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Product Manager", width=20, command=open_product_window).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Cart Manager", width=20, command=open_cart_window).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Search & Inventory", width=20, command=open_search_window).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Checkout & History", width=20, command=open_checkout_window).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="v1.0 | Developed with Tkinter", font=("Arial", 10)).pack(side=tk.BOTTOM, pady=10)

if __name__ == "__main__":
    MainWindow().mainloop()
