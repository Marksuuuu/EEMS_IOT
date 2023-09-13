import tkinter as tk

class CustomTable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.headers = ["Name", "Age", "Button"]
        self.create_widgets()

    def create_widgets(self):
        # Create a canvas for the scrollable area
        canvas = tk.Canvas(self, height=200)  # Adjust the height as needed
        canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Connect the canvas to the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the table
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Insert sample data
        for i in range(1, 12):
            name = f"Person {i}"
            age = 25 + i
            button_text = f"Ticket {i}"

            # Create frame for each row
            row_frame = tk.Frame(frame)
            row_frame.pack(side="top", fill="x", padx=5, pady=5)

            # Display data in labels
            tk.Label(row_frame, text=name).pack(side="left", padx=5, pady=5, fill="x")
            tk.Label(row_frame, text=str(age)).pack(side="left", padx=5, pady=5, fill="x")

            # Create button-like label for the button column
            button_label = tk.Label(row_frame, text=button_text, relief="raised", padx=10, pady=5)
            button_label.pack(side="left", padx=5, pady=5)
            button_label.bind("<ButtonRelease-1>", lambda event, values=(name, age, button_text): self.on_button_click(values))
            button_label.bind("<Enter>", self.on_button_hover_enter)
            button_label.bind("<Leave>", self.on_button_hover_leave)
            button_label.config(bg="white")

        # Bind the canvas to update scroll region when the frame size changes
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_button_click(self, values):
        print(f"Button clicked for row: {values}")

    def on_button_hover_enter(self, event):
        event.widget.configure(background="lightgray")

    def on_button_hover_leave(self, event):
        event.widget.configure(background="white")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Table with Buttons")

    custom_table = CustomTable(root)
    custom_table.pack(expand=True, fill="both")

    root.mainloop()
