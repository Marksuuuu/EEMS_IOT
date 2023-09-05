import json
import os
import tkinter as tk
import tkinter.font as tkFont
from datetime import date
from datetime import datetime
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

import requests

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Facilitiestemp\Desktop\Github Desktop\EEMS_IOT\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.title("Request Ticket")
window.geometry("1145x878")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 878,
    width = 1145,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    326.0,
    20.0,
    anchor="nw",
    text="REQUEST TICKET",
    fill="#5E95FF",
    font=("Montserrat Bold", 55 * -1)
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
    x=607.0,
    y=759.0,
    width=227.0,
    height=78.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=868.0,
    y=759.0,
    width=227.0,
    height=78.0
)

canvas.create_text(
    630.0,
    152.0,
    anchor="nw",
    text="Requestor",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

canvas.create_text(
    630.0,
    194.0,
    anchor="nw",
    text="FullName",
    fill="#868E96",
    font=("Montserrat SemiBold", 34 * -1)
)

canvas.create_text(
    50.0,
    154.0,
    anchor="nw",
    text="Machine Name",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

canvas.create_text(
    50.0,
    196.0,
    anchor="nw",
    text="Machine_01",
    fill="#868E96",
    font=("Montserrat SemiBold", 34 * -1)
)

canvas.create_text(
    50.0,
    264.0,
    anchor="nw",
    text="MO Number",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

canvas.create_text(
    50.0,
    306.0,
    anchor="nw",
    text="MO1235123",
    fill="#868E96",
    font=("Montserrat SemiBold", 34 * -1)
)

canvas.create_text(
    627.0,
    264.0,
    anchor="nw",
    text="Date | Time",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

canvas.create_text(
    627.0,
    307.0,
    anchor="nw",
    text="DateTime",
    fill="#868E96",
    font=("Montserrat SemiBold", 34 * -1)
)

canvas.create_text(
    437.0,
    439.0,
    anchor="nw",
    text="Downtime Type",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

canvas.create_text(
    500.0,
    556.0,
    anchor="nw",
    text="Remarks",
    fill="#343A40",
    font=("Montserrat Bold", 31 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    572.5,
    661.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    font=("Montserrat Bold", 25 * -1),
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=58.0,
    y=605.0,
    width=1029.0,
    height=110.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    569.5,
    505.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#EFEFEF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=445.0,
    y=482.0,
    width=249.0,
    height=44.0
)
window.resizable(False, False)
window.mainloop()


