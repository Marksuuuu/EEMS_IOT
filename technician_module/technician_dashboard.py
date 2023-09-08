import json
import os
import tkinter as tk
import tkinter.font as tkFont
from io import BytesIO
from tkinter import messagebox

import requests
from PIL import Image, ImageTk

from utils.status_update import StatusUpdate
# from technician_module.technician_utils.downtime_type import DownTimeType
from utils.ticket_status import TicketChecker


# from ttkbootstrap.constants import *


class TechnicianDashboard:
    def __init__(self, root, user_department, user_position, dataJson):

        ## GLOBAL VARIABLE ##

        data = dataJson['data']
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        self.downtime_type = ''
        self.root = root

        # self.notes = ''
        # self.poppedData = self.downtime_type.pop()
        # print(f"==>> poppedData: {self.poppedData}")
        # if self.poppedData.title() == 'Setup':
        #     self.notes = """ PLEASE GO AND MAKE A SETUP!"""
        #     print(f"==>> notes: {self.notes}")
        # elif self.poppedData.title() == 'Conversion':
        #     self.notes = """ PLEASE GO AND MAKE A CONVERTION!"""
        #     print(f"==>> notes: {self.notes}")
        # elif self.poppedData.title() == 'Repair':
        #     self.notes = """ PLEASE GO AND MAKE A REPAIR!"""
        #     print(f"==>> notes: {self.notes}")
        # elif self.poppedData.title() == 'Others':
        #     self.notes = """ PLEASE CHECK!"""
        #     print(f"==>> notes: {self.notes}")
        # else:
        #     self.notes = ""
        #     print(f"==>> notes: {self.notes}")

        if self.extracted_photo_url == False or self.extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:

            image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 60
        pil_image = pil_image.resize(
            (desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        ## FUNCTIONS ##

        self.ticket_checking_var()
        self.tech_gui()
        self.update_status()
        self.verify_ticket_status()

        ## END ##

        # setting title

        root.title(
            f"TECHNICIAN DASHBOARD - {self.extracted_employee_no} -- POSSITION - {self.extracted_possition}")

        # setting window size

        width = 1800
        height = 1013
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

    def tech_gui(self):
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

        self.logout_btn = tk.Button(self.root)
        self.logout_btn["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times', size=16)
        self.logout_btn["font"] = ft
        self.logout_btn["fg"] = "#ffffff"
        self.logout_btn["justify"] = "center"
        self.logout_btn["text"] = "LOG ME OUT"
        self.logout_btn.place(x=1640, y=110, width=149, height=50)
        self.logout_btn["command"] = self.logout

        self.statusHere = tk.Label(self.root)
        self.statusHere["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times', size=52)
        self.statusHere["font"] = ft
        self.statusHere["fg"] = "#ffffff"
        self.statusHere["justify"] = "center"
        self.statusHere["text"] = "OFFLINE"
        self.statusHere.place(x=40, y=10, width=359, height=106)

        self.ticket_checking = tk.Label(self.root)
        self.ticket_checking["bg"] = "#ffb800"
        self.ticket_checking["cursor"] = "circle"
        ft = tkFont.Font(family='Times', size=13)
        self.ticket_checking["font"] = ft
        self.ticket_checking["fg"] = "#000000"
        self.ticket_checking["justify"] = "center"
        self.ticket_checking[
            "text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        self.ticket_checking.place(x=460, y=10, width=750, height=37)

    def logout(self):
        response = messagebox.askyesno(
            "Logout", "Are you sure you want to logout?")
        if response:
            self.root.destroy()
            os.system("python index.py")

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
        self.root.after(5000, self.update_status)

    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()

        if ticket_present:
            self.ticket_checking[
                "text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        else:
            self.ticket_checking.destroy()

    def read_machno(self):
        with open("data/main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_data = []
            extracted_machno = data["machno"]
        return extracted_machno

    def ticket_checking_var(self):
        lams_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
        response = requests.get(lams_url)
        if response.status_code == 200:
            data = response.json()
            result = data["result"]
            res = 0
            machno_alerts = []
            machno_status = []
            self.downtime_type = []
            for x in result:
                if x.get("MACH201_MACHNO") == self.read_machno():
                    res = 1
                    machno_alerts.append(x["DTNO"])
                    machno_status.append(x["STATUS"])
                    self.downtime_type.append(x["DOWNTIME_TYPE"])  # Append to the list
                    break
                if res == 1:
                    self.get_downtime_type('1')
                    self.machno_string = ", ".join(machno_alerts)
                    self.machno_string_status = ", ".join(machno_status)

        self.root.after(15000, self.ticket_checking_var)

    def get_downtime_type(self, downtimeType):
        print(f"==>> downtimeType: {downtimeType}")
        cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
        response = requests.get(cmms_url)
        data = response.json()
        result = data["result"]
        print(f"==>> result: {result}")
        if response.status_code == 200:
            for item in result:
                if downtimeType in item['ID']:
                    downtime_type = item["DOWNTIME_TYPE"]
                    print(f"==>> downtime_type: {downtime_type}")
                    break
                else:
                    print('else')
        print(f"==>> downtime_type: {downtime_type}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
