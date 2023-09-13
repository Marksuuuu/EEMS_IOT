import csv
# from ttkbootstrap.constants import *
import datetime
import json
import logging
import os
import re
import time
import tkinter as tk
import tkinter.font as tkFont
import uuid
from datetime import datetime
from tkinter import Toplevel
from tkinter import messagebox
from tkinter.messagebox import showerror
import datetime
import matplotlib.pyplot as plt
import numpy as np
import requests
import socketio
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


## IMPORTS ##


from operator_module.operator_dashboard_test import OperatorDashboardTest
from technician_module.technician_dashboard_test import TechnicianDashboardTest
# from utils.trigger_downtime import TriggerDowntime
from socketio_utils.socketio_manager import SocketIOManager
from utils.quantity_data import QuantityData
from utils.status_update import StatusUpdate
from utils.ticket_status import TicketChecker
from utils.time_data import TimeData


# from utils.trigger_downtime import TriggerDowntime

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


class DashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.configure(bg="#E5E5E5")
        current_year = datetime.datetime.now().year
        self.root.title(f"EEMS_IOT - © {current_year}")

        ## GLOBAL VARIABLE ##

        button1 = "assets\\frame_dashboard\\button_1.png"
        button2 = "assets\\frame_technician\\ticket.png"

        img_1 = "assets\\frame_dashboard\\image_1.png"
        img_2 = "assets\\frame_dashboard\\image_2.png"
        img_3 = "assets\\frame_dashboard\\image_3.png"
        img_4 = "assets\\frame_dashboard\\image_4.png"
        img_5 = "assets\\frame_dashboard\\image_5.png"
        img_6 = "assets\\frame_dashboard\\image_6.png"
        img_7 = "assets\\frame_dashboard\\image_7.png"
        img_8 = "assets\\frame_dashboard\\image_8.png"
        img_9 = "assets\\frame_dashboard\\image_9.png"
        img_10 = "assets\\frame_dashboard\\image_10.png"
        img_11 = "assets\\frame_dashboard\\image_11.png"
        img_12 = "assets\\frame_dashboard\\image_12.png"
        img_13 = "assets\\frame_dashboard\\image_13.png"
        img_14 = "assets\\frame_dashboard\\image_14.png"

        entry1 = "assets\\frame_dashboard\\entry_1.png"

        button1_pill = Image.open(button1)
        button2_pill = Image.open(button2)

        self.tk_btn_1 = ImageTk.PhotoImage(button1_pill)
        self.tk_btn_2 = ImageTk.PhotoImage(button2_pill)

        entry_1 = Image.open(entry1)

        image_1 = Image.open(img_1)
        image_2 = Image.open(img_2)
        image_3 = Image.open(img_3)
        image_4 = Image.open(img_4)
        image_5 = Image.open(img_5)
        image_6 = Image.open(img_6)
        image_7 = Image.open(img_7)
        image_8 = Image.open(img_8)
        image_9 = Image.open(img_9)
        image_10 = Image.open(img_10)
        image_11 = Image.open(img_11)
        image_12 = Image.open(img_12)
        image_13 = Image.open(img_13)
        image_14 = Image.open(img_14)

        self.tk_entry_1 = ImageTk.PhotoImage(entry_1)

        self.tk_image_1 = ImageTk.PhotoImage(image_1)
        self.tk_image_2 = ImageTk.PhotoImage(image_2)
        self.tk_image_3 = ImageTk.PhotoImage(image_3)
        self.tk_image_4 = ImageTk.PhotoImage(image_4)
        self.tk_image_5 = ImageTk.PhotoImage(image_5)
        self.tk_image_6 = ImageTk.PhotoImage(image_6)
        self.tk_image_7 = ImageTk.PhotoImage(image_7)
        self.tk_image_8 = ImageTk.PhotoImage(image_8)
        self.tk_image_9 = ImageTk.PhotoImage(image_9)
        self.tk_image_10 = ImageTk.PhotoImage(image_10)
        self.tk_image_11 = ImageTk.PhotoImage(image_11)
        self.tk_image_12 = ImageTk.PhotoImage(image_12)
        self.tk_image_13 = ImageTk.PhotoImage(image_13)
        self.tk_image_14 = ImageTk.PhotoImage(image_14)
        self.total_img = self.create_total_qty_graph()
        self.oee_img = self.create_oee_graph()
        self.line_graph_img = self.create_line_chart()
        self.downtime_started = self.load_downtime_state()

        self.quantity_data = QuantityData("../data")
        self.get_data = TimeData('../data')
        self.ticket_inspector = TicketChecker()
        self.ticket_present = self.ticket_inspector.checking()
        # self.sio_manager = SocketIOManager()
        # self.receiver = ReceiveAndRequest(self.socketio_path())
        self.total_running_qty = self.quantity_data.total_running_qty()
        # self.calculate_oee = self.get_data.calculate_oee
        self.total_remaining_qty_value = self.quantity_data.total_remaining_qty()
        self.get_available_hrs = self.get_data.get_available_hrs()
        self.get_productive_hrs = self.get_data.calculate_total_productive_time()
        self.get_downtime_hrs = self.get_data.calculate_total_downtime()
        self.get_idle_hrs = self.get_data.calculate_total_idle()

        # if self.oee_graph is not None:
        #     self.oee_graph.configure(image=self.chart_img)
        # if self.quantity_graph is not None:
        #     self.quantity_graph.configure(image=self.total_img)
        # if self.cpk_graph is not None:
        #     self.cpk_graph.configure(image=self.line_img)

        ## FUNCTIONS ##

        self.create_gui_elements()
        self.update_clock()
        self.update_logs()
        self.update_status()
        self.verify_ticket_status()
        self.save_downtime_state()
        self.makeCenter()
        self.mch_label()
        self.checking_ticket()

        ## END ##

    def makeCenter(self):
        self.width = 1024
        self.height = 600
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth -
                                                              self.width) / 2, (self.screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def create_gui_elements(self):
        self.canvas = Canvas(
            self.root,
            bg="#E5E5E5",
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
            10.0,
            282.0,
            86.97332763671875,
            fill="#D3F9D8",
            outline="")

        self.image_1 = self.canvas.create_image(
            516.0,
            49.0,
            image=self.tk_image_1
        )

        self.image_2 = self.canvas.create_image(
            872.0,
            49.0,
            image=self.tk_image_2
        )

        entry_bg_1 = self.canvas.create_image(
            533.5,
            50.0,
            image=self.tk_entry_1
        )
        self.employee_id = Entry(
            self.root,
            bd=0,
            bg="#EFEFEF",
            fg="#000716",
            highlightthickness=0,
            font=("arial", 30),
            justify='center'  # Set text alignment to center
        )

        self.employee_id.place(
            x=378.0,
            y=28.0,
            width=311.0,
            height=42.0
        )

        self.employee_id.bind("<KeyRelease>", self.validate_employee_number)

        image_3 = self.canvas.create_image(
            782.0,
            48.0,
            image=self.tk_image_3
        )

        self.clock = self.canvas.create_text(
            806.0,
            38.0,
            anchor="nw",
            fill="#343A40",
            font=("Roboto Regular", 16 * -1)
        )

        image_4 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.tk_image_4
        )

        image_5 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.tk_image_5

        )

        image_6 = self.canvas.create_image(
            512.0,
            259.0,
            image=self.tk_image_6
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

        image_7 = self.canvas.create_image(
            167.0,
            259.0,
            image=self.tk_image_7
        )

        image_8 = self.canvas.create_image(
            167.0,
            260.0,
            image=self.oee_img
        )

        image_9 = self.canvas.create_image(
            340.0,
            509.0,
            image=self.tk_image_9
        )

        self.machine_data_lbl = self.canvas.create_text(
            24.0,
            442.0,
            anchor="nw",
            fill="#343A40",
            font=("Roboto Medium", 20 * -1)
        )

        image_10 = self.canvas.create_image(
            855.0,
            509.0,
            image=self.tk_image_10
        )

        image_11 = self.canvas.create_image(
            856.0,
            259.0,
            image=self.tk_image_11
        )

        self.canvas.create_text(
            700.0,
            435.0,
            anchor="nw",
            # text="LOGS",
            fill="#343A40",
            width=100,
            font=("Roboto Medium", 14 * -1)
        )

        self.canvas.create_text(
            689.0,
            112.0,
            anchor="nw",
            text="Total Quantity",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1)
        )

        self.canvas.create_text(
            0.0,
            112.0,
            anchor="nw",
            text="Overall Equipment Effectiveness",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1),
        )

        self.canvas.create_text(
            345.0,
            112.0,
            anchor="nw",
            text="Process Capability Index",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1)
        )

        image_12 = self.canvas.create_image(
            362.0,
            49.0,
            image=self.tk_image_12
        )

        self.button_1 = Button(
            image=self.tk_btn_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        image_13 = self.canvas.create_image(
            871.0,
            263.0,
            image=self.total_img

        )

        image_14 = self.canvas.create_image(
            512.0,
            264.0,
            image=self.line_graph_img
        )

        self.set_logs = self.canvas.create_text(
            709.0,
            435.0,
            anchor="nw",
            fill="#343A40",
            font=("Roboto Medium", 8 * -1)
        )

        # Add the rest of your GUI elements here

    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')

        dateNTime = current_date + ' ' + current_time
        self.canvas.itemconfig(self.clock, text=dateNTime)
        self.root.after(1000, self.update_clock)

    def create_total_qty_graph(self):
        self.quantity_data = QuantityData("../data")
        if self.quantity_data.total_running_qty() == 0 and self.quantity_data.total_remaining_qty() == 0:
            return None

        result_qty = self.quantity_data.total_running_qty(
        ) - self.quantity_data.total_remaining_qty()
        data = [self.quantity_data.total_remaining_qty(), result_qty]
        labels = ['', '']
        colors = ['#4CAF50', '#e74c3c']
        explode = (0.05, 0)

        figure = Figure(figsize=(3, 2), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        autotexts = plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                             startangle=90, pctdistance=0.85, explode=explode)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plot.add_artist(centre_circle)

        plot.set_facecolor('none')
        plot.axis('equal')

        autopct_values = [f'{p}' for p in autotexts]
        legend_labels = ['QUANTITY COMPLETED', 'PROCESS QUANTITY']

        # Move the legend outside the plot
        plot.legend(legend_labels, loc='center right',
                    bbox_to_anchor=(1, 0.5), fontsize='small')

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)

        return img

    def create_oee_graph(self):
        self.get_data = TimeData('../data')
        calculated_oee = self.get_data.calculate_oee()
        calculated_oee = max(0, min(calculated_oee, 100))

        total = 100 - calculated_oee
        data = [calculated_oee, total]
        labels = ['', '']
        colors = ['#4CAF50', '#e74c3c']
        explode = (0.05, 0)

        figure = Figure(figsize=(3, 2), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        autotexts = plot.pie(data, labels=labels, colors=colors, autopct='%1.1f%%',
                             startangle=90, pctdistance=0.85, explode=explode)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plot.add_artist(centre_circle)

        plot.set_facecolor('none')
        plot.axis('equal')

        autopct_values = [f'{p}' for p in autotexts]
        legend_labels = ['EFFECTIVENESS', 'INEFFECTIVENESS']

        # Move the legend outside the plot
        plot.legend(legend_labels, loc='center right',
                    bbox_to_anchor=(1, 0.5), fontsize='small')

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            'RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img = ImageTk.PhotoImage(image=pil_image)

        return img

    def create_line_chart(self):
        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        days = np.arange(1, 8)
        values = [10, 0, 2, 11, 4, 2, 15]

        ax.plot(days, values, marker='o', label="7-Day Data")
        plt.rcParams.update({'font.size': 6})
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

    def update_logs(self):
        log_file_path = os.path.join(
            self.get_script_directory(), 'data/logs', 'activity_log.txt')
        try:
            with open(log_file_path, 'r') as file:
                log_content = file.read()
            lines = log_content.split('\n')
            last_5_logs = '\n'.join(lines[-16:])
            self.canvas.itemconfig(self.set_logs, text=last_5_logs)

        except FileNotFoundError:
            self.logs["text"] = "Log file not found."
        self.root.after(60000, self.update_logs)

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
            image=self.tk_image_5
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
            image=self.tk_image_4
        )

    def update_status(self):
        statusHere = StatusUpdate('data/logs/logs.csv')
        getStatus = statusHere.get_last_log_value()
        if getStatus is None or False:
            pass
        elif getStatus == 'ONLINE':
            self.online_status_card()
        else:
            self.offline_status_card()
            self.delete_file_data()
        self.root.after(1000, self.update_status)

    def disable_label(self):
        self.button_1.place_forget()

    def enable_label(self):
        self.button_1.place(
            x=689.0,
            y=553.0725708007812,
            width=335.0,
            height=45.92742919921875
        )
        
    def checking_ticket(self):
        pass
        # if self.ticket_present:
        #     pass
        # else:
        #     self.downtime_started = False
        # # self.root.after(1000, self.checking_ticket)

    def verify_ticket_status(self):
        if self.ticket_present:
            self.enable_label()
            if not self.downtime_started:
                self.downtime_started = True
                self.log_event("DOWNTIME_START")
        else:
            # print(f"💻==>> self.ticket_present: {self.ticket_present}")
            self.disable_label()
            if self.downtime_started:
                self.downtime_started = False
                self.log_event("DOWNTIME_STOP")

    def log_event(self, msg):
        current_time = datetime.datetime.now()
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
                            pass
                            # print(
                            #     "Employee data doesn't contain department or position.")
                    else:
                        pass
                        # print(
                        #     "Response data is not in the expected format (dictionary).")
                except KeyError:
                    pass
                    # print("Response data doesn't have expected keys.")
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
        self.employee_number = self.employee_id.get()

        permissions = self.load_permissions()
        if permissions.is_department_allowed(user_department) and permissions.is_position_allowed(user_position):
            if permissions.is_technician(user_position):
                self.show_tech_dashboard(
                    user_department, user_position, dataJson)
            elif permissions.is_operator(user_position):
                print(f"{user_position} is an operator.")
                self.show_operator_dashboard(
                    user_department, user_position, dataJson)
                data = {
                    "msg": f'User login successful. ID NUM: {self.employee_number}',
                    "emp_id": self.employee_number
                }
                sio.emit('activity_log', {
                    'data': data})
                self.log_activity(
                    logging.INFO,  f'User login successful. ID NUM: {self.employee_number}')
                sio.emit('activity_log', {'data': data})

            else:
                self.log_activity(
                    logging.INFO,  f'User login successful. ID NUM: {self.employee_number}')
                data = {
                    "msg": f"User's department or position is not allowed. Please check, Current Department / Position: {user_department} {user_position}",
                    "emp_id": self.employee_number
                }
                sio.emit('activity_log', {
                    'data': data})
                showerror(title='Login Failed',
                          message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}")

        else:
            self.log_activity(
                logging.INFO, f'User login unsuccessful. ID NUM: {self.employee_number}')
            data = {
                "msg": f"User's department or position is not allowed. Please check, Current Department / Position: {user_department} {user_position}",
                "emp_id": self.employee_number
            }
            sio.emit('activity_log', {
                     'data': data})
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
        OpeDashboard = tk.Toplevel(self.root)
        assets_dir = 'assets'
        ope_dashboard = OperatorDashboardTest(
            OpeDashboard, user_department, user_position, data_json, assets_dir)
        self.root.withdraw()

    def show_tech_dashboard(self, user_department, user_position, dataJson):
        techDashboard = Toplevel(self.root)
        assets_dir = 'assets'
        tech_dashboard = TechnicianDashboardTest(
            techDashboard, user_department, user_position, dataJson, assets_dir)
        self.root.withdraw()

    def mch_label(self):
        machine_details = f"""DOWNTIME HRS: \t\t{self.get_data.calculate_total_downtime()}\nPRODUCTIVE HRS: \t{self.get_productive_hrs}\nAVAIL HRS: \t\t{self.get_data.get_available_hrs()}\nTOTAL IDLE HRS: \t\t{self.get_idle_hrs}\nQTY PROCESSED: \t{self.total_remaining_qty_value}\nTTL QTY TO PROCESS: \t{self.total_running_qty} 
        """
        # print('test')
        self.canvas.itemconfig(self.machine_data_lbl, text=machine_details)
        self.root.after(1000, self.mch_label)

    def delete_file_data(self):
        idle = os.path.join(
            self.get_script_directory(), "data/logs", 'idle.csv')
        downtime = os.path.join(
            self.get_script_directory(), "data/logs", 'downtime.csv')
        productive_hrs = os.path.join(
            self.get_script_directory(), "data", 'time.csv')
        total_avail_hrs = os.path.join(
            self.get_script_directory(), "data/logs", 'logs.csv')
        try:
            with open(idle, 'w') as file:
                file.truncate(0)
            with open(productive_hrs, 'w') as file:
                file.truncate(0)
            with open(downtime, 'w') as file:
                file.truncate(0)
            with open(total_avail_hrs, 'w') as file:
                file.truncate(0)
        except IOError:
            print(f"Error deleting data in '{filename}'.")

    @sio.event
    def my_message(data):
        print('Message received with', data)
        toPassData = data['dataToPass']
        machno = data['machno']
        remove_py = re.sub('.py', '', filename)
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


sio.connect('http://10.0.2.150:8083')


if __name__ == "__main__":
    window = tk.Tk()
    window.resizable(False, False)
    app = DashboardGUI(window)
    window.iconbitmap("config/ico/favicon.ico")
    window.mainloop()
