import json
import os
import tkinter as tk
import tkinter.font as tkFont
from datetime import date
from datetime import datetime
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror

import requests


class RequestTicket:
    def __init__(self, root, extracted_fullname, extracted_employee_no):
        self.root = root
        # setting title
        root.title("TICKET")
        # setting window size
        width = 998
        height = 531
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.fullname = extracted_fullname
        self.employee_no = extracted_employee_no

        now = datetime.now()
        today = date.today()
        self.current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        self.dropdown_var = tk.StringVar()

        self.fetch_downtime_types()

        # ////////////////////////////////////////
        # REQUESTOR
        lbl_Requestor = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_Requestor["font"] = ft
        lbl_Requestor["fg"] = "#333333"
        lbl_Requestor["justify"] = "center"
        lbl_Requestor["text"] = "REQUESTOR"
        lbl_Requestor.place(x=0, y=8, width=144, height=50)

        lbl_FullName = tk.Label(root)
        lbl_FullName["bg"] = "#fefefe"
        lbl_FullName["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=13)
        lbl_FullName["font"] = ft
        lbl_FullName["fg"] = "#333333"
        lbl_FullName["justify"] = "center"
        lbl_FullName["text"] = extracted_fullname
        lbl_FullName.place(x=0, y=40, width=516, height=50)

        # ////////////////////////////////////////
        # DATE NOW

        lbl_DateTime = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_DateTime["font"] = ft
        lbl_DateTime["fg"] = "#333333"
        lbl_DateTime["justify"] = "center"
        lbl_DateTime["text"] = "DATE | TIME"
        lbl_DateTime.place(x=20, y=90, width=300, height=50)

        lbl_DateNow = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_DateNow["font"] = ft
        lbl_DateNow["fg"] = "#333333"
        lbl_DateNow["justify"] = "center"
        lbl_DateNow["text"] = self.current_date_time
        lbl_DateNow.place(x=20, y=120, width=300, height=50)



        # ////////////////////////////////////////
        # TIME DOWN

        lbl_TimeDown = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_TimeDown["font"] = ft
        lbl_TimeDown["fg"] = "#333333"
        lbl_TimeDown["justify"] = "center"
        lbl_TimeDown["text"] = "TIME DOWN"
        lbl_TimeDown.place(x=900, y=120, width=300, height=50)



        # ////////////////////////////////////////
        # MACHINE NO.
        lbl_MachineNo = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_MachineNo["font"] = ft
        lbl_MachineNo["fg"] = "#333333"
        lbl_MachineNo["justify"] = "center"
        lbl_MachineNo["text"] = "MACHINE NO."
        lbl_MachineNo.place(x=20, y=200, width=200, height=50)

        lbl_MachineNo_Value = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_MachineNo_Value["font"] = ft
        lbl_MachineNo_Value["fg"] = "#333333"
        lbl_MachineNo_Value["justify"] = "center"
        lbl_MachineNo_Value["text"] = self.load_machno()
        lbl_MachineNo_Value.place(x=20, y=230, width=200, height=50)

        lbl_DowntimeType = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_DowntimeType["font"] = ft
        lbl_DowntimeType["fg"] = "#333333"
        lbl_DowntimeType["justify"] = "center"
        lbl_DowntimeType["text"] = "DOWNTIME TYPE"
        lbl_DowntimeType.place(x=540, y=200, width=250, height=50)

        dropdown = ttk.Combobox(root, textvariable=self.dropdown_var, state="readonly")
        dropdown["values"] = [item["DOWNTIME_TYPE"] for item in self.downtime_data]
        dropdown.bind("<<ComboboxSelected>>", self.on_select)
        dropdown.place(x=540, y=240, width=250, height=30)

        # dropdown.pack(padx=20, pady=20)

        # ////////////////////////////////////////
        # REMARKS

        self.le_Remarks = tk.Entry(root)
        self.le_Remarks["bg"] = "#ffffff"
        self.le_Remarks["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=13)
        self.le_Remarks["font"] = ft
        self.le_Remarks["fg"] = "#333333"
        self.le_Remarks["justify"] = "center"
        self.le_Remarks["text"] = "Entry"
        self.le_Remarks.delete(0, tk.END)
        self.le_Remarks.place(x=60, y=330, width=859, height=82)

        lbl_Remarks = tk.Label(root)
        ft = tkFont.Font(family="Times", size=13)
        lbl_Remarks["font"] = ft
        lbl_Remarks["fg"] = "#333333"
        lbl_Remarks["justify"] = "center"
        lbl_Remarks["text"] = "REMARKS"
        lbl_Remarks.place(x=440, y=300, width=101, height=30)

        # ////////////////////////////////////////
        # CHECKBOX
        self.checkbox_var = tk.BooleanVar()

        checkbox = ttk.Checkbutton(
            root,
            text="Supervisor",
            variable=self.checkbox_var,
            command=self.checkbox_clicked,
        )
        checkbox.place(x=540, y=280, height=30)

        # ////////////////////////////////////////
        # BUTTONS

        btn_Submit = tk.Button(root)
        btn_Submit["bg"] = "#5fb878"
        ft = tkFont.Font(family="Times", size=13)
        btn_Submit["font"] = ft
        btn_Submit["fg"] = "#fbfbfb"
        btn_Submit["justify"] = "center"
        btn_Submit["text"] = "SUBMIT"
        btn_Submit.place(x=850, y=460, width=125, height=49)
        btn_Submit["command"] = self.submit

        btn_Cancel = tk.Button(root)
        btn_Cancel["bg"] = "#ff0909"
        ft = tkFont.Font(family="Times", size=13)
        btn_Cancel["font"] = ft
        btn_Cancel["fg"] = "#ffffff"
        btn_Cancel["justify"] = "center"
        btn_Cancel["text"] = "CANCEL"
        btn_Cancel.place(x=700, y=460, width=124, height=50)
        btn_Cancel["command"] = self.close_window

        # ////////////////////////////////////////
        # FUNCTIONS

    def load_machno(self):
        log_file_path = os.path.join(self.get_script_directory(), "../../data", "main.json")

        with open(log_file_path, "r") as json_file:
            get_machno = json.load(json_file)["machno"]

        return get_machno

        # matching_employee = None
        # for employee in data:
        #     if employee.get('employee_id_no') == employee_number:
        #         matching_employee = employee
        #         break

        # if matching_employee:
        #     user_department = matching_employee.get('employee_department')
        #     user_position = matching_employee.get('employee_position')

        #     self.validate_permissions(user_department, user_position)
        # else:
        #     print("Employee not found.")

    def checkbox_clicked(self):
        checkbox_value = self.checkbox_var.get()
        self.set_checkbox_value = None

        if checkbox_value == True:
            self.set_checkbox_value = 1
        else:
            self.set_checkbox_value = 0

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def fetch_downtime_types(self):
        cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
        response = requests.get(cmms_url)
        data = response.json()
        self.downtime_data = data["result"]

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
        checkbox_value = self.set_checkbox_value
        remarks_value = self.le_Remarks.get()

        # Load existing JSON data if the file exists, or create an empty list
        file_path = "data/logs/ticket_logs.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)
        else:
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
                showinfo("warning", f"Already have ticket . \nDTNO {dtno_value}")
            else:
                dtno_value = value_url['dtno']
                showinfo("Success", f"Job order created successfully. \nDTNO {dtno_value}")
            print(value_url['dtno'])
        else:
            showerror("Error", "Error in creating job order.")

    def get_selected_downtime_type_id(self):
        selected_text = self.dropdown_var.get()
        selected_id = None
        for item in self.downtime_data:
            if item['DOWNTIME_TYPE'] == selected_text:
                selected_id = item['ID']
                break
        return selected_id

    def submit(self):
        print("Submit")
        self.collect_and_print_values()

    def close_window(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RequestTicket(root)
    root.mainloop()
