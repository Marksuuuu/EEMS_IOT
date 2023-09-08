import tkinter as tk
import os
from tkinter import Canvas, Button, PhotoImage


class TechnicianDashboard:
    def __init__(self, root, user_department, user_position, dataJson, assets_dir):

        self.root = root
        self.assets_dir = assets_dir
        self.root.geometry("1024x600")
        self.root.configure(bg="#E5E5E5")

        self.canvas = Canvas(
            root,
            bg="#E5E5E5",
            height=600,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            1024.0,
            100.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_rectangle(
            31.0,
            10.0,
            282.0,
            86.97332763671875,
            fill="#D3F9D8",
            outline=""
        )

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.image_image_2
        )

        self.canvas.create_text(
            97.0,
            27.0,
            anchor="nw",
            text="MACHINE",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1)
        )

        self.canvas.create_text(
            97.0,
            44.0,
            anchor="nw",
            text="ONLINE",
            fill="#343A40",
            font=("Roboto Medium", 24 * -1)
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
            x=872.0,
            y=119.0,
            width=122.0,
            height=42.0
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            728.0,
            48.0,
            image=self.image_image_3
        )

        self.canvas.create_rectangle(
            31.0,
            181.0,
            506.0,
            581.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_rectangle(
            522.0,
            181.0,
            994.0,
            581.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_text(
            769.0,
            39.0,
            anchor="nw",
            text="Alex Fernan F. Mercado",
            fill="#339AF0",
            font=("Roboto Bold", 20 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=326.0,
            y=115.0,
            width=372.0,
            height=51.0
        )
        self.root.resizable(False, False)
        self.root.mainloop()

    def relative_to_assets(self, filename):
        full_path = os.path.join(self.assets_dir, "frame_technician", filename)
        print(f"==>> full_path: {full_path}")
        return full_path


if __name__ == "__main__":
    root = Tk()
    app = TechnicianFrame(root)
