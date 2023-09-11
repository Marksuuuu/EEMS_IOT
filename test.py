import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.widgets()

    def widgets(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.label = tk.Label(self.master, text="Label")
        self.label.grid(row=0, column=0, sticky="nsew")

        self.button1 = tk.Button(self.master, text="Button 1")
        self.button1.grid(row=0, column=1, sticky="nsew")

        self.button2 = tk.Button(self.master, text="Button 2")
        self.button2.grid(row=1, column=0, sticky="nsew")

        self.canvas = tk.Canvas(self.master, bg="red")
        self.canvas.grid(row=1, column=1, sticky="nsew")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
