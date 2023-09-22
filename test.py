import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        self.open_button = tk.Button(root, text="Open New Window", command=self.open_new_window)
        self.open_button.pack()

    def open_new_window(self):
        self.root.withdraw()  # Hide the main window
        new_window = tk.Toplevel(self.root)
        NewWindow(new_window)

class NewWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("New Window")
        self.close_button = tk.Button(root, text="Close New Window", command=self.close_and_open_main)
        self.close_button.pack()

    def close_and_open_main(self):
        self.root.quit()  # Close the new window
        main_window.root.deiconify()  # Show the main window again

if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()
