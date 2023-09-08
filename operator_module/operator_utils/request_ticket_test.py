import tkinter as tk
import os
from pathlib import Path
from PIL import Image, ImageTk
import json
import tkinter.font as tkFont
from datetime import date
from datetime import datetime
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

import requests


class RequestTicketTest:
    def __init__(self, root, extracted_fullname, extracted_employee_no, assets_dir):
        self.root = root
        root.title("Ticket Request")
        self.assets_dir = assets_dir
        self.root.geometry("933x563")
        self.root.configure(bg="#FFFFFF")
        # self.root.overrideredirect(True)

        self.fullname = extracted_fullname
        self.employee_no = extracted_employee_no

        now = datetime.now()
        today = date.today()
        self.current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        self.dropdown_var = tk.StringVar()

        self.fetch_downtime_types()

        # self.button_1 = tk.Button(
        #     self.root,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=self.close_window(),
        #     relief="flat"
        # )
        # self.button_1.place(x=506.0, y=454.0, width=172.0, height=59.0)

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
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(
            198.0,
            17.0,
            anchor="nw",
            text="REQUEST TICKET",
            fill="#5E95FF",
            font=("Arial BoldMT", 48 * -1),
        )

        self.button_1 = tk.Button(
            self.root,
            image=self.tk_btn_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.close_window,
            relief="flat",
        )
        self.button_1.place(x=506.0, y=454.0, width=172.0, height=59.0)

        self.button_2 = tk.Button(
            self.root,
            image=self.tk_btn_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit,
            relief="flat",
        )
        self.button_2.place(x=712.0, y=454.0, width=172.0, height=59.0)

        self.canvas.create_text(
            52.0,
            98.0,
            anchor="nw",
            text="Machine Name",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        self.canvas.create_text(
            50.0,
            124.0,
            anchor="nw",
            text=self.load_machno(),
            fill="#868E96",
            font=("ArialMT", 32 * -1),
        )

        self.canvas.create_text(
            52.0,
            178.0,
            anchor="nw",
            text="MO Number",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        self.canvas.create_text(
            50.0,
            206.0,
            anchor="nw",
            text="MO_01",
            fill="#868E96",
            font=("ArialMT", 32 * -1),
        )

        self.canvas.create_text(
            530.0,
            93.0,
            anchor="nw",
            text="Requestor",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        self.canvas.create_text(
            530.0,
            119.93170166015625,
            anchor="nw",
            text=self.fullname,
            fill="#868E96",
            font=("ArialMT", 32 * -1),
        )

        self.canvas.create_text(
            530.0,
            178.06951904296875,
            anchor="nw",
            text="Date | Time",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        self.canvas.create_text(
            530.0,
            205.64239501953125,
            anchor="nw",
            text=self.current_date_time,
            fill="#868E96",
            font=("ArialMT", 32 * -1),
        )

        self.canvas.create_text(
            50.0,
            264.0,
            anchor="nw",
            text="Downtime Type",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        # Adjust  the font of the text inside the dropdown 
        root.option_add("*TCombobox*Listbox.font", ("Arial BoldMT", 20))

        dropdown = ttk.Combobox(root, textvariable=self.dropdown_var, state="readonly")
        dropdown["values"] = [item["DOWNTIME_TYPE"] for item in self.downtime_data]
        dropdown.bind("<<ComboboxSelected>>", self.on_select)
        dropdown.place(x=58.0, y=293.0, width=212.0, height=34.0)
        dropdown.config(font=("Arial BoldMT", 20))

        self.canvas.create_text(
            50.0,
            344.0,
            anchor="nw",
            text="Remarks",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1),
        )

        self.entry_bg_1 = self.canvas.create_image(468.5, 402.0, image=self.tk_entry_1)
        self.entry_1 = tk.Entry(
            self.root, bd=0, bg="#EFEFEF", fg="#000716", highlightthickness=0, font=("Helvetica", 30)
        )
        self.entry_1.place(x=60.0, y=373.0, width=817.0, height=56.0)


        self.canvas.create_rectangle(
            961.0, 154.0, 1061.0, 254.0, fill="#000000", outline=""
        )

        self.button_image_3 = tk.PhotoImage(
            file=self.relative_to_assets("button_3.png")
        )
        self.button_3 = tk.Button(
            self.root,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat",
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

    def load_machno(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "../../data", "main.json"
        )

        with open(log_file_path, "r") as json_file:
            get_machno = json.load(json_file)["machno"]

        return get_machno

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def fetch_downtime_types(self):
        cmms_url = "http://cmms.teamglac.com/main_downtime_type.php"
        response = requests.get(cmms_url)
        data = response.json()
        self.downtime_data = data["result"]

    def on_select(self, event):
        selected_text = self.dropdown_var.get()
        selected_id = None
        for item in self.downtime_data:
            if item["DOWNTIME_TYPE"] == selected_text:
                selected_id = item["ID"]
                break

        if selected_id is not None:
            print("Selected ID:", selected_id)
            print("Selected Text:", selected_text)

    def collect_and_print_values(self):
        employee_no = self.employee_no
        machine_no_value = self.load_machno()
        downtime_type_id = self.get_selected_downtime_type_id()
        print(f"==>> downtime_type_id: {downtime_type_id}")
        checkbox_value = 0
        remarks_value = self.entry_1.get()
        print('remarks_value: ', remarks_value)

        # Load existing JSON data if the file exists, or create an empty list
        file_path = "data/logs/ticket_logs.json"
        existing_data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as json_file:
                    existing_data = json.load(json_file)
            except json.decoder.JSONDecodeError as e:
                print("Error loading JSON:", e)
                existing_data = []

        # Create a new entry dictionary
        new_entry = {
            "employee_no": employee_no,
            "machine_no_value": machine_no_value,
            "downtime_type_id": downtime_type_id,
            "checkbox_value": checkbox_value,
            "remarks_value": remarks_value,
        }

        # Add the new entry to the existing data
        existing_data.append(new_entry)

        # Save the updated JSON data to the file
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

        # Your existing code for sending the HTTP request and displaying messages
        url = f'http://lams.teamglac.com/lams/api/job_order/create_jo.php?params=["{machine_no_value}","{downtime_type_id}","{remarks_value}","{employee_no}","{checkbox_value}"]'
        r = requests.post(url)

        if r.status_code == 200:
            value_url = r.json()
            print(f"==>> value_url: {value_url}")
            if value_url["status"] == "meron":
                dtno_value = value_url["dtno"]
                showinfo("warning", f"Already have ticket . \nDTNO {dtno_value}")
            else:
                dtno_value = value_url["dtno"]
                showinfo(
                    "Success", f"Job order created successfully. \nDTNO {dtno_value}"
                )
            print(value_url["dtno"])
        else:
            showerror("Error", "Error in creating job order.")

    def get_selected_downtime_type_id(self):
        selected_text = self.dropdown_var.get()
        selected_id = None
        for item in self.downtime_data:
            if item["DOWNTIME_TYPE"] == selected_text:
                selected_id = item["ID"]
                break
        return selected_id

    def submit(self):
        print("Submit")
        self.collect_and_print_values()

    def close_window(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketRequestApp(root)
    root.mainloop()