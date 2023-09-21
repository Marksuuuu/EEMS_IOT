import json
import os
import tkinter as tk
import tkinter.font as tkFont
import csv
from datetime import datetime
from io import BytesIO
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
import requests
from PIL import Image, ImageTk
import logging
import datetime
import subprocess
from utils.status_update import StatusUpdate


# from mo_details import MO_Details
# from operator_module.operator_utils.mo_controller import MoDetails
# from operator_module.operator_utils.request_ticket import RequestTicket
from operator_module.operator_utils.request_ticket_test import RequestTicketTest
from operator_module.operator_utils.mo_controller_test import MoDetailsTest
from utils.ticket_status import TicketChecker
# from request_ticket import RequestTicket
# from move_mo import MOData
from tkinter import Canvas, Entry, Button, PhotoImage
from pathlib import Path


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

class OperatorDashboardTest:
    def __init__(self, root, user_department, user_position, dataJson, assets_dir):
        data = dataJson["data"]

        ## GLOBAL VARIABLE ##
        self.root = root
        # self.root.attributes('-fullscreen',True)
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        self.extracted_username = data[6]



        self.idle_started = self.load_idle_state()
        self.details_window = None
        self.ticket_window = None
        self.window_open = False

        if self.extracted_photo_url == False or self.extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:
            # Replace with your image URL
            image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 74
        pil_image = pil_image.resize(
            (desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        self.assets_dir = assets_dir
        self.root.geometry("1024x600")
        self.root.configure(bg="#D45151")
        root.title(
            f"OPERATOR DASHBOARD - {self.extracted_employee_no} -- POSITION - {self.extracted_possition}"
        )


        button1 = "assets/frame_operator/button_1.png"
        button2 = "assets/frame_operator/button_2.png"
        button3 = "assets/frame_operator/button_3.png"

        img_1 = "assets/frame_operator/image_1.png"
        img_2 = "assets/frame_operator/image_2.png"
        img_3 = "assets/frame_operator/image_3.png"

        button1_pill = Image.open(button1)
        button2_pill = Image.open(button2)
        button3_pill = Image.open(button3)

        image_1 = Image.open(img_1)
        image_2 = Image.open(img_2)
        image_3 = Image.open(img_3)

        self.tk_btn_1 = ImageTk.PhotoImage(button1_pill)
        self.tk_btn_2 = ImageTk.PhotoImage(button2_pill)
        self.tk_btn_3 = ImageTk.PhotoImage(button3_pill)

        self.tk_image_1 = ImageTk.PhotoImage(image_1)
        self.tk_image_2 = ImageTk.PhotoImage(image_2)
        self.tk_image_3 = ImageTk.PhotoImage(image_3)

        
        self.canvas = Canvas(
            self.root,
            bg="#F7F7F7",
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
            181.0,
            994.0,
            581.0,
            fill="#FFFFFF",
            outline="")



        # self.image_image_1 = self.canvas.create_image(
        #     64.0,
        #     47.0,
        #     image=self.tk_image_1
        # )


        
        self.image_image_3 = self.canvas.create_image(
            728.0,
            48.0,
            image=self.image
        )




        self.button_1 = tk.Button(
            self.root,
            image=self.tk_btn_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.signout,
            relief="flat",
        )

        self.button_1.place(
            x=872.0,
            y=119.0,
            width=122.0,
            height=42.0
        )


        # FULL NAME
        # ///////////////////////////////////////////
        self.canvas.create_text(
            769.0,
            39.0,
            anchor="nw",
            text=self.extracted_fullname,
            fill="#343A40",
            font=("Roboto Bold", 20 * -1)
        )


        self.button_2 = tk.Button(
            self.root,
            image=self.tk_btn_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.tickets_command,
            relief="flat",
        )

        self.button_2.place(
            x=31.0,
            y=118.0,
            width=162.0,
            height=43.0
        )



        # FUNCTIONS
        # /////////////////////////////////////
        self.update_status()
        self.verify_ticket_status()
        # self.update_table()
        # self.check_window_active()
        # self.save_idle_state()

        self.create_tree_view()
        self.center_window()
        self.online_status_card()
        self.root.resizable(False, False)
        # self.root.attributes('-topmost', True)

    def destroy_details_window(self):
        if self.details_window is not None and self.details_window.winfo_exists():
            self.details_window.destroy()
            self.details_window = None

    def destroy_ticket_window(self):
        if self.ticket_window is not None and self.ticket_window.winfo_exists():
            self.ticket_window.destroy()
            self.ticket_window = None

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
                # "ACTION",
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
        # self.tree.heading("ACTION", text="ACTION")
        self.tree.pack(pady=10)

        header_style = ttk.Style()
        header_style.configure("Treeview.Heading", font=("Helvetica", 13))


        row_style = ttk.Style()
        row_style.configure("Treeview", font=("Helvetica", 12))
        row_style.configure("Treeview.Item", padding=(0, 0))
        row_style.configure('Treeview', rowheight=40)

        # Adjust the width for each column
        self.tree.column("ROW NUMBER",minwidth=0, width=50, stretch=False)
        self.tree.column("CUSTOMER",minwidth=0, width=100, stretch=False)
        self.tree.column("DEVICES",minwidth=0, width=180, stretch=False)
        self.tree.column("MAIN OPERATION",minwidth=0, width=130, stretch=False)
        self.tree.column("PACKAGE",minwidth=0, width=100, stretch=False)
        self.tree.column("MO QUANTITY",minwidth=0, width=130, stretch=False)
        self.tree.column("MO",minwidth=0, width=120, stretch=False)
        self.tree.column("STATUS",minwidth=0, width=150, stretch=False)
        # self.tree.column("ACTION",minwidth=0, width=90, stretch=False)
        # self.tree.column("ACTION", width=90, anchor="center")

        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.populate_table()

        self.update_status()

        self.tree.bind("<Double-1>", self.double_click_handler)
        self.tree.place(x=31.0, y=181.0, width=964, height=400)


    def online_status_card(self):
        self.canvas.create_rectangle(
            31.0,
            10.0,
            282.0,
            86.97332763671875,
            fill="#D3F9D8",
            outline=""
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

        self.image_image_2 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.tk_image_2
        )

    def offline_status_card(self):
        self.canvas.create_rectangle(
            31.0,
            10.0,
            282.0,
            86.97332763671875,
            fill="#FFCECE",
            outline=""
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
            text="OFFLINE",
            fill="#343A40",
            font=("Roboto Medium", 24 * -1)
        )

        self.image_image_1 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.tk_image_1
        )


    def show_ticket_button(self):
        self.button_3 = tk.Button(
            self.root,
            image=self.tk_btn_3,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )

        self.button_3.place(
            x=326.0,
            y=115.0,
            width=372.0,
            height=51.0
        )

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "../config", "settings.json"
        )
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    # def on_button_click(self, values):
    #     # Implement the action to be taken when the button in the ACTION column is clicked.
    #     # You can use the 'values' parameter to identify which row was clicked.
    #     print(f"Button clicked for row {values[0]}")


    def double_click_handler(self, event):
        if not self.get_last_offline_entry():
            self.show_popup_view(event)


    def get_last_offline_entry(self):
        last_offline_entry = None
        with open('data/logs/logs.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if row[0] == "OFFLINE":
                    last_offline_entry = row

        if last_offline_entry:
            event_type, event_date, event_time = last_offline_entry[:3]
            event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
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


    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        self.populate_table()

    def populate_table(self):

        if os.stat("data/mo_logs.json").st_size == 0:
            data = self.read_json_file()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data, start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

        else:
            data = self.read_json_file_with_status()

            for i, (customer, device, main_opt, package, running_qty, wip_entity_name, status) in enumerate(data, start=1):
                self.tree.insert(
                    "", "end", iid=i, text=str(i),
                    values=(i, customer, device, main_opt, package,
                            running_qty, wip_entity_name, status)
                )

    def show_popup_view(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            showinfo(title="Error", message="No row is selected.")
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
                break

        if matching_employee:
            user_department = matching_employee.get("employee_department")
            self.validate_permissions(user_department)
        else:
            showerror('Error', 'Employee not found!')


    def validate_permissions(self, user_department):
        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department):
            if user_department == "Materials Planning & Control and Purchasing":
                selected_item = self.tree.selection()
                self.swap_position(selected_item)
            else:
                showerror(
                title="Login Failed",
                message=f"User's department is not allowed. {user_department}",
            )
        else:
            showerror(
                title="Login Failed",
                message=f"User's department is not allowed. {user_department}",
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

    # def update_status(self):
    #     statusHere = StatusUpdate('data/logs/logs.csv')
    #     getStatus = statusHere.get_last_log_value()
    #     if getStatus is None or False:
    #         pass
    #     elif getStatus == 'ONLINE':
    #         self.online_status_card()

    #     else:
    #         self.offline_status_card()

    #     self.root.after(1000, self.update_status)

    def update_status(self):
        statusHere = StatusUpdate('data/logs/logs.csv')
        getStatus = statusHere.get_last_log_value()
        if getStatus is None or False:
            pass
        elif getStatus == 'ONLINE':
            self.online_status_card()
        else:
            self.offline_status_card()
            # Disable opening MoDetailsTest and show a warning
            if self.details_window is not None and self.details_window.winfo_exists():
                showwarning("MACHINE OFFLINE!", "Machine is currently OFFLINE.")
                self.details_window.destroy()

        self.root.after(1000, self.update_status)
    def logout(self):
        response = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()
            os.system("python index.py")

    def tickets_command(self):
        self.destroy_ticket_window()

        selected_item = self.tree.selection()
        if not selected_item:
            showinfo(title="Error", message="No data selected.")
            return
        item = self.tree.item(selected_item)
        data = item["values"]

        if self.ticket_window is None or not self.ticket_window.winfo_exists():
            self.ticket_dashboard = Toplevel(self.root)
            assets_dir = 'assets'
            show_ticket_dashboard = RequestTicketTest(
                self.ticket_dashboard, self.extracted_fullname, self.extracted_employee_no, assets_dir, data, self.show_ticket_button)
            self.ticket_window = self.ticket_dashboard  # Set the ticket window to the newly opened window
        else:
            self.ticket_window.lift()

    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()

        if ticket_present:
            self.show_ticket_button()
            # self.ticket_checking["text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        else:
            # self.ticket_checking.destroy()
            pass

    def show_mo_details_function(self, data):
        self.destroy_details_window()

        if self.details_window is None or not self.details_window.winfo_exists():
            self.details_window = tk.Toplevel(self.root)
            assets_dir = 'assets'
            # show_mo_details_window = MoDetails(
            #     self.details_window, self.extracted_fullname, self.extracted_employee_no,
            #     self.extracted_photo_url, self.extracted_username, data, self.update_table)
            show_mo_details_window = MoDetailsTest(
                self.details_window, self.extracted_fullname, self.extracted_employee_no,
                self.extracted_photo_url, self.extracted_username, data, self.update_table, assets_dir)
            self.window_open = True
            
        else:
            self.details_window.lift()
          

    def check_window_active(self):
        if self.details_window is not None and self.details_window.winfo_exists():
            # print('win close')
            if self.idle_started:
                self.idle_started = False
                print("TURN OFF ALL")
                self.log_event("IDLE_STOP")
        else:
            # print('win open')
            if not self.idle_started:
                self.idle_started = True
                print("TURN ORANGE")
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
            
    def signout(self):
        response: bool = messagebox.askyesno(
            "Sign out", "Are you sure you want to Sign out?")
        if response:
            self.root.withdraw()
            subprocess.call(["python", "index.py"])


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
    app = OperatorDashboardTest(root)
    root.mainloop()

