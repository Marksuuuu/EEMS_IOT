import csv
import datetime
import json
import os
import tkinter as tk
import tkinter.font as tkFont
# from datetime import datetime
from io import BytesIO
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
# from datetime import datetime

import requests
from PIL import Image, ImageTk

# from mo_details import MO_Details
from operator_module.operator_utils.mo_controller import MoDetails
from operator_module.operator_utils.request_ticket import RequestTicket
from utils.status_update import StatusUpdate
from utils.ticket_status import TicketChecker


# from request_ticket import RequestTicket
# from move_mo import MOData


class UserPermissions:
    def __init__(self, config_path):
        self.config_path = config_path
        self.employee_departments = []
        self.employee_positions = []
        self.technician = []
        self.operator = []

    def load_permissions(self):
        try:
            with open(self.config_path) as json_file:
                data = json.load(json_file)
                self.employee_departments = data["allowed_users"]["employee_department"]
                self.employee_positions = data["allowed_users"]["employee_position"]
                self.operator = data["allowed_users"]["operator"]
                self.technician = data["allowed_users"]["technician"]
        except FileNotFoundError as e:
            print(e)
            self.employee_departments = []
            self.employee_positions = []
            self.technician = []
            self.operator = []

    def is_department_allowed(self, department):
        return department in self.employee_departments

    def is_position_allowed(self, position):
        return position in self.employee_positions

    def is_technician(self, position):
        return position in self.technician

    def is_operator(self, position):
        return position in self.operator


class CSVMonitor:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.previous_content = self.read_csv_content()
        self.new_data_count = 0

    def read_csv_content(self):
        try:
            with open(self.csv_file_path, "r") as csv_file:
                return csv_file.read()
        except FileNotFoundError:
            return ""

    def check_for_new_data(self):
        current_content = self.read_csv_content()

        if self.previous_content != current_content:
            current_rows = current_content.strip().split("\n")
            previous_rows = self.previous_content.strip().split("\n")

            new_rows = len(current_rows) - len(previous_rows)
            if new_rows > 0:
                self.new_data_count += new_rows

            self.previous_content = current_content

        return self.new_data_count


class OperatorDashboard:
    def __init__(self, root, user_department, user_position, dataJson):
        data = dataJson["data"]

        ## GLOBAL VARIABLE ##
        self.root = root
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        self.extracted_username = data[6]
        self.idle_started = self.load_idle_state()
        self.details_window = None
        self.window_open = False

        self.details_window = None

        if self.extracted_photo_url == False or self.extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:
            # Replace with your image URL
            image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize(
            (desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        ## FUNCTIONS ##

        self.gui_operator()
        self.update_status()
        self.create_tree_view()
        self.verify_ticket_status()
        self.update_table()
        self.check_window_active()
        self.save_idle_state()
        # self.save_idle_state()

        ## END ##

        root.title(
            f"OPERATOR DASHBOARD - {self.extracted_employee_no} -- POSITION - {self.extracted_possition}"
        )
        width = 1800
        height = 1013
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "../config", "settings.json"
        )
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def gui_operator(self):
        self.set_fullname = tk.Label(self.root)
        self.set_fullname["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=18)
        self.set_fullname["font"] = ft
        self.set_fullname["fg"] = "#333333"
        self.set_fullname["justify"] = "center"
        self.set_fullname["text"] = self.extracted_fullname
        self.set_fullname.place(x=1390, y=10, width=400, height=75)

        self.set_img = tk.Label(self.root, image=self.image)
        self.set_img["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.set_img["font"] = ft
        self.set_img["fg"] = "#333333"
        self.set_img["justify"] = "center"
        self.set_img["text"] = "label"
        self.set_img.place(x=1270, y=10, width=109, height=75)

        self.ticket_checking = tk.Label(self.root)
        self.ticket_checking["bg"] = "#ffb800"
        # self.ticket_checking["cursor"] = "circle"
        ft = tkFont.Font(family='Times', size=10)
        self.ticket_checking["font"] = ft
        self.ticket_checking["fg"] = "#000000"
        self.ticket_checking["justify"] = "center"
        self.ticket_checking.place(x=460, y=10, width=750, height=37)

        # self.GLabel_703 = tk.Label(self.root)
        # self.GLabel_703["bg"] = "#ffffff"
        # ft = tkFont.Font(family='Times', size=10)
        # self.GLabel_703["font"] = ft
        # self.GLabel_703["fg"] = "#333333"
        # self.GLabel_703["justify"] = "center"
        # self.GLabel_703["text"] = "label"
        # self.GLabel_703.place(x=40, y=200, width=1730, height=582)

        self.show_mo_details = tk.Button(self.root)
        self.show_mo_details["bg"] = "#01aaed"
        ft = tkFont.Font(family='Times', size=16)
        self.show_mo_details["font"] = ft
        self.show_mo_details["fg"] = "#ffffff"
        self.show_mo_details["justify"] = "center"
        self.show_mo_details["text"] = 'REQUEST TICKET'
        self.show_mo_details.place(x=40, y=810, width=236, height=77)
        self.show_mo_details["command"] = self.tickets_command

        self.logout_btn = tk.Button(self.root)
        self.logout_btn["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times', size=16)
        self.logout_btn["font"] = ft
        self.logout_btn["fg"] = "#ffffff"
        self.logout_btn["justify"] = "center"
        self.logout_btn["text"] = "LOG ME OUT"
        self.logout_btn.place(x=1640, y=110, width=149, height=50)
        self.logout_btn["command"] = self.logout

        # self.refresh_btn = tk.Button(self.root)
        # self.refresh_btn["bg"] = "#999999"
        # self.refresh_btn["cursor"] = "circle"
        # ft = tkFont.Font(family="Times", size=16)
        # self.refresh_btn["font"] = ft
        # self.refresh_btn["fg"] = "#333333"
        # self.refresh_btn["justify"] = "center"
        # self.refresh_btn["text"] = "REFRESH"
        # self.refresh_btn["command"] = self.update_table
        # self.refresh_btn.place(x=1450, y=110, width=150, height=50)

        self.statusHere = tk.Label(self.root)
        ft = tkFont.Font(family='Times', size=56)
        self.statusHere["font"] = ft
        self.statusHere["justify"] = "center"
        self.statusHere["text"] = "ONLINE"
        self.statusHere.place(x=40, y=10, width=359, height=106)

    def create_tree_view(self):
        self.tree = ttk.Treeview(
            self.root,
            show="headings",
            columns=(
                "ROW NUMBER",
                "CUSTOMER",
                "DEVICES",
                "MAIN OPERATION",
                "PACKAGE",
                "MO QUANTITY",
                "MO",
                "STATUS",
            ),
        )
        self.tree.heading("ROW NUMBER", text="#")
        self.tree.heading("CUSTOMER", text="CUSTOMER")
        self.tree.heading("DEVICES", text="DEVICES")
        self.tree.heading("MAIN OPERATION", text="MAIN OPERATION")
        self.tree.heading("PACKAGE", text="PACKAGE")
        self.tree.heading("MO QUANTITY", text="MO QUANTITY")
        self.tree.heading("MO", text="MO NUMBER")
        self.tree.heading("STATUS", text="STATUS")
        self.tree.pack(pady=120)

        header_style = ttk.Style()
        header_style.configure("Treeview.Heading", font=("Helvetica", 15))

        row_style = ttk.Style()
        row_style.configure("Treeview", font=("Helvetica", 12))
        row_style.configure("Treeview.Item", padding=(10, 5))

        # Adjust the width for each column
        self.tree.column("ROW NUMBER", width=50)
        self.tree.column("CUSTOMER", width=150)
        self.tree.column("DEVICES", width=250)
        self.tree.column("MAIN OPERATION", width=150)
        self.tree.column("PACKAGE", width=100)
        self.tree.column("MO QUANTITY", width=100)
        self.tree.column("MO", width=100)
        self.tree.column("STATUS", width=100)

        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.populate_table()
        # self.root.after(5000, self.update_table)

        self.update_status()

        self.tree.bind("<Double-1>", self.double_click_handler)
        self.tree.place(x=40, y=200, width=1730, height=582)

    def double_click_handler(self, event):
        if not self.get_last_offline_entry():
            self.show_popup_view(event)
        # else:
        #     showinfo("Offline Alert", "Cannot perform action while offline.")

    def get_last_offline_entry(self):
        last_offline_entry = None
        with open('data/logs/logs.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == "OFFLINE":
                    last_offline_entry = row

        if last_offline_entry:
            event_type, event_date, event_time = last_offline_entry[:3]
            event_datetime = datetime.strptime(
                f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
            showwarning(
                "MACHINE OFFLINE!",
                "Attention! The machine is currently OFFLINE",
            )
            return {
                "event_type": event_type,
                "event_datetime": event_datetime
            }
        else:
            return None

    def read_json_file(self):
        try:
            with open("data/main.json", "r") as json_file:
                data = json.load(json_file)
                extracted_data = []

                for item in data["data"]:
                    customer = item["customer"]
                    device = item["device"]
                    main_opt = item["main_opt"]
                    package = item["package"]
                    running_qty = item["running_qty"]
                    wip_entity_name = item["wip_entity_name"]
                    status = item.get("status", "")
                    extracted_data.append(
                        (customer, device, main_opt, package, running_qty, wip_entity_name, status))
            return extracted_data
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error {e}")
            return []

    def read_mo_logs(self):
        try:
            with open('data/mo_logs.json', 'r') as json_file:
                mo_logs = json.load(json_file)
            return mo_logs

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error {e}")
            return []

    def read_json_file_with_status(self):
        main_data = None

        mo_logs = self.read_mo_logs()

        with open("data/main.json", "r") as json_file:
            main_data = json.load(json_file)

        extracted_data = []

        for item in main_data["data"]:
            wip_entity_name = item["wip_entity_name"]
            status = ""

            for mo_log_entry in mo_logs["data"]:
                if mo_log_entry["wip_entity_name"] == wip_entity_name:
                    status = mo_log_entry["status"]
                    break

            extracted_data.append((
                item["customer"],
                item["device"],
                item["main_opt"],
                item["package"],
                item["running_qty"],
                item["wip_entity_name"],
                status  # Add the status here
            ))

        return extracted_data

    def populate_table(self):

        if os.stat("data/mo_logs.json").st_size == 0:
            data = self.read_json_file()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data,
                                                                                                            start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

        else:
            data = self.read_json_file_with_status()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data,
                                                                                                            start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        self.populate_table()

    def show_popup_view(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            showinfo(title="Error", message="No data selected.")
            return

        item = self.tree.item(selected_item)
        data = item["values"]

        if selected_item[0] == "1":
            self.show_mo_details_function(data)

        else:
            self.validate_ppc_employee()

    def validate_ppc_employee(self):
        employee_number = self.extracted_employee_no
        log_file_path = os.path.join(
            self.get_script_directory(), "../config", "hris.json")
        employee_number = simpledialog.askstring(
            "Employee ID", "Please enter your Employee ID."
        )

        if employee_number is None:
            return

        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)["result"]

        matching_employee = None
        for employee in data:
            if int(employee.get("employee_id_no")) == int(employee_number):
                matching_employee = employee
                # self.update_table()
                # print("UPDATE TABLE RUN")
                break

        if matching_employee:
            user_department = matching_employee.get("employee_department")
            self.validate_permissions(user_department)
        else:
            showerror('Error', 'Employee not found!')

    def validate_permissions(self, user_department):
        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department):
            selected_item = self.tree.selection()
            self.swap_position(selected_item)
        else:
            showerror(
                title="Login Failed",
                message=f"User's department or position is not allowed. {user_department}",
            )

    def swap_position(self, selected_item):

        selected_id = self.tree.item(selected_item, "text")
        first_id = "1"

        selected_data = self.tree.item(selected_item, "values")
        first_data = self.tree.item(first_id, "values")

        # Load data from the JSON file
        with open("data/main.json", "r") as json_file:
            data = json.load(json_file)

        # Swap data within the dictionaries
        data_list = data["data"]
        (
            data_list[int(selected_id) - 1]["customer"],
            data_list[int(first_id) - 1]["customer"],
        ) = (first_data[1], selected_data[1])
        (
            data_list[int(selected_id) - 1]["device"],
            data_list[int(first_id) - 1]["device"],
        ) = (first_data[2], selected_data[2])
        (
            data_list[int(selected_id) - 1]["main_opt"],
            data_list[int(first_id) - 1]["main_opt"],
        ) = (first_data[3], selected_data[3])
        (
            data_list[int(selected_id) - 1]["package"],
            data_list[int(first_id) - 1]["package"],
        ) = (first_data[4], selected_data[4])
        (
            data_list[int(selected_id) - 1]["running_qty"],
            data_list[int(first_id) - 1]["running_qty"],
        ) = (first_data[5], selected_data[5])
        (
            data_list[int(selected_id) - 1]["wip_entity_name"],
            data_list[int(first_id) - 1]["wip_entity_name"],
        ) = (first_data[6], selected_data[6])

        data["data"] = data_list

        with open("data/main.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        self.tree.item(
            selected_item,
            values=(
                selected_id, first_data[1], first_data[2], first_data[3], first_data[4], first_data[5], first_data[6]),
        )
        self.tree.item(
            first_id,
            values=(first_id, selected_data[1], selected_data[2], selected_data[3], selected_data[4], selected_data[5],
                    selected_data[6]),
        )

        showinfo("Success", "Data swapped successfully!")
        self.update_table()

    def update_status(self):
        statusHere = StatusUpdate('data/logs/logs.csv')
        getStatus = statusHere.get_last_log_value()
        if getStatus is None or False:
            self.statusHere["bg"] = "#ffffff"
            self.statusHere["text"] = ''
        elif getStatus == 'ONLINE':
            self.statusHere["bg"] = "#4CAF50"
            self.statusHere["fg"] = "#ffffff"
            self.statusHere["text"] = getStatus
        else:
            self.statusHere["bg"] = "#cc0000"
            self.statusHere["fg"] = "#ffffff"
            self.statusHere["text"] = 'OFFLINE'
        self.root.after(50000, self.update_status)

    def logout(self):
        response = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()
            os.system("python index.py")

    def tickets_command(self):
        # self.root.withdraw()
        self.ticket_dashboard = Toplevel(self.root)
        show_ticket_dashboard = RequestTicket(
            self.ticket_dashboard, self.extracted_fullname, self.extracted_employee_no
        )

    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()

        if ticket_present:
            self.ticket_checking[
                "text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        else:
            self.ticket_checking.destroy()

    def show_mo_details_function(self, data):
        if self.details_window is None or not self.details_window.winfo_exists():
            self.details_window = tk.Toplevel(self.root)
            assets_dir = 'assets'
            show_mo_details_window = MoDetails(
                self.details_window, self.extracted_fullname, self.extracted_employee_no,
                self.extracted_photo_url, self.extracted_username, data, self.update_table)
            # show_mo_details_window = MoDetailsTest(
            #     self.details_window, self.extracted_fullname, self.extracted_employee_no,
            #     self.extracted_photo_url, self.extracted_username, data, self.update_table, assets_dir)
            self.window_open = True
        else:
            self.details_window.lift()

    def check_window_active(self):
        if self.details_window is not None and self.details_window.winfo_exists():
            # print('win close')
            if self.idle_started:
                self.idle_started = False
                self.log_event("IDLE_STOP")
        else:
            # print('win open')
            if not self.idle_started:
                self.idle_started = True
                self.log_event("IDLE_START")
        self.root.after(10000, self.check_window_active)

    def log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open('data/logs/idle.csv', mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def load_idle_state(self):
        try:
            with open('config/idle_state.json', 'r') as state_file:
                state = json.load(state_file)
                return state.get('idle_started', False)
        except FileNotFoundError:
            return False

    def save_idle_state(self):
        with open('config/idle_state.json', 'w') as state_file:
            json.dump({'idle_started': self.idle_started}, state_file)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("config/ico/favicon.ico")
    app = App(root)
    root.mainloop()
