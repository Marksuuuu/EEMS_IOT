import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
from pathlib import Path

class RequestTicket:
    def __init__(self, root, extracted_fullname, extracted_employee_no):
        self.root = root
        self.root.geometry("1145x878")
        self.root.configure(bg="#FFFFFF")

        self.canvas = self.create_canvas()

        # Create buttons
        self.button_1, self.button_image_1 = self.create_button("button_1.png", self.button_1_click)
        self.button_2, self.button_image_2 = self.create_button("button_2.png", self.button_2_click)
        self.button_1.place(x=607.0, y=759.0, width=227.0, height=78.0)
        self.button_2.place(x=868.0, y=759.0, width=227.0, height=78.0)

        # Create text elements
        self.create_text(326.0, 20.0, "REQUEST TICKET", font=("Montserrat Bold", 55 * -1), fill="#5E95FF")
        self.create_text(630.0, 152.0, "Requestor", font=("Montserrat Bold", 31 * -1), fill="#343A40")
        self.create_text(630.0, 194.0, "FullName", font=("Montserrat SemiBold", 34 * -1), fill="#868E96")
        self.create_text(50.0, 154.0, "Machine Name", font=("Montserrat Bold", 31 * -1), fill="#343A40")
        self.create_text(50.0, 196.0, "Machine_01", font=("Montserrat SemiBold", 34 * -1), fill="#868E96")
        self.create_text(50.0, 264.0, "MO Number", font=("Montserrat Bold", 31 * -1), fill="#343A40")
        self.create_text(50.0, 306.0, "MO1235123", font=("Montserrat SemiBold", 34 * -1), fill="#868E96")
        self.create_text(627.0, 264.0, "Date | Time", font=("Montserrat Bold", 31 * -1), fill="#343A40")
        self.create_text(627.0, 307.0, "DateTime", font=("Montserrat SemiBold", 34 * -1), fill="#868E96")
        self.create_text(437.0, 439.0, "Downtime Type", font=("Montserrat Bold", 31 * -1), fill="#343A40")
        self.create_text(500.0, 556.0, "Remarks", font=("Montserrat Bold", 31 * -1), fill="#343A40")

        # Create entry fields
        self.entry_1 = self.create_entry(572.5, 661.0, 1029.0, 110.0)
        self.entry_2 = self.create_entry(569.5, 505.0, 249.0, 44.0)

        self.root.resizable(False, False)

        self.fullname = extracted_fullname
        print('self.fullname: ', self.fullname)
        
        self.employee_no = extracted_employee_no
        print('self.employee_no: ', self.employee_no)

    def create_canvas(self):
        canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=878,
            width=1145,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        return canvas

    def create_button(self, image_path, command):
        button_image = PhotoImage(file=self.relative_to_assets(image_path))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        return button, button_image

    def create_text(self, x, y, text, font=("Montserrat Bold", 31 * -1), fill="#343A40"):
        self.canvas.create_text(
            x,
            y,
            anchor="nw",
            text=text,
            fill=fill,
            font=font
        )

    def create_entry(self, x, y, width, height, bg="#EFEFEF", fg="#000716"):
        entry_image = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        entry_bg = self.canvas.create_image(
            x,
            y,
            image=entry_image
        )
        entry = Entry(
            bd=0,
            bg=bg,
            fg=fg,
            highlightthickness=0
        )
        entry.place(
            x=x - width / 2,
            y=y - height / 2,
            width=width,
            height=height
        )
        return entry

    def button_1_click(self):
        print("button_1 clicked")

    def button_2_click(self):
        print("button_2 clicked")

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Facilitiestemp\Desktop\Github Desktop\EEMS_IOT\assets\frame0")
        return ASSETS_PATH / Path(path)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RequestTicket(root, "John Doe", "123456")
    app.run()
