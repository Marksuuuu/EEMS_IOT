import tkinter as tk
import os
from pathlib import Path
from PIL import Image, ImageTk


class TicketRequestApp:
    def __init__(self, root, extracted_fullname, extracted_employee_no, assets_dir):
        self.root = root
        self.assets_dir = assets_dir
        self.root.geometry("933x563")
        self.root.configure(bg="#FFFFFF")
        # self.root.overrideredirect(True)

        self.button_1 = tk.Button(
            self.root,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1_click,
            relief="flat"
        )
        self.button_1.place(x=506.0, y=454.0, width=172.0, height=59.0)

        button1 = "assets\\frame_ticket\\button_1.png"
        button2 = "assets\\frame_ticket\\button_2.png"
        entry1 = "assets\\frame_ticket\\entry_1.png"

        button1_pill = Image.open(button1)
        button2_pill = Image.open(button2)
        entry1_pill = Image.open(entry1)
        self.tk_btn_1 = ImageTk.PhotoImage(button1_pill)
        self.tk_btn_2 = ImageTk.PhotoImage(button2_pill)
        self.tk_entry_1 = ImageTk.PhotoImage(entry1_pill)
        # self.button_1.config(image=tk_image)
        # self.button_1.image = tk_image

        self.canvas = tk.Canvas(
            self.root,
            bg="#FFFFFF",
            height=563,
            width=933,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            198.0,
            17.0,
            anchor="nw",
            text="REQUEST TICKET",
            fill="#5E95FF",
            font=("Arial BoldMT", 48 * -1)
        )

        self.button_1 = tk.Button(
            self.root,
            image=self.tk_btn_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1_click,
            relief="flat"
        )
        self.button_1.place(x=506.0, y=454.0, width=172.0, height=59.0)

        self.button_2 = tk.Button(
            self.root,
            image=self.tk_btn_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_2_click,
            relief="flat"
        )
        self.button_2.place(x=712.0, y=454.0, width=172.0, height=59.0)

        self.canvas.create_text(
            52.0,
            98.0,
            anchor="nw",
            text="Machine Name",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            50.0,
            124.0,
            anchor="nw",
            text="Machine_01",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            52.0,
            178.0,
            anchor="nw",
            text="MO Number",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            50.0,
            206.0,
            anchor="nw",
            text="MO1235123",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            530.0,
            93.0,
            anchor="nw",
            text="Requestor",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            530.0,
            119.93170166015625,
            anchor="nw",
            text="FullName",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            530.0,
            178.06951904296875,
            anchor="nw",
            text="Date | Time",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            530.0,
            205.64239501953125,
            anchor="nw",
            text="DateTime",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            50.0,
            264.0,
            anchor="nw",
            text="Downtime Type",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            50.0,
            344.0,
            anchor="nw",
            text="Remarks",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.entry_bg_1 = self.canvas.create_image(
            468.5, 402.0, image=self.tk_entry_1)
        self.entry_1 = tk.Entry(self.root, bd=0, bg="#EFEFEF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=60.0, y=373.0, width=817.0, height=56.0)

        self.entry_image_2 = tk.PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            164.0, 311.0, image=self.entry_image_2)
        self.entry_2 = tk.Entry(
            self.root, bd=0, bg="#EFEFEF", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=58.0, y=293.0, width=212.0, height=34.0)

        self.canvas.create_rectangle(
            961.0, 154.0, 1061.0, 254.0, fill="#000000", outline="")

        self.button_image_3 = tk.PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = tk.Button(
            self.root,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat"
        )
        self.button_3.place(x=884.0, y=0.0, width=49.0, height=37.0)

        self.center_window()
        self.root.resizable(False, False)

    def set_working_directory(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(script_dir, ".."))

    def relative_to_assets(self, filename):
        # No need to go up one directory since we changed the working directory
        full_path = os.path.join(self.assets_dir, "frame_ticket", filename)
        print(f"==>> full_path: {full_path}")
        return full_path

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def on_button_1_click(self):
        print("button_1 clicked")

    def on_button_2_click(self):
        print("button_2 clicked")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketRequestApp(root)
    root.mainloop()
