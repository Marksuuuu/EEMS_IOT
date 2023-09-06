import csv
import json
import logging
import os
import re
import signal
import tkinter as tk
import tkinter.font as tkFont
import uuid
from datetime import datetime, timedelta
from tkinter import Toplevel
from tkinter import messagebox
from tkinter.messagebox import showerror
import time
import matplotlib.pyplot as plt
import requests
import socketio
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
# from ttkbootstrap.constants import *
import datetime

from operator_module.operator_dashboard import OperatorDashboard
from technician_module.technician_dashboard import TechnicianDashboard
from utils.quantity_data import QuantityData
from utils.status_update import StatusUpdate
from utils.time_data import TimeData
from utils.ticket_status import TicketChecker
# from utils.trigger_downtime import TriggerDowntime
from socketio_utils.socketio_manager import SocketIOManager


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


class App:
    def __init__(self, root):
        # setting title
        root.title("EEMS_IOT - © 2023")
        # setting window size

        ## GLOBAL VARIABLES##

        self.quantity_data = QuantityData("../data")
        self.get_data = TimeData('../data')

        # self.receiver = ReceiveAndRequest(self.socketio_path())
        self.total_running_qty = self.quantity_data.total_running_qty()
        self.calculate_oee = self.get_data.calculate_oee
        self.total_remaining_qty_value = self.quantity_data.total_remaining_qty()
        self.get_available_hrs = self.get_data.get_available_hrs()
        self.get_productive_hrs = self.get_data.calculate_total_productive_time()
        self.get_downtime_hrs = self.get_data.calculate_total_downtime()
        self.last_ticket_status = None
        # self.downtime_started = False
        self.downtime_started = self.load_downtime_state()
        print('test', self.downtime_started )
        self.update_interval = 50000
        self.root = root

        # self.root = root

        ## FUNCTIONS##

        self.makeCenter()
        self.mainGui()
        self.init_logging()
        self.update_clock()
        self.update_status()
        self.time_data()
        self.update_logs()
        self.create_total_qty_graph()
        self.create_oee_graph()
        self.charts()
        self.verify_ticket_status()
        self.auto_update()
        self.save_downtime_state()
        # self.downtime_trigger_record()
        # self.continuously_check_tickets()

        ## END##

    def makeCenter(self):
        self.width = 1800
        self.height = 1013
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth -
                                                              self.width) / 2, (self.screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def mainGui(self):
        self.cpk_graph = tk.Label(self.root)
        self.cpk_graph["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.cpk_graph["font"] = ft
        self.cpk_graph["fg"] = "#333333"
        self.cpk_graph["justify"] = "center"
        self.cpk_graph["text"] = "CPK"
        self.cpk_graph.place(x=20, y=130, width=580, height=550)

        self.oee_graph = tk.Label(self.root)
        self.oee_graph["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.oee_graph["font"] = ft
        self.oee_graph["fg"] = "#333333"
        self.oee_graph["justify"] = "center"
        self.oee_graph["text"] = "label"
        self.oee_graph.place(x=610, y=130, width=580, height=550)

        self.quantity_graph = tk.Label(self.root)
        self.quantity_graph["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.quantity_graph["font"] = ft
        self.quantity_graph["fg"] = "#333333"
        self.quantity_graph["justify"] = "center"
        self.quantity_graph["text"] = "QTY GRAPH"
        self.quantity_graph.place(x=1200, y=130, width=580, height=550)

        self.productive_hrs = tk.Label(self.root)
        self.productive_hrs["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.productive_hrs["font"] = ft
        self.productive_hrs["fg"] = "#333333"
        self.productive_hrs["justify"] = "center"
        self.productive_hrs.place(x=20, y=700, width=580, height=90)

        self.available_hrs = tk.Label(self.root)
        self.available_hrs["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.available_hrs["font"] = ft
        self.available_hrs["fg"] = "#333333"
        self.available_hrs["justify"] = "left"
        self.available_hrs.place(x=610, y=700, width=580, height=90)

        self.total_quantity_to_process = tk.Label(self.root)
        self.total_quantity_to_process["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.total_quantity_to_process["font"] = ft
        self.total_quantity_to_process["fg"] = "#333333"
        self.total_quantity_to_process["justify"] = "left"
        self.total_quantity_to_process.place(
            x=610, y=800, width=580, height=90)

        self.total_remaining_qty = tk.Label(self.root)
        self.total_remaining_qty["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.total_remaining_qty["font"] = ft
        self.total_remaining_qty["fg"] = "#333333"
        self.total_remaining_qty["justify"] = "left"
        self.total_remaining_qty.place(x=20, y=800, width=580, height=90)

        self.downtime = tk.Label(self.root)
        self.downtime["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.downtime["font"] = ft
        self.downtime["fg"] = "#333333"
        self.downtime["justify"] = "center"
        self.downtime.place(x=20, y=900, width=580, height=90)

        self.idle = tk.Label(self.root)
        self.idle["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.idle["font"] = ft
        self.idle["fg"] = "#333333"
        self.idle["justify"] = "center"
        self.idle["text"] = "IDLE"
        self.idle.place(x=610, y=900, width=580, height=90)

        self.statusHere = tk.Label(self.root)
        ft = tkFont.Font(family='Times', size=58)
        self.statusHere["font"] = ft
        self.statusHere["justify"] = "center"
        self.statusHere.place(x=20, y=10, width=359, height=106)

        self.employee_id = tk.Entry(self.root)
        self.employee_id["bg"] = "#ffffff"
        self.employee_id["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=83)
        self.employee_id["font"] = ft
        self.employee_id["fg"] = "#333333"
        self.employee_id["justify"] = "center"
        self.employee_id["text"] = "10450"
        self.employee_id.bind(
            '<KeyRelease>', self.validate_employee_number)
        self.employee_id.place(x=650, y=10, width=500, height=106)

        self.logs_message = tk.Message(self.root)
        self.logs_message["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=15)
        self.logs_message["font"] = ft
        self.logs_message["fg"] = "#333333"
        self.logs_message["justify"] = "left"
        self.logs_message['width'] = 580
        self.logs_message.place(x=1200, y=700, width=580, height=290)

        self.date_time = tk.Label(self.root)
        self.date_time["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=15)
        self.date_time["font"] = ft
        self.date_time["fg"] = "#333333"
        self.date_time["justify"] = "center"
        self.date_time.place(x=1480, y=10, width=300, height=60)

        self.ticket = tk.Label(root)
        self.ticket["bg"] = "#ffb800"
        self.ticket["cursor"] = "circle"
        ft = tkFont.Font(family='Times', size=9)
        self.ticket["font"] = ft
        self.ticket["fg"] = "#000000"
        self.ticket["justify"] = "left"
        self.ticket.place(x=1199, y=73, width=581, height=43)

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def socketio_path(self):
        path_here = os.path.join(
            self.get_script_directory(), "data", 'main.json')
        return path_here

    def check_internet_connection_requests(self):
        try:
            response = requests.get("http://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def validate_employee_number(self, event):
        employee_number = self.employee_id.get()
        if len(employee_number) == 5:
            if self.check_internet_connection_requests():
                self.validate_online_employee(employee_number)
            else:
                self.validate_offline_employee(employee_number)
        elif len(employee_number) == 4:
            if self.check_internet_connection_requests():
                self.validate_online_employee(employee_number)
            else:
                self.validate_offline_employee(employee_number)

    def validate_online_employee(self, employee_number):
        try:
            employee_number = int(employee_number)
            hris_url = f'http://hris.teamglac.com/api/users/emp-num?empno={employee_number}'
            response = requests.get(hris_url)

            if response.status_code == 200:
                try:
                    data = json.loads(response.text)['result']

                    # Check if data is a dictionary before accessing its values
                    if isinstance(data, dict):
                        user_department = data.get('employee_department')
                        fullname = data.get('fullname')
                        user_position = data.get('employee_position')
                        employee_no = data.get('employee_no')
                        employee_department = data.get('employee_department')
                        photo_url = data.get('photo_url')
                        username = data.get('username')

                        data = [
                            user_department,
                            fullname,
                            employee_no,
                            employee_department,
                            photo_url,
                            user_position,
                            username
                        ]
                        dataJson = {'data': data}

                        if user_department and user_position:
                            self.validate_permissions(
                                user_department, user_position, dataJson)
                        else:
                            print(
                                "Employee data doesn't contain department or position.")
                    else:
                        print(
                            "Response data is not in the expected format (dictionary).")
                except KeyError:
                    print("Response data doesn't have expected keys.")
            else:
                print("Error accessing HRIS API:", response.status_code)
        except ValueError:
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a valid integer employee number.")

    def validate_offline_employee(self, employee_number):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", 'hris.json')

        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)['result']

        matching_employee = None
        for employee in data:
            if employee.get('employee_id_no') == employee_number:
                matching_employee = employee
                break

        if matching_employee:
            user_department = matching_employee.get('employee_department')
            user_position = matching_employee.get('employee_position')
            # user_empNo = matching_employee.get('employee_id_no')

            self.validate_permissions(user_department, user_position)
        else:
            print("Employee not found.")

    def validate_permissions(self, user_department, user_position, dataJson):
        employee_number = self.employee_id.get()

        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department) and permissions.is_position_allowed(user_position):
            if permissions.is_technician(user_position):
                self.show_tech_dashboard(
                    user_department, user_position, dataJson)
            elif permissions.is_operator(user_position):
                print(f"{user_position} is an operator.")
                self.show_operator_dashboard(
                    user_department, user_position, dataJson)
                self.log_activity(
                    logging.INFO, f'User login successful. ID NUM: {employee_number}')

            else:
                self.log_activity(
                    logging.INFO, f'User login unsuccessful. ID NUM: {employee_number}')

                showerror(title='Login Failed',
                          message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

        else:
            self.log_activity(
                logging.INFO, f'User login unsuccessful. ID NUM: {employee_number}')
            showerror(title='Login Failed',
                      message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", 'settings.json')
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

    def checking_allowed_user(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "config")
        log_file_path = os.path.join(log_folder, 'settings.json')
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()
                result = log_content['allowed_users']
        except FileNotFoundError as e:
            print(e)

    def init_logging(self):
        log_file = 'data/logs/activity_log.txt'
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
        # print(f'Logging to {log_file}')-

    def log_activity(self, level, message):
        logging.log(level, message)

    def show_operator_dashboard(self, user_department, user_position, data_json):
        OpeDashboard = tk.Toplevel(root)
        ope_dashboard = OperatorDashboard(
            OpeDashboard, user_department, user_position, data_json)
        root.withdraw()

    def show_tech_dashboard(self, user_department, user_position, dataJson):
        techDashboard = Toplevel(root)
        tech_dashboard = TechnicianDashboard(
            techDashboard, user_department, user_position, dataJson)
        root.withdraw()

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')

        dateNTime = current_date + ' ' + current_time
        self.date_time["text"] = 'DATETIME: ' + dateNTime
        root.after(1000, self.update_clock)

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
            self.statusHere["text"] = getStatus
            self.status_card()
        self.root.after(1000, self.update_status)

    def status_card(self):
        self.time_data()
        self.get_data.calculate_oee
        self.charts()
        self.delete_file_data()
        self.get_data.calculate_total_productive_time()

    def delete_file_data(self):
        filename = os.path.join(
            self.get_script_directory(), "data", 'time.csv')
        try:
            with open(filename, 'w') as file:
                file.truncate(0)

        except IOError:
            print(f"Error deleting data in '{filename}'.")

    def update_logs(self):
        log_file_path = os.path.join(
            self.get_script_directory(), 'data/logs', 'activity_log.txt')
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()
            lines = log_content.split('\n')
            last_5_logs = '\n'.join(lines[-6:])
            self.logs_message["text"] = last_5_logs

        except FileNotFoundError:
            self.logs["text"] = "Log file not found."
        root.after(50000, self.update_logs)

    def time_data(self):
        self.total_remaining_qty["text"] = f"TOTAL PROCESS : {self.total_running_qty}"
        self.productive_hrs["text"] = f"PRODUCTIVE HRS : {self.get_productive_hrs}"
        self.available_hrs["text"] = f"AVAILABLE HRS : {self.get_available_hrs}"
        self.total_quantity_to_process[
            "text"] = f"QUANTITY PROCESSED : {self.total_remaining_qty_value}"

    def create_total_qty_graph(self):
        if self.total_running_qty == 0 and self.total_remaining_qty_value == 0:
            return None

        result_qty = self.total_running_qty - self.total_remaining_qty_value
        data = [self.total_remaining_qty_value, result_qty]
        labels = ['QUANTITY COMPLETED', 'PROCESS QUANTITY']
        colors = ['#4CAF50', '#e74c3c']
        explode = (0.05, 0)

        figure = Figure(figsize=(5, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                 startangle=90, pctdistance=0.85, explode=explode)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plot.add_artist(centre_circle)

        center_text = 'QUANTITY'
        plot.text(0, 0, center_text, va='center', ha='center', fontsize=12)

        plot.axis('equal')
        # plot.set_title('QUANTITY GRAPH')

        plot.legend(loc='upper center', labels=labels, fontsize='small')

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)
        self.root.after(50000, self.create_total_qty_graph)
        return img

    def create_oee_graph(self):
        calculated_oee = self.calculate_oee()
        calculated_oee = max(0, min(calculated_oee, 100))

        total = 100 - calculated_oee
        data = [calculated_oee, total]
        labels = ['EFFECTIVENESS', 'INEFFECTIVENESS']
        colors = ['#4CAF50', '#e74c3c']
        explode = (0.05, 0)

        figure = Figure(figsize=(5, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                 startangle=90, pctdistance=0.85, explode=explode)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plot.add_artist(centre_circle)

        center_text = 'OEE'
        plot.text(0, 0, center_text, va='center', ha='center', fontsize=12)
        plot.legend(loc='upper center', labels=labels, fontsize='small')

        plot.axis('equal')
        # plot.set_title('OEE GRAPH')

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)
        self.root.after(50000, self.create_oee_graph)
        return img

    def create_line_chart(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        days = np.arange(1, 8)
        values = [10, 0, 2, 11, 4, 2, 15]

        ax.plot(days, values, marker='o', label="7-Day Data")
        ax.set_xlabel("Day")
        ax.set_ylabel("Value")
        ax.set_title("CPK GRAPH")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        img = self.convert_figure_to_photoimage(canvas)
        return img

    def convert_figure_to_photoimage(self, fig_canvas):
        buf = fig_canvas.buffer_rgba()
        img_data = buf.tobytes()  # Convert memoryview to bytes
        img = Image.frombytes("RGBA", fig_canvas.get_width_height(), img_data)
        return ImageTk.PhotoImage(image=img)

    def time_data(self):
        self.total_remaining_qty["text"] = f"TOTAL TO PROCESS : {self.total_running_qty}"
        self.productive_hrs["text"] = f"PRODUCTIVE HOURS : {self.get_productive_hrs}"
        self.available_hrs["text"] = f"AVAILABLE HOURS : {self.get_data.get_available_hrs()}"
        self.total_quantity_to_process[
            "text"] = f"QUANTITY PROCESSED : {self.total_remaining_qty_value}"
        self.downtime["text"] = f"DOWNTIME : {self.get_downtime_hrs}"
        # self.root.after(50000, self.time_data)
        
        self.label_update_id = self.root.after(self.update_interval, self.time_data)

    def charts(self):
        self.chart_img = self.create_oee_graph()
        self.total_img = self.create_total_qty_graph()
        self.line_img = self.create_line_chart()
        if self.oee_graph is not None:
            self.oee_graph.configure(image=self.chart_img)
        if self.quantity_graph is not None:
            self.quantity_graph.configure(image=self.total_img)
        if self.cpk_graph is not None:
            self.cpk_graph.configure(image=self.line_img)
            
        self.chart_update_id = self.root.after(self.update_interval, self.charts)

    def auto_update(self):
        """
        CAN BE ENABLED, BUT IT CAN EAT A LOT OF RESOURCES
        """
        pass
        # self.time_data()
        # self.get_data.calculate_oee
        # self.create_oee_graph()
        # self.create_line_chart()
        # self.root.after(50000, self.auto_update)

    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()
        if ticket_present:
            print(f"==>> ticket_present: {ticket_present}")
            self.ticket["text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
            if not self.downtime_started:
                print("==>> go here:")
                self.downtime_started = True
                print(f"==>> downtime_started: {self.downtime_started}")
                self.log_event("DOWNTIME_START")
                print("==>> DOWNTIME_START: ")
        else:
            if self.downtime_started:
                self.downtime_started = False
                self.log_event("DOWNTIME_STOP")
            self.ticket.destroy()

    def log_event(self, msg):
        current_time = datetime.datetime.now()
        print(f"==>> current_time: {current_time}")
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open('data/logs/downtime.csv', mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def load_downtime_state(self):
        try:
            with open('config/downtime_state.json', 'r') as state_file:
                state = json.load(state_file)
                return state.get('downtime_started', False)
        except FileNotFoundError:
            return False

    def save_downtime_state(self):
        with open('config/downtime_state.json', 'w') as state_file:
            json.dump({'downtime_started': self.downtime_started}, state_file)


# receiver.sio.wait()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.iconbitmap("config/ico/favicon.ico")
    root.mainloop()
