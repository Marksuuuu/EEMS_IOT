import json
import os
import csv
import tkinter.simpledialog as simpledialog
from tkinter.messagebox import showinfo, showwarning, showerror
from datetime import datetime
import tkinter as tk
from tkinter import ttk


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
                print(self.new_data_count)

            self.previous_content = current_content

        return self.new_data_count


class TreeViewManager:
    def __init__(self, root):
        self.tree = ttk.Treeview(
            root,
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
        self.tree.heading("ROW NUMBER", text="ROW NUMBER")
        self.tree.heading("CUSTOMER", text="CUSTOMER")
        self.tree.heading("DEVICES", text="DEVICES")
        self.tree.heading("MAIN OPERATION", text="MAIN OPERATION")
        self.tree.heading("PACKAGE", text="PACKAGE")
        self.tree.heading("MO QUANTITY", text="MO QUANTITY")
        self.tree.heading("MO", text="MO")
        self.tree.heading("STATUS", text="STATUS")
        self.tree.pack(pady=120)

        self.populate_table()
        # self.root.after(5000, self.update_table)

        self.tree.bind("<Double-1>", self.double_click_handler)
        self.tree.place(x=40, y=200, width=1730, height=582)

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def double_click_handler(self, event):
        if not self.get_last_offline_entry():
            self.show_popup_view(event)
        # else:
        #     showinfo("Offline Alert", "Cannot perform action while offline.")

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "../config", "settings.json"
        )
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

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
            print('last_offline_entry: ', last_offline_entry)
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

    def populate_table(self):

        if os.stat("data/mo_logs.json").st_size == 0:
            print("mo_logs.json is empty.")
            data = self.read_json_file()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data, start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

        else:
            print("mo_logs.json is not empty.")
            data = self.read_json_file_with_status()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data, start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

    def update_table(self):
        # Clear existing data from the treeview
        self.tree.delete(*self.tree.get_children())

        self.populate_table()

        # self.root.after(5000, self.update_table)

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
            self.validate_offline_employee()

    def validate_offline_employee(self):
        employee_number = self.extracted_employee_no
        log_file_path = os.path.join(
            self.get_script_directory(), "../config", "hris.json")
        employee_number = simpledialog.askstring(
            "Employee ID", "Please enter your Employee ID."
        )
        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)["result"]

        matching_employee = None
        for employee in data:
            if int(employee.get("employee_id_no")) == int(employee_number):
                matching_employee = employee
                break

        if matching_employee:
            user_department = matching_employee.get("employee_department")
            self.validate_permissions(user_department)
        else:
            print("Employee not found.")

    def validate_permissions(self, user_department):
        print(user_department)
        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department):
            selected_item = self.tree.selection()
            self.swap_position(selected_item)

            print("User allowed.")
        else:
            showerror(
                title="Login Failed",
                message=f"User's department or position is not allowed. {user_department}",
            )

    def swap_position(self, selected_item):
        print('selected_item: ', selected_item)

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

    def show_mo_details_function(self, data):
        self.details_window = tk.Toplevel(self.root)
        show_mo_details_window = MoDetails(self.details_window, self.extracted_fullname, self.extracted_employee_no,
                                           self.extracted_photo_url, self.extracted_username, data)


if __name__ == "__main__":
    TreeViewManager()