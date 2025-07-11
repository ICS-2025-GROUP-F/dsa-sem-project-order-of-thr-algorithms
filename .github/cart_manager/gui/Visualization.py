import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from math import sqrt


class DataStructureVisualizer:
    def __init__(self, parent, hash_table, linked_list, priority_queue, bst):
        self.parent = parent
        self.hash_table = hash_table
        self.linked_list = linked_list
        self.priority_queue = priority_queue
        self.bst = bst

        self.canvas = tk.Canvas(parent, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.draw_button = ttk.Button(parent, text="Refresh Visualization", command=self.draw_all)
        self.draw_button.pack(pady=10)

        self.font = tkfont.Font(family='Consolas', size=10)
        self.draw_all()

    def draw_all(self):
        """Draw all data structures on the canvas"""
        self.canvas.delete("all")
        self.draw_hash_table(50, 50)
        self.draw_linked_list(50, 200)
        self.draw_priority_queue(400, 50)
        self.draw_bst(400, 200)

    def draw_hash_table(self, x, y):
        """Visualize hash table with buckets and chains"""
        self.canvas.create_text(x, y - 20, text="Hash Table", anchor='w', font=self.font)

        bucket_width = 60
        bucket_height = 30
        item_radius = 12

        for i in range(len(self.hash_table.table)):
            # Draw bucket
            bucket_x = x + i * (bucket_width + 10)
            self.canvas.create_rectangle(
                bucket_x, y,
                bucket_x + bucket_width, y + bucket_height,
                outline='blue'
            )
            self.canvas.create_text(
                bucket_x + bucket_width / 2, y + bucket_height / 2,
                text=f"Bucket {i}", font=self.font
            )


            chain_y = y + bucket_height + 10
            for j, (key, value) in enumerate(self.hash_table.table[i]):
                item_x = bucket_x + bucket_width / 2
                self.canvas.create_oval(
                    item_x - item_radius, chain_y - item_radius,
                    item_x + item_radius, chain_y + item_radius,
                    fill='lightblue', outline='blue'
                )
                self.canvas.create_text(
                    item_x, chain_y,
                    text=str(key), font=self.font
                )


                if j < len(self.hash_table.table[i]) - 1:
                    self.canvas.create_line(
                        item_x, chain_y + item_radius,
                        item_x, chain_y + item_radius + 15,
                        arrow=tk.LAST, width=2
                    )

                chain_y += 40

    def draw_linked_list(self, x, y):
        """Visualize doubly linked list with nodes and pointers"""
        self.canvas.create_text(x, y - 20, text="Doubly Linked List", anchor='w', font=self.font)

        node_width = 60
        node_height = 40
        radius = 15

        current = self.linked_list.head
        pos_x = x

        while current:

            self.canvas.create_rectangle(
                pos_x, y,
                pos_x + node_width, y + node_height,
                fill='lightgreen', outline='green'
            )
            self.canvas.create_text(
                pos_x + node_width / 2, y + node_height / 2,
                text=str(current.data), font=self.font
            )


            if current.next:
                self.canvas.create_line(
                    pos_x + node_width, y + node_height / 2,
                    pos_x + node_width + 30, y + node_height / 2,
                    arrow=tk.LAST, width=2
                )


            if current.prev:
                self.canvas.create_line(
                    pos_x, y + node_height / 2,
                           pos_x - 30, y + node_height / 2,
                    arrow=tk.LAST, width=2
                )
                self.canvas.create_text(
                    pos_x - 15, y + node_height / 2 - 15,
                    text="prev", font=self.font
                )

            pos_x += node_width + 40
            current = current.next

    def draw_priority_queue(self, x, y):
        """Visualize priority queue as a binary heap"""
        self.canvas.create_text(x, y - 20, text="Priority Queue", anchor='w', font=self.font)

        if not hasattr(self.priority_queue, '_queue'):
            return

        items = [item[-1] for item in sorted(self.priority_queue._queue, key=lambda x: (-x[0], x[1]))]

        node_radius = 20
        level_height = 70
        max_width = 200

        for i, item in enumerate(items):
            if i >= 7:
                break

            level = int(sqrt(i + 1))
            nodes_in_level = 2 ** level
            x_offset = max_width * (i - (2 ** level - 1) + 0.5) / nodes_in_level

            node_x = x + x_offset
            node_y = y + level * level_height

            self.canvas.create_oval(
                node_x - node_radius, node_y - node_radius,
                node_x + node_radius, node_y + node_radius,
                fill='lightcoral', outline='red'
            )
            self.canvas.create_text(
                node_x, node_y,
                text=f"P:{item.priority if hasattr(item, 'priority') else 'N/A'}",
                font=self.font
            )


            left_child = 2 * i + 1
            if left_child < len(items):
                child_x = x + max_width * (left_child - (2 ** (level + 1) - 1) + 0.5) / (2 ** (level + 1))
                child_y = y + (level + 1) * level_height
                self.canvas.create_line(
                    node_x, node_y + node_radius,
                    child_x, child_y - node_radius,
                    width=2
                )

    def draw_bst(self, x, y):

        self.canvas.create_text(x, y - 20, text="Binary Search Tree", anchor='w', font=self.font)

        node_radius = 20
        level_height = 60

        def draw_node(node, x, y, x_offset):
            if not node:
                return

            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill='lightyellow', outline='orange'
            )
            self.canvas.create_text(
                x, y,
                text=str(node.key), font=self.font
            )

            if node.left:
                new_x = x - x_offset
                self.canvas.create_line(
                    x, y + node_radius,
                    new_x, y + level_height - node_radius,
                    width=2
                )
                draw_node(node.left, new_x, y + level_height, x_offset / 2)

            if node.right:
                new_x = x + x_offset
                self.canvas.create_line(
                    x, y + node_radius,
                    new_x, y + level_height - node_radius,
                    width=2
                )
                draw_node(node.right, new_x, y + level_height, x_offset / 2)

        if self.bst.root:
            draw_node(self.bst.root, x + 150, y, 75)