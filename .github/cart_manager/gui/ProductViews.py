import tkinter as tk
from tkinter import ttk, messagebox
from ..data_structures.HashTable import HashTable
from ..data_structures.BinarySearchTree import BinarySearchTree


class ProductManager:
    def __init__(self, parent, db_ops, product_hash, category_tree):
        self.parent = parent
        self.db_ops = db_ops
        self.product_hash = product_hash
        self.category_tree = category_tree

        self._setup_ui()
        self._load_products()

    def _setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.search_entry.bind('<KeyRelease>', self._on_search)

        # Treeview for products
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Name', 'Category', 'Price', 'Stock'),
                                 show='headings', selectmode='browse')

        # Configure columns
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('Name', text='Name', anchor=tk.W)
        self.tree.heading('Category', text='Category', anchor=tk.W)
        self.tree.heading('Price', text='Price', anchor=tk.W)
        self.tree.heading('Stock', text='Stock', anchor=tk.W)

        self.tree.column('ID', width=50, minwidth=50)
        self.tree.column('Name', width=150, minwidth=150)
        self.tree.column('Category', width=100, minwidth=100)
        self.tree.column('Price', width=80, minwidth=80)
        self.tree.column('Stock', width=60, minwidth=60)

        self.tree.pack(expand=True, fill='both')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Add Product", command=self._add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Product", command=self._edit_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Product", command=self._delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self._load_products).pack(side=tk.RIGHT, padx=5)

    def _load_products(self):
        """Load products from database into the treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get products from database
        products = self.db_ops.get_all_products()

        # Insert into treeview
        for product in products:
            self.tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                f"${product['price']:.2f}",
                product['stock']
            ))

    def _on_search(self, event=None):
        """Handle search functionality"""
        query = self.search_entry.get().lower()

        if not query:
            self._load_products()
            return

        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Search in hash table (could also search in BST by category)
        products = self.db_ops.get_all_products()
        for product in products:
            if (query in str(product['id']).lower() or
                    query in product['name'].lower() or
                    (product['category'] and query in product['category'].lower())):
                self.tree.insert('', 'end', values=(
                    product['id'],
                    product['name'],
                    product['category'],
                    f"${product['price']:.2f}",
                    product['stock']
                ))

    def _add_product(self):
        """Open add product dialog"""
        dialog = ProductDialog(self.parent, "Add Product", self.db_ops,
                               self.product_hash, self.category_tree)
        self.parent.wait_window(dialog.top)
        self._load_products()

    def _edit_product(self):
        """Open edit product dialog"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to edit")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]

        product = self.db_ops.get_product(product_id)
        if not product:
            messagebox.showerror("Error", "Product not found")
            return

        dialog = ProductDialog(self.parent, "Edit Product", self.db_ops,
                               self.product_hash, self.category_tree, product)
        self.parent.wait_window(dialog.top)
        self._load_products()

    def _delete_product(self):
        """Delete selected product"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a product to delete")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            success = self.db_ops.delete_product(product_id)
            if success:
                # Remove from data structures
                self.product_hash.delete(product_id)
                # Note: Priority queue and BST would need special handling
                messagebox.showinfo("Success", "Product deleted successfully")
                self._load_products()
            else:
                messagebox.showerror("Error", "Failed to delete product")


class ProductDialog:
    def __init__(self, parent, title, db_ops, product_hash, category_tree, product=None):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.db_ops = db_ops
        self.product_hash = product_hash
        self.category_tree = category_tree
        self.product = product

        self._setup_ui()

    def _setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.top)
        main_frame.pack(padx=10, pady=10)

        # Form fields
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.category_entry = ttk.Entry(main_frame, width=30)
        self.category_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="Price:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.price_entry = ttk.Entry(main_frame, width=30)
        self.price_entry.grid(row=2, column=1, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="Stock:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.stock_entry = ttk.Entry(main_frame, width=30)
        self.stock_entry.grid(row=3, column=1, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="Priority (1-5):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.priority_combobox = ttk.Combobox(main_frame, values=[1, 2, 3, 4, 5], width=27)
        self.priority_combobox.grid(row=4, column=1, sticky=tk.EW, pady=2)
        self.priority_combobox.set(3)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self._save_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT, padx=5)

        # If editing, populate fields
        if self.product:
            self.name_entry.insert(0, self.product['name'])
            if self.product['category']:
                self.category_entry.insert(0, self.product['category'])
            self.price_entry.insert(0, str(self.product['price']))
            self.stock_entry.insert(0, str(self.product['stock']))
            self.priority_combobox.set(self.product['priority'])

    def _save_product(self):
        """Save product to database and data structures"""
        try:
            product_data = {
                'name': self.name_entry.get(),
                'category': self.category_entry.get(),
                'price': float(self.price_entry.get()),
                'stock': int(self.stock_entry.get()),
                'priority': int(self.priority_combobox.get())
            }

            if not product_data['name']:
                messagebox.showwarning("Validation Error", "Product name is required")
                return

            if self.product:
                # Update existing product
                success = self.db_ops.update_product(self.product['id'], product_data)
                if success:
                    # Update hash table
                    updated_product = self.db_ops.get_product(self.product['id'])
                    self.product_hash.insert(updated_product['id'], updated_product)

                    # Note: Would need to update priority queue and BST as well
                    messagebox.showinfo("Success", "Product updated successfully")
                    self.top.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update product")
            else:
                # Add new product
                product_id = self.db_ops.add_product(product_data)
                if product_id:
                    # Add to data structures
                    new_product = self.db_ops.get_product(product_id)
                    self.product_hash.insert(product_id, new_product)
                    self.category_tree.insert(new_product['category'], new_product)
                    messagebox.showinfo("Success", "Product added successfully")
                    self.top.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add product")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")