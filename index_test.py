import tkinter as tk
import os
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage




class App:
  def __init__(self, name, age):
      pass
  
  def make_gui(self):
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg = "#E5E5E5")


    canvas = Canvas(
        window,
        bg = "#E5E5E5",
        height = 600,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1024.0,
        100.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        31.0,
        10.0,
        282.0,
        86.97332763671875,
        fill="#D3F9D8",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        516.0,
        49.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        872.0,
        49.0,
        image=image_image_2
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        533.5,
        50.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#EFEFEF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=378.0,
        y=28.0,
        width=311.0,
        height=42.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        782.0,
        48.0,
        image=image_image_3
    )

    canvas.create_text(
        806.0,
        38.0,
        anchor="nw",
        text="28-08-23  | 11:25 :00 ",
        fill="#343A40",
        font=("Roboto Regular", 16 * -1)
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        64.0,
        47.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        64.0,
        47.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        512.0,
        259.0,
        image=image_image_6
    )

    canvas.create_text(
        97.0,
        27.0,
        anchor="nw",
        text="MACHINE",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        97.0,
        44.0,
        anchor="nw",
        text="ONLINE",
        fill="#343A40",
        font=("Roboto Medium", 24 * -1)
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        167.0,
        259.0,
        image=image_image_7
    )

    canvas.create_text(
        709.0,
        435.0,
        anchor="nw",
        text="LOGS",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    image_image_8 = PhotoImage(
        file=relative_to_assets("image_8.png"))
    image_8 = canvas.create_image(
        340.0,
        509.0,
        image=image_image_8
    )

    canvas.create_text(
        24.0,
        442.0,
        anchor="nw",
        text="MACHINE",
        fill="#343A40",
        font=("Roboto Medium", 30 * -1)
    )

    image_image_9 = PhotoImage(
        file=relative_to_assets("image_9.png"))
    image_9 = canvas.create_image(
        855.0,
        509.0,
        image=image_image_9
    )

    image_image_10 = PhotoImage(
        file=relative_to_assets("image_10.png"))
    image_10 = canvas.create_image(
        856.0,
        259.0,
        image=image_image_10
    )

    canvas.create_text(
        700.0,
        435.0,
        anchor="nw",
        text="LOGS",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        689.0,
        112.0,
        anchor="nw",
        text="QTY",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        0.0,
        112.0,
        anchor="nw",
        text="OEE",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        345.0,
        112.0,
        anchor="nw",
        text="CPK",
        fill="#343A40",
        font=("Roboto Medium", 14 * -1)
    )

    image_image_11 = PhotoImage(
        file=relative_to_assets("image_11.png"))
    image_11 = canvas.create_image(
        362.0,
        49.0,
        image=image_image_11
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=689.0,
        y=553.0725708007812,
        width=335.0,
        height=45.92742919921875
    )
  
      