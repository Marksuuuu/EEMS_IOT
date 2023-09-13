import tkinter as tk
from tkinter import ttk


def toggle_label(item_id):
    current_state = tree.item(item_id, 'values')[0]
    print(f":computer:==>> current_state: {current_state}")
    new_state = "On" if current_state == "Off" else "Off"
    tree.item(item_id, values=(new_state,))


def on_item_click(event):
    item_id = tree.identify_row(event.y)
    if item_id:
        toggle_label(item_id)

        
root = tk.Tk()
root.title("Toggleable Label in Treeview")
# Create a Treeview widget
tree = ttk.Treeview(root, columns=("State",))
tree.heading("#1", text="State")
tree.pack()
# Insert sample data with toggleable labels
items = [
    ("Item 1", "On"),
    ("Item 2", "Off"),
    ("Item 3", "On"),
    ("Item 1", "On"),
    ("Item 2", "Off"),
    ("Item 3", "On"),
    ("Item 1", "On"),
    ("Item 2", "Off"),
    ("Item 3", "On"),
]
for item in items:
    item_id = tree.insert("", "end", values=(item[1],))
    label = tk.Label(tree, text=item[0])
    label.grid(row=tree.index(item_id), column=0, padx=5, pady=2, sticky="w")
    toggle_button = tk.Button(tree, text="Toggle", command=lambda : toggle_label(item_id))
    toggle_button.grid(row=tree.index(item_id), column=1, padx=5, pady=2, sticky="e")
# Bind a click event to toggle the label
tree.bind("<Button-1>", on_item_click)
root.mainloop()