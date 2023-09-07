import tkinter as tk
from pathlib import Path
from tkinter import ttk
import tkinter.font as tkFont
import requests
from datetime import datetime
from datetime import date
from tkinter.messagebox import showinfo, showerror
import json
import os
import requests


class RequestTicket:
    def __init__(self, root, extracted_fullname, extracted_employee_no):

        self.root = root
        root.title("REQUEST TICKET")
        self.root.geometry("933x563")
        self.root.configure(bg="#FFFFFF")
        # self.root.overrideredirect(True)

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

        self.fullname = extracted_fullname
        self.employee_no = extracted_employee_no

        now = datetime.now()
        today = date.today()
        self.current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        self.dropdown_var = tk.StringVar()
        self.fetch_downtime_types()
        self.checkbox_var = tk.BooleanVar()



        self.create_gui_elements()

    def create_gui_elements(self):
        self.canvas.create_text(
            198.0,
            17.0,
            anchor="nw",
            text="REQUEST TICKET",
            fill="#5E95FF",
            font=("Arial BoldMT", 48 * -1)
        )

        # ////////////////////////////////////////
        # BUTTONS

        self.btn_Submit = tk.Button(self.root)
        self.btn_Submit["bg"] = "#5fb878"
        ft = tkFont.Font(family="Times", size=13)
        self.btn_Submit["font"] = ft
        self.btn_Submit["fg"] = "#fbfbfb"
        self.btn_Submit["justify"] = "center"
        self.btn_Submit["text"] = "SUBMIT"
        self.btn_Submit.place(x=712.0, y=454.0, width=172.0, height=59.0)
        self.btn_Submit["command"] = self.submit

        self.btn_Cancel = tk.Button(self.root)
        self.btn_Cancel["bg"] = "#ff0909"
        ft = tkFont.Font(family="Times", size=13)
        self.btn_Cancel["font"] = ft
        self.btn_Cancel["fg"] = "#ffffff"
        self.btn_Cancel["justify"] = "center"
        self.btn_Cancel["text"] = "CANCEL"
        self.btn_Cancel.place(x=506.0, y=454.0, width=172.0, height=59.0)
        self.btn_Cancel["command"] = self.close_window

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
            text=self.load_machno(),
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
            text=self.fullname,
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
            text=self.current_date_time,
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


        self.le_Remarks = tk.Entry(self.root)
        self.le_Remarks["bg"] = "#ffffff"
        self.le_Remarks["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=13)
        self.le_Remarks["font"] = ft
        self.le_Remarks["fg"] = "#333333"
        self.le_Remarks["justify"] = "center"
        self.le_Remarks["text"] = "Entry"
        self.le_Remarks.delete(0, tk.END)
        self.le_Remarks.place(x=60.0, y=373.0, width=817.0, height=56.0)


        self.canvas.create_rectangle(
            961.0,
            154.0,
            1061.0,
            254.0,
            fill="#000000",
            outline=""
        )


        self.dropdown = ttk.Combobox(self.root, textvariable=self.dropdown_var, state="readonly")
        self.dropdown["values"] = [item["DOWNTIME_TYPE"]
                              for item in self.downtime_data]
        self.dropdown.bind("<<ComboboxSelected>>", self.on_select)
        self.dropdown.place(x=58.0, y=293.0, width=212.0, height=34.0)

        self.center_window()
        self.root.resizable(False, False)

        

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
            self.get_script_directory(), "../../data", "main.json")

        with open(log_file_path, "r") as json_file:
            get_machno = json.load(json_file)["machno"]

        return get_machno      


    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))
    
    def fetch_downtime_types(self):
        cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
        response = requests.get(cmms_url)
        data = response.json()
        self.downtime_data = data["result"]

    def get_selected_downtime_type_id(self):
        selected_text = self.dropdown_var.get()
        selected_id = None
        for item in self.downtime_data:
            if item['DOWNTIME_TYPE'] == selected_text:
                selected_id = item['ID']
                break
        return selected_id
    
    def on_select(self, event):
        selected_text = self.dropdown_var.get()
        selected_id = None
        for item in self.downtime_data:
            if item['DOWNTIME_TYPE'] == selected_text:
                selected_id = item['ID']
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
        remarks_value = self.le_Remarks.get()

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
            "remarks_value": remarks_value
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
            value_url = (r.json())
            print(f"==>> value_url: {value_url}")
            if value_url['status'] == 'meron':
                dtno_value = value_url['dtno']
                showinfo(
                    "warning", f"Already have ticket . \nDTNO {dtno_value}")
            else:
                dtno_value = value_url['dtno']
                showinfo(
                    "Success", f"Job order created successfully. \nDTNO {dtno_value}")
            print(value_url['dtno'])
        else:
            showerror("Error", "Error in creating job order.")

    def submit(self):
        self.collect_and_print_values()

    def close_window(self):
        self.root.destroy()


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    request_ticket_app = RequestTicket(root)
    request_ticket_app.run()