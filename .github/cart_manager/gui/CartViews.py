import tkinter as tk
from tkinter import ttk, messagebox
from ..data_structures.DoublyLinkedList import DoublyLinkedList
from ..data_structures.PriorityQueue import PriorityQueue


class QuantityDialog:
    def __init__(self, parent, title, current_qty):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.result = None

        ttk.Label(self.top, text="New Quantity:").pack()
        self.entry = ttk.Entry(self.top)
        self.entry.insert(0, str(current_qty))
        self.entry.pack()

        ttk.Button(self.top, text="OK", command=self._on_ok).pack()

    def _on_ok(self):
        try:
            self.result = int(self.entry.get())
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

class CartManager:
    def __init__(self, parent, db_ops, cart_list, priority_queue):
        self.parent = parent
        self.db_ops = db_ops
        self.cart_list = cart_list
        self.priority_queue = priority_queue

        self._setup_ui()
        self._load_cart()

    def _setup_ui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Treeview for cart items
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Name', 'Price', 'Quantity', 'Total'),
                                 show='headings', selectmode='browse')

        # Configure columns
        self.tree.heading('ID', text='Product ID', anchor=tk.W)
        self.tree.heading('Name', text='Name', anchor=tk.W)
        self.tree.heading('Price', text='Price', anchor=tk.W)
        self.tree.heading('Quantity', text='Quantity', anchor=tk.W)
        self.tree.heading('Total', text='Total', anchor=tk.W)

        self.tree.column('ID', width=80, minwidth=80)
        self.tree.column('Name', width=150, minwidth=150)
        self.tree.column('Price', width=80, minwidth=80)
        self.tree.column('Quantity', width=80, minwidth=80)
        self.tree.column('Total', width=80, minwidth=80)

        self.tree.pack(expand=True, fill='both')

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Summary frame
        summary_frame = ttk.Frame(self.main_frame)
        summary_frame.pack(fill=tk.X, pady=5)

        self.total_label = ttk.Label(summary_frame, text="Total: $0.00", font=('Arial', 10, 'bold'))
        self.total_label.pack(side=tk.RIGHT, padx=10)

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="Add to Cart", command=self._add_to_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove from Cart", command=self._remove_from_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Quantity", command=self._update_quantity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Cart", command=self._clear_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Checkout", command=self._checkout).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self._load_cart).pack(side=tk.RIGHT, padx=5)

    def _load_cart(self):
        """Load cart items from database into the treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get cart items from database
        cart_items = self.db_ops.get_cart_items()

        # Calculate total
        total = 0.0

        # Insert into treeview and update linked list
        self.cart_list = DoublyLinkedList()  # Reset the list

        for item in cart_items:
            self.tree.insert('', 'end', values=(
                item['product_id'],
                item['name'],
                f"${item['price']:.2f}",
                item['quantity'],
                f"${item['price'] * item['quantity']:.2f}"
            ))
            self.cart_list.insert_at_tail(item)
            total += item['price'] * item['quantity']

        # Update total label
        self.total_label.config(text=f"Total: ${total:.2f}")

    def _add_to_cart(self):
        """Open dialog to add product to cart"""
        dialog = AddToCartDialog(self.parent, self.db_ops)
        self.parent.wait_window(dialog.top)
        self._load_cart()

    def _remove_from_cart(self):
        """Remove selected item from cart"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to remove")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]

        if messagebox.askyesno("Confirm Remove", "Remove this item from cart?"):
            success = self.db_ops.remove_from_cart(product_id)
            if success:
                # Update linked list
                self.cart_list.delete({'product_id': product_id})
                messagebox.showinfo("Success", "Item removed from cart")
                self._load_cart()
            else:
                messagebox.showerror("Error", "Failed to remove item from cart")

    def _update_quantity(self):
        """Update quantity of selected cart item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an item to update")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        current_qty = item['values'][3]

        dialog = QuantityDialog(self.parent, "Update Quantity", current_qty)
        self.parent.wait_window(dialog.top)

        if dialog.result:
            new_qty = dialog.result
            if new_qty <= 0:
                messagebox.showwarning("Invalid Quantity", "Quantity must be positive")
                return

            # Calculate difference to add/remove
            difference = new_qty - current_qty

            if difference > 0:
                self.db_ops.add_to_cart(product_id, difference)
            else:
                self.db_ops.remove_from_cart(product_id, abs(difference))

            self._load_cart()

    def _clear_cart(self):
        """Clear all items from cart"""
        if messagebox.askyesno("Confirm Clear", "Clear all items from cart?"):
            self.db_ops.clear_cart()
            self.cart_list = DoublyLinkedList()  # Reset the list
            self._load_cart()

    def _checkout(self):
        """Process checkout"""
        cart_items = self.db_ops.get_cart_items()
        if not cart_items:
            messagebox.showwarning("Empty Cart", "Your cart is empty")
            return

        total = sum(item['price'] * item['quantity'] for item in cart_items)

        # Check stock availability
        for item in cart_items:
            product = self.db_ops.get_product(item['product_id'])
            if product['stock'] < item['quantity']:
                messagebox.showerror("Stock Issue",
                                     f"Not enough stock for {product['name']}. Available: {product['stock']}")
                return

        # Process checkout (in a real app, this would involve payment processing)
        if messagebox.askyesno("Confirm Checkout", f"Total: ${total:.2f}\nProceed with checkout?"):
            # Update stock levels
            for item in cart_items:
                product = self.db_ops.get_product(item['product_id'])
                new_stock = product['stock'] - item['quantity']
                self.db_ops.update_product(product['id'], {'stock': new_stock})

            # Clear cart
            self.db_ops.clear_cart()
            self.cart_list = DoublyLinkedList()

            messagebox.showinfo("Success", "Checkout completed successfully!")
            self._load_cart()


class AddToCartDialog:
    def __init__(self, parent, db_ops):
        self.top = tk.Toplevel(parent)
        self.top.title("Add to Cart")
        self.db_ops = db_ops
        self.result = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup the dialog UI"""
        main_frame = ttk.Frame(self.top)
        main_frame.pack(padx=10, pady=10)