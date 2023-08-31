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
from ttkbootstrap.constants import *

from operator_module.operator_dashboard import OperatorDashboard
from utils.quantity_data import QuantityData
from utils.status_update import StatusUpdate
from utils.time_data import TimeData
from utils.ticket_status import TicketChecker

sio = socketio.Client(reconnection=True, reconnection_attempts=5,
                      reconnection_delay=1, reconnection_delay_max=5)
client = str(uuid.uuid4())
filename = os.path.basename(__file__)
removeExtension = re.sub('.py', '', filename)


@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename, 'client': client})
    sio.emit('controller', {'machine_name': filename})
    sio.emit('client', {'machine_name': filename, 'client': client})


@sio.event
def disconnect():
    print('disconnected to server')


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
        self.total_running_qty = self.quantity_data.total_running_qty()
        self.calculate_oee = self.get_data.calculate_oee
        self.total_remaining_qty_value = self.quantity_data.total_remaining_qty()
        self.get_available_hrs = self.get_data.get_available_hrs()
        self.get_productive_hrs = self.get_data.calculate_total_productive_time()

        self.root = root

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
        self.total_remaining_qty = tk.Label(self.root)
        self.total_remaining_qty["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.total_remaining_qty["font"] = ft
        self.total_remaining_qty["fg"] = "#333333"
        self.total_remaining_qty["justify"] = "left"
        self.total_remaining_qty.place(x=20, y=900, width=580, height=90)

        self.productive_hrs = tk.Label(self.root)
        self.productive_hrs["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.productive_hrs["font"] = ft
        self.productive_hrs["fg"] = "#333333"
        self.productive_hrs["justify"] = "center"
        self.productive_hrs.place(x=20, y=700, width=580, height=90)

        self.cpk_graph = tk.Label(self.root)
        self.cpk_graph["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=10)
        self.cpk_graph["font"] = ft
        self.cpk_graph["fg"] = "#333333"
        self.cpk_graph["justify"] = "center"
        self.cpk_graph["text"] = "CPK"
        self.cpk_graph.place(x=20, y=130, width=580, height=550)

        self.available_hrs = tk.Label(self.root)
        self.available_hrs["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.available_hrs["font"] = ft
        self.available_hrs["fg"] = "#333333"
        self.available_hrs["justify"] = "left"
        self.available_hrs.place(x=20, y=800, width=580, height=90)

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
        self.quantity_graph["text"] = "label"
        self.quantity_graph.place(x=1200, y=130, width=580, height=550)

        self.total_quantity_to_process = tk.Label(self.root)
        self.total_quantity_to_process["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.total_quantity_to_process["font"] = ft
        self.total_quantity_to_process["fg"] = "#333333"
        self.total_quantity_to_process["justify"] = "left"
        self.total_quantity_to_process.place(
            x=610, y=700, width=580, height=90)

        self.GLabel_655 = tk.Label(self.root)
        self.GLabel_655["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.GLabel_655["font"] = ft
        self.GLabel_655["fg"] = "#333333"
        self.GLabel_655["justify"] = "center"
        self.GLabel_655["text"] = "IDLE"
        self.GLabel_655.place(x=610, y=800, width=580, height=90)

        self.GLabel_725 = tk.Label(self.root)
        self.GLabel_725["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.GLabel_725["font"] = ft
        self.GLabel_725["fg"] = "#333333"
        self.GLabel_725["justify"] = "center"
        self.GLabel_725["text"] = "DOWTIME"
        self.GLabel_725.place(x=610, y=900, width=580, height=90)

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

        self.GLabel_794 = tk.Label(self.root)
        self.GLabel_794["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=22)
        self.GLabel_794["font"] = ft
        self.GLabel_794["fg"] = "#333333"
        self.GLabel_794["justify"] = "center"
        self.GLabel_794.place(x=1480, y=10, width=300, height=60)
        
        self.ticket=tk.Label(root)
        self.ticket["bg"] = "#ffb800"
        self.ticket["cursor"] = "circle"
        ft = tkFont.Font(family='Times',size=9)
        self.ticket["font"] = ft
        self.ticket["fg"] = "#000000"
        self.ticket["justify"] = "left"
        self.ticket.place(x=1199,y=73,width=581,height=43)

    @sio.event
    def my_message(data):
        print('Message received with', data)
        toPassData = data['dataToPass']
        machno = data['machno']
        fileNameWithIni = 'main.json'
        folder_path = 'data'
        file_path = f'{folder_path}/{fileNameWithIni}'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, 'w') as file:
            data = {
                'machno': machno,
                'filename': remove_py,
                'data': toPassData
            }
            json.dump(data, file)
        sio.emit('my_response', {'response': 'my response'})

    @sio.event
    def getMatrixfromServer(data):
        print('Message received with', data)
        toPassData = data['dataToPass'][0]

        flattened_data = ', '.join(toPassData).replace("'", "")
        print(f"==>> toPassData: {flattened_data}")

        filename = 'matrix.csv'
        folder_path = 'data'
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                header_row = [f'data{i}' for i in range(
                    1, len(toPassData) + 1)]
                writer.writerow(header_row)

            writer.writerow(toPassData)

        sio.emit('my_response', {'response': 'my response'})

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

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
                            print("Employee data doesn't contain department or position.")
                    else:
                        print("Response data is not in the expected format (dictionary).")
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

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')

        dateNTime = current_date + ' ' + current_time
        self.GLabel_794["text"] = dateNTime
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
        self.root.after(5000, self.update_status)

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
            "text"] = f"QUANTITY TO PROCESS : {self.total_remaining_qty_value}"

    def create_total_qty_graph(self):
        if self.total_running_qty == 0 and self.total_remaining_qty_value == 0:
            return None

        result_qty = self.total_remaining_qty_value - self.total_running_qty
        data = [self.total_remaining_qty_value, self.total_running_qty]
        labels = ['REMAINING', 'TOTAL RUNNING QTY']
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
        labels = ['EFFECTIVENESS', 'NOT EFFECTIVE']
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

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)
        return img

    def charts(self):
        self.chart_image = self.create_oee_graph()
        self.total_img = self.create_total_qty_graph()
        if self.oee_graph is not None:
            self.oee_graph.configure(image=self.chart_image)
        if self.quantity_graph is not None:
            self.quantity_graph.configure(image=self.total_img)
            
    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()
        
        if ticket_present:
            self.ticket["text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        else:
            self.ticket.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.iconbitmap("config/ico/favicon.ico")
    root.mainloop()
