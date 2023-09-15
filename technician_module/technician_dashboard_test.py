import json
import os
import tkinter as tk
from tkinter import Scrollbar, Text
import tkinter.font as tkFont
import csv
from datetime import datetime
import logging
from io import BytesIO
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
# from ttkbootstrap.constants import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


import requests
from PIL import Image, ImageTk

# from technician_module.technician_utils.downtime_type import DownTimeType
from utils.ticket_status import TicketChecker
from utils.status_update import StatusUpdate


class TechnicianDashboardTest:
    def __init__(self, root, user_department, user_position, dataJson, assets_dir):
        self.root = root
        self.assets_dir = assets_dir
        # self.root.attributes('-fullscreen',True)
        # self.root.attributes('-topmost', True)
        ## GLOBAL VARIABLE ##
        data = dataJson['data']
        self.extracted_user_department = data[0]
        self.extracted_fullname = data[1]
        self.extracted_employee_no = data[2]
        self.extracted_employee_department = data[3]
        self.extracted_photo_url = data[4]
        self.extracted_possition = data[5]
        self.downtime_type = ''
        self.log_configured = False 
        self.root = root
        self.root.geometry("1024x600")
        self.root.configure(bg="#FBFBFB")
        self.ticket_logging()
        

        if self.extracted_photo_url == False or self.extracted_photo_url is None:
            image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        else:

            image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"

        response = requests.get(image_url)
        pil_image = Image.open(BytesIO(response.content))
        desired_width = 83
        desired_height = 74
        pil_image = pil_image.resize(
            (desired_width, desired_height), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(pil_image)

        button1 = "assets/frame_technician/sign_out.png"
        button2 = "assets/frame_technician/ticket.png"

        img_1 = "assets/frame_technician/image_1.png"
        img_2 = "assets/frame_technician/image_2.png"
        img_3 = "assets/frame_technician/image_3.png"

        button1_pill = Image.open(button1)
        button2_pill = Image.open(button2)

        image_1 = Image.open(img_1)
        image_2 = Image.open(img_2)
        image_3 = Image.open(img_3)

        self.tk_btn_1 = ImageTk.PhotoImage(button1_pill)
        self.tk_btn_2 = ImageTk.PhotoImage(button2_pill)

        self.tk_image_1 = ImageTk.PhotoImage(image_1)
        self.tk_image_2 = ImageTk.PhotoImage(image_2)
        self.tk_image_3 = ImageTk.PhotoImage(image_3)

        self.canvas = Canvas(
            self.root,
            bg="#FBFBFB",
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
            outline=""
        )

        # self.image_image_1 = self.canvas.create_image(
        #     64.0,
        #     47.0,
        #     image=self.tk_image_1
        # )

        self.image_image_2 = self.canvas.create_image(
            64.0,
            47.0,
            image=self.tk_image_2
        )

        self.image_image_3 = self.canvas.create_image(
            728.0,
            48.0,
            image=self.image
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

        # self.image_image_3 = PhotoImage(
        #     file=self.relative_to_assets("image_3.png"))
        # self.image_3 = self.canvas.create_image(
        #     728.0,
        #     48.0,
        #     image=self.image_image_3
        # )

        self.canvas.create_rectangle(
            31.0,
            181.0,
            506.0,
            581.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_rectangle(
            522.0,
            181.0,
            994.0,
            581.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_text(
            769.0,
            39.0,
            anchor="nw",
            text=" " + self.extracted_fullname,
            fill="#343A40",
            font=("Roboto Bold", 20 * -1)
        )

        # Create a Label widget for displaying and wrapping text
        # Adjust wraplength as needed
        self.log_text = tk.Label(
            root, text="Your text goes here", wraplength=900, font=("RobotoRoman Regular", 18)
        )
        self.log_text.grid(row=2, column=5)
        # Create a canvas window to add the Label widget to the canvas
        self.canvas_window = self.canvas.create_window(
            560.0,
            214.0,
            anchor="nw",
            window=self.log_text,
        )

        self.label1 = self.canvas.create_text(
            400.0,
            214.0,
            anchor="ne",
            # text="label 1",
            fill="#000000",
            font=("RobotoRoman Regular", 20 * -1)
        )

        self.accept_btn = tk.Button(
            self.root, text="ACCEPT TICKET", command=self.accept_ticket)
        self.button_window = self.canvas.create_window(
            80.0, 214.0, window=self.accept_btn, anchor="nw")

        self.button_2 = tk.Button(
            self.root,
            image=self.tk_btn_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )
        self.button_2.place(
            x=326.0,
            y=115.0,
            width=372.0,
            height=51.0
        )

        ## FUNCTIONS ##

        self.ticket_checking_var()
        self.verify_ticket_status()
        

        ## END ##

        self.center_window()
        self.root.resizable(False, False)

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

        # if self.extracted_photo_url == False or self.extracted_photo_url is None:
        #     image_url = "https://www.freeiconspng.com/uploads/no-image-icon-15.png"
        # else:

        #     image_url = f"http://hris.teamglac.com/{self.extracted_photo_url}"

        # response = requests.get(image_url)
        # pil_image = Image.open(BytesIO(response.content))
        # desired_width = 83
        # desired_height = 60
        # pil_image = pil_image.resize(
        #     (desired_width, desired_height), Image.ANTIALIAS)

        # self.image = ImageTk.PhotoImage(pil_image)

        ## FUNCTIONS ##

        # self.tech_gui()
        # self.update_status()
        # self.verify_ticket_status()

        ## END ##

        # setting title

        # setting window size

    # def logout(self):
    #     response = messagebox.askyesno(
    #         "Logout", "Are you sure you want to logout?")
    #     if response:
    #         self.root.destroy()
    #         os.system("python index.py")

    # def update_status(self):
    #     statusHere = StatusUpdate('data/logs/logs.csv')
    #     getStatus = statusHere.get_last_log_value()
    #     if getStatus is None or False:
    #         self.statusHere["bg"] = "#ffffff"
    #         self.statusHere["text"] = ''
    #     elif getStatus == 'ONLINE':
    #         self.statusHere["bg"] = "#4CAF50"
    #         self.statusHere["fg"] = "#ffffff"
    #         self.statusHere["text"] = getStatus
    #     else:
    #         self.statusHere["bg"] = "#cc0000"
    #         self.statusHere["fg"] = "#ffffff"
    #         self.statusHere["text"] = getStatus
    #     self.root.after(5000, self.update_status)

    # def verify_ticket_status(self):
    #     ticket_inspector = TicketChecker()
    #     ticket_present = ticket_inspector.checking()

    #     if ticket_present:
    #         self.ticket_checking["text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
    #     else:
    #         self.ticket_checking.destroy()

    # def read_machno(self):
    #     with open("data/main.json", "r") as json_file:
    #         data = json.load(json_file)
    #         extracted_data = []
    #         extracted_machno = data["machno"]
    #     return extracted_machno

    # def ticket_checking_var(self):
    #     lams_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
    #     response = requests.get(lams_url)
    #     if response.status_code == 200:
    #         data = response.json()
    #         result = data["result"]
    #         res = 0
    #         machno_alerts = []
    #         machno_status = []
    #         self.downtime_type = []
    #         for x in result:
    #             if x.get("MACH201_MACHNO") == self.read_machno():
    #                 res = 1
    #                 machno_alerts.append(x["DTNO"])
    #                 machno_status.append(x["STATUS"])
    #                 self.downtime_type.append(x["DOWNTIME_TYPE"])  # Append to the list
    #                 break
    #             if res == 1:
    #                 self.get_downtime_type('1')
    #                 self.machno_string = ", ".join(machno_alerts)
    #                 self.machno_string_status = ", ".join(machno_status)

    #     self.root.after(15000, self.ticket_checking_var)

    # def get_downtime_type(self, downtimeType):
    #     print(f"==>> downtimeType: {downtimeType}")
    #     cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
    #     response = requests.get(cmms_url)
    #     data = response.json()
    #     result = data["result"]
    #     print(f"==>> result: {result}")
    #     if response.status_code == 200:
    #         for item in result:
    #             if downtimeType in item['ID']:
    #                 downtime_type = item["DOWNTIME_TYPE"]
    #                 print(f"==>> downtime_type: {downtime_type}")
    #                 break
    #             else:
    #                 print('else')
    #     print(f"==>> downtime_type: {downtime_type}")

    def accept_ticket(self):
        url = f'http://lams.teamglac.com/lams/api/job_order/accept_jo.php?empno={self.extracted_employee_no}&dtno={self.machno_string}'
        # print(f"💻==>> url: {url}")
        try:
            r = requests.post(url)
            r.raise_for_status()  # Raise an exception for HTTP errors

            value_url = r.json()

            # Check the 'status' key in the JSON response and display appropriate messages
            if 'flag' in value_url:
                if value_url['flag'] == False:
                    accept_res = value_url['msg']
                    showinfo("Warning", f"{accept_res}")
                    self.log_ticket_activity(
                logging.INFO, f'{accept_res}.. ID NUM: {self.extracted_employee_no,}')
                else:
                    showinfo("Success", f"Job order accepted successfully.")
                    self.log_ticket_activity(
                logging.INFO, f'Job order accepted successfully.. ID NUM: {self.extracted_employee_no,}')
                    self.ticket_checking_var()
            else:
                showerror("Error", "Invalid response format from the server.")
                self.log_ticket_activity(
                logging.INFO, f'Invalid response format from the server... ID NUM: {self.extracted_employee_no,}')
        except requests.RequestException as e:
            print(f"Error in creating job order: {e}")
            showerror("Error", "Error in creating job order.")
            self.log_ticket_activity(
                logging.INFO, f'Error in creating job order... ID NUM: {self.extracted_employee_no,}')
            
    def ticket_logging(self):
        if not self.log_configured:
            log_file = 'data/logs/accepted_ticket.txt'
            logging.basicConfig(filename=log_file, level=logging.INFO,
                                format='[%(asctime)s] %(levelname)s: %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
            print(f'Logging to {log_file}')
            self.log_configured = True  # Set the flag to True after configuring logging
        
        
    def log_ticket_activity(self, level, message):
        logging.log(level, message)


    def signout(self):
        response = messagebox.askyesno(
            "Sign out", "Are you sure you want to Sign out?")
        if response:
            self.root.destroy()
            os.system("python index.py")

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
                    self.downtime_type.append(x["DOWNTIME_TYPE"])
                    break
            if res == 1:
                # self.get_downtime_type('1')
                self.machno_string = ", ".join(machno_alerts)
                self.machno_string_status = ", ".join(machno_status)
                print(
                    f"==>> machno_string_status: {self.machno_string_status}")
                print(f"==>> machno_string: {self.machno_string}")

                if self.machno_string is None or self.machno_string_status is None:
                    self.new_text = 'DT NO: ' + self.machno_string + \
                        ' ' + '|| ' + self.machno_string_status
                    self.canvas.itemconfigure(self.label1, text=self.new_text)
                    self.accept_btn.place_forget()
                else:
                    self.new_text = 'DT NO: ' + self.machno_string + \
                        ' ' + '|| ' + self.machno_string_status
                    self.canvas.itemconfigure(self.label1, text=self.new_text)

    # def get_downtime_type(self, downtimeType):
    #     print(f"==>> downtimeType: {downtimeType}")
    #     cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
    #     response = requests.get(cmms_url)
    #     data = response.json()
    #     result = data["result"]
    #     print(f"==>> result: {result}")
    #     if response.status_code == 200:
    #         for item in result:
    #             if downtimeType in item['ID']:
    #                 downtime_type = item["DOWNTIME_TYPE"]
    #                 print(f"==>> downtime_type: {downtime_type}")
    #                 break
    #             else:
    #                 print('else')
    #     print(f"==>> downtime_type: {downtime_type}")

    def disable_label(self):
        self.button_2.place_forget()

    def enable_label(self):
        self.button_2.place(x=326.0, y=115.0, width=372.0, height=51.0)

    def verify_ticket_status(self):
        ticket_inspector = TicketChecker()
        ticket_present = ticket_inspector.checking()

        if ticket_present:
            self.enable_label()
        else:
            self.disable_label()


if __name__ == "__main__":
    root = tk.Tk()
    app = TechnicianDashboardTest(root)
    root.mainloop()