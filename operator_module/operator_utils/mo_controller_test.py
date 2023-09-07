import tkinter as tk
import os
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage



class MoDetailsTest:
    def __init__(
            self,
            root,
            extracted_fullname,
            extracted_employee_no,
            extracted_photo_url,
            extracted_username,
            data,
            update_table_function,
            assets_dir
            ):
        
        self.root = root
        self.assets_dir = assets_dir
        self.root.geometry("933x563")
        self.root.configure(bg="#FFFFFF")
        self.center_window()
        # self.root.overrideredirect(True)

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=563,
            width=933,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            243.0,
            68.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            104.0,
            37.0,
            anchor="nw",
            text="MO1234567",
            fill="#FFFFFF",
            font=("ArialMT", 48 * -1)
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            556.0,
            68.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            465.0,
            265.0,
            image=self.image_image_3
        )

        self.canvas.create_text(
            597.0,
            57.0,
            anchor="nw",
            text="Alex Fernan F. Mercado",
            fill="#343A40",
            font=("Roboto Bold", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.root,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=712.0,
            y=468.0,
            width=172.0,
            height=58.0
        )

        self.canvas.create_text(
            66.0,
            147.0,
            anchor="nw",
            text="Main Operation",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            64.0,
            173.0,
            anchor="nw",
            text="Wirebond/3RD Opt. Insp.",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            68.0,
            267.0,
            anchor="nw",
            text="Device",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            66.0,
            295.0,
            anchor="nw",
            text="PM9:0001234",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            526.0,
            143.0,
            anchor="nw",
            text="Package",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            526.0,
            170.0,
            anchor="nw",
            text="SOT",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.canvas.create_text(
            528.0,
            268.06951904296875,
            anchor="nw",
            text="Customer",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            528.0,
            296.0,
            anchor="nw",
            text="TPC",
            fill="#868E96",
            font=("ArialMT", 32 * -1)
        )

        self.image_image_4 = PhotoImage(
            file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(
            163.0,
            474.0,
            image=self.image_image_4
        )

        self.canvas.create_text(
            129.0,
            434.0,
            anchor="nw",
            text="MO Qty.",
            fill="#FFFFFF",
            font=("ArialMT", 20 * -1)
        )

        self.canvas.create_text(
            64.0,
            457.0,
            anchor="nw",
            text="1234567",
            fill="#FFFFFF",
            font=("Arial BoldMT", 48 * -1)
        )

        self.image_image_5 = PhotoImage(
            file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(
            479.0,
            474.0,
            image=self.image_image_5
        )

        self.canvas.create_text(
            400.0,
            439.0,
            anchor="nw",
            text="Remaining MO Qty.",
            fill="#FFFFFF",
            font=("ArialMT", 19 * -1)
        )

        self.canvas.create_text(
            383.0,
            458.0,
            anchor="nw",
            text="1234567",
            fill="#FFFFFF",
            font=("Arial BoldMT", 48 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.root,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=712.0,
            y=467.0,
            width=172.0,
            height=58.0
        )

        # Add other widget creations here...

        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.root,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat"
        )
        self.button_3.place(
            x=884.0,
            y=0.0,
            width=49.0,
            height=37.0
        )


        self.root.resizable(False, False)
        self.root.mainloop()

    def relative_to_assets(self, filename):
        # No need to go up one directory since we changed the working directory
        full_path = os.path.join(self.assets_dir, "frame_mo_details", filename)
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


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
