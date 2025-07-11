import tkinter as tk
from tkinter import ttk, messagebox
from ..data_structures.DoublyLinkedList import DoublyLinkedList
from ..data_structures.HashTable import HashTable
from ..data_structures.PriorityQueue import PriorityQueue
from ..data_structures.BinarySearchTree import BinarySearchTree
from .ProductViews import ProductManager
from .CartViews import CartManager
from .Visualization import DataStructureVisualizer
from ..database.DBOperations import DBOperations


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cart Manager")
        self.geometry("1200x800")
        self.db_ops = DBOperations()

        # Initialize data structures
        self.product_hash = HashTable()
        self.cart_list = DoublyLinkedList()
        self.priority_queue = PriorityQueue()
        self.category_tree = BinarySearchTree()

        self._load_data_structures()

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.product_frame = ttk.Frame(self.notebook)
        self.cart_frame = ttk.Frame(self.notebook)
        self.visualization_frame = ttk.Frame(self.notebook)

        # Add tabs
        self.notebook.add(self.product_frame, text='Product Management')
        self.notebook.add(self.cart_frame, text='Cart Management')
        self.notebook.add(self.visualization_frame, text='Data Structures')

        # Initialize components
        self.product_manager = ProductManager(self.product_frame, self.db_ops,
                                              self.product_hash, self.category_tree)
        self.cart_manager = CartManager(self.cart_frame, self.db_ops,
                                        self.cart_list, self.priority_queue)
        self.visualizer = DataStructureVisualizer(self.visualization_frame,
                                                  self.product_hash,
                                                  self.cart_list,
                                                  self.priority_queue,
                                                  self.category_tree)

        # Status bar
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_data_structures(self):
        """Load data from database into our data structures"""
        products = self.db_ops.get_all_products()
        for product in products:
            # Add to hash table
            self.product_hash.insert(product['id'], product)

            # Add to priority queue
            self.priority_queue.enqueue(product, product['priority'])

            # Add to category tree
            if product['category']:
                self.category_tree.insert(product['category'], product)

        # Load cart items
        cart_items = self.db_ops.get_cart_items()
        for item in cart_items:
            self.cart_list.insert_at_tail(item)

    def _on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.after(5000, lambda: self.status_bar.config(text="Ready"))