import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter.font as tkFont
import os
import csv
import json
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showwarning, showerror
import datetime
import importlib

from .mo_transaction import MOData
# from operator_module.operator_utils.controller import MakeCommand


class MoDetails:
    def __init__(
        self,
        root,
        extracted_fullname,
        extracted_employee_no,
        extracted_photo_url,
        extracted_username,
        data,
    ):
        # MO PROPERTIES
        # ///////////////////////////////////////////////////////////////
        root.title("MO")
        width = 1264
        height = 675
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

        self.root = root
        self.extracted_employee_no = extracted_employee_no
        self.extracted_photo_url = extracted_photo_url
        self.extracted_username = extracted_username
        self.extracted_fullname = extracted_fullname
        self.root.title("MO DETAILS")
        self.test_data = data

        self.customer = data[1]
        self.device = data[2]
        self.main_opt = data[3]
        self.package = data[4]
        self.running_qty = data[5]
        self.wip_entity_name = data[6]

        self.data_dict = {}

        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")
        self.currentDateTime = f"{date} {time}"

        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

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

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_folder = os.path.join(script_directory, "../../data")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.csv_file_path = os.path.join(self.log_folder, "time.csv")

        self.image = ImageTk.PhotoImage(pil_image)

        GLabel_841 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        GLabel_841["font"] = ft
        GLabel_841["fg"] = "#333333"
        GLabel_841["justify"] = "center"
        GLabel_841["text"] = self.main_opt
        GLabel_841.place(x=20, y=110, width=526, height=63)

        GLabel_932 = tk.Label(root)
        GLabel_932["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=18)
        GLabel_932["font"] = ft
        GLabel_932["fg"] = "#333333"
        GLabel_932["justify"] = "left"
        GLabel_932["text"] = f"Device : {data[2]}"
        GLabel_932.place(x=20, y=180, width=526, height=97)

        GLabel_771 = tk.Label(root)
        GLabel_771["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=18)
        GLabel_771["font"] = ft
        GLabel_771["fg"] = "#333333"
        GLabel_771["justify"] = "left"
        GLabel_771["text"] = f"Package : {data[4]}"
        GLabel_771.place(x=20, y=300, width=526, height=97)

        GLabel_146 = tk.Label(root)
        GLabel_146["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=18)
        GLabel_146["font"] = ft
        GLabel_146["fg"] = "#333333"
        GLabel_146["justify"] = "left"
        GLabel_146["text"] = f"Customer : {data[1]}"
        GLabel_146.place(x=20, y=420, width=526, height=97)

        GLabel_915 = tk.Label(root)
        # GLabel_915["bg"] = "#89d35f"
        GLabel_915["fg"] = "#333333"
        ft = tkFont.Font(family="Times", size=18)
        GLabel_915["font"] = ft
        GLabel_915["justify"] = "left"
        GLabel_915["text"] = f"MO Quantity : {data[5]}"
        GLabel_915.place(x=20, y=540, width=526, height=97)

        # lbl_remaining_qty=tk.Label(root)
        # lbl_remaining_qty["bg"] = "#ffffff"
        # ft = tkFont.Font(family='Times',size=18)
        # lbl_remaining_qty["font"] = ft
        # lbl_remaining_qty["fg"] = "#333333"
        # lbl_remaining_qty["justify"] = "left"
        # lbl_remaining_qty["text"] = f"Remaining MO Quantity : {data[5]}"
        # lbl_remaining_qty.place(x=450,y=540,width=526,height=97)

        GLabel_514 = tk.Label(root)
        ft = tkFont.Font(family="Times", size=24)
        GLabel_514["font"] = ft
        GLabel_514["fg"] = "#333333"
        GLabel_514["justify"] = "left"
        GLabel_514["text"] = extracted_fullname
        GLabel_514.place(x=820, y=20, width=424, height=87)

        GLabel_978 = tk.Label(root, image=self.image)
        ft = tkFont.Font(family="Times", size=10)
        GLabel_978["font"] = ft
        GLabel_978["fg"] = "#333333"
        GLabel_978["justify"] = "left"
        GLabel_978["text"] = "img"
        GLabel_978.place(x=680, y=20, width=120, height=87)

        self.start_btn = tk.Button(root)
        self.start_btn["bg"] = "#5fb878"
        ft = tkFont.Font(family="Times", size=23)
        self.start_btn["font"] = ft
        self.start_btn["fg"] = "#ffffff"
        self.start_btn["justify"] = "center"
        self.start_btn["text"] = "START"
        self.start_btn.place(x=1000, y=540, width=245, height=97)
        self.start_btn["command"] = self.start_command

        self.stop_btn = tk.Button(root)
        self.stop_btn["bg"] = "#cc0000"
        ft = tkFont.Font(family="Times", size=23)
        self.stop_btn["font"] = ft
        self.stop_btn["fg"] = "#f9f9f9"
        self.stop_btn["justify"] = "center"
        self.stop_btn["text"] = "STOP"
        self.stop_btn.place(x=1000, y=430, width=245, height=97)
        self.stop_btn.place_forget()
        self.stop_btn["command"] = self.stop_command

        GLabel_65 = tk.Label(root)
        GLabel_65["bg"] = "#ffffff"
        GLabel_65["borderwidth"] = "2px"
        ft = tkFont.Font(family="Times", size=58)
        GLabel_65["font"] = ft
        GLabel_65["fg"] = "#333333"
        GLabel_65["justify"] = "center"
        GLabel_65["text"] = data[6]
        GLabel_65.place(x=20, y=20, width=526, height=87)

        GLabel_566 = tk.Label(root)
        ft = tkFont.Font(family="Times", size=11)
        GLabel_566["font"] = ft
        GLabel_566["fg"] = "#333333"
        GLabel_566["justify"] = "center"
        GLabel_566["text"] = "PERSON ASSIGNED"
        GLabel_566.place(x=820, y=80, width=424, height=30)

        lbl_remaining_qty = tk.Label(root)
        lbl_remaining_qty["bg"] = "#ffffff"
        ft = tkFont.Font(family="Times", size=18)
        lbl_remaining_qty["font"] = ft
        lbl_remaining_qty["fg"] = "#333333"
        lbl_remaining_qty["justify"] = "center"
        self.lbl_remaining_qty = lbl_remaining_qty
        lbl_remaining_qty.place(x=450, y=540, width=526, height=97)

        # FUNCTIONS
        # ///////////////////////////////////////////////////////////////

        self.check_total_finished()
        self.get_remaining_qty_from_logs()

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_remaining_qty_from_logs(self):
        self.lbl_remaining_qty["text"] = f"Remaining MO Quantity: "

        remaining_qty = None

        try:
            with open("data/mo_logs.json", "r") as json_file:
                data = json.load(json_file)
                for entry in data["data"]:
                    if (
                        "wip_entity_name" in entry
                        and entry["wip_entity_name"] == self.wip_entity_name
                    ):
                        remaining_qty = entry["remaining_qty"]
                        break
        except FileNotFoundError:
            pass

        if remaining_qty is None:
            try:
                with open("data/main.json", "r") as json_file:
                    main_data = json.load(json_file)
                    wip_entities = main_data.get("data", [])
                    for entry in wip_entities:
                        if (
                            "wip_entity_name" in entry
                            and entry["wip_entity_name"] == self.wip_entity_name
                        ):
                            self.lbl_remaining_qty[
                                "text"] = f"Remaining MO Quantity: {entry['running_qty']}"
                            return entry["running_qty"]
            except FileNotFoundError:
                pass

            self.lbl_remaining_qty["text"] = "Remaining MO Quantity: N/A"
            return None

        self.lbl_remaining_qty["text"] = f"Remaining MO Quantity: {remaining_qty}"
        return remaining_qty

    def log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open(self.csv_file_path, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def show_start_btn(self):

        self.start_btn.place(x=1000, y=540, width=245, height=97)
        self.stop_btn.place_forget()

    def show_stop_btn(self):
        self.stop_btn.place(x=1000, y=540, width=245, height=97)
        self.start_btn.place_forget()

    def hide_start_and_stop_btn(self):
        self.start_btn.place_forget()
        self.stop_btn.place_forget()

    def start_command(self):
        pass
        #self.checking()  # comment this if there is a ticket for testing

        # self.show_stop_btn() #uncomment this to show the start button
        # self.log_event("START")

    def stop_command(self):
        # self.show_input_dialog()
        hris_password = simpledialog.askstring(
            "Password",
            "Enter Password", show='*'
        )

        if hris_password is not None and hris_password.strip() != "":
            input_password = str(hris_password)

            url = f"http://hris.teamglac.com/api/users/login?u={self.extracted_username}&p={input_password}"
            response = requests.get(url).json()
            if response['result'] == False or response['result'] == None:
                print("FAILED")
                # self.start_btn["state"] = "disabled"
                # self.stop_btn["state"] = "normal"

                self.show_stop_btn()
                showerror(
                    title="Login Failed",
                    message=f"Password is incorrect. Please try again.",
                )
                # self.show_input_dialog()

            else:
                # self.start_btn["state"] = "normal"    # Enable the START button
                print("Success")
                # self.stop_btn["state"] = "disabled"

                self.show_input_dialog()
                self.mo_data = MOData()
                self.mo_data.perform_check_and_swap()
        else:
            pass

    def read_machno(self):
        with open("data\main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_data = []
            extracted_machno = data["machno"]
        return extracted_machno

    def checking(self):
        hris_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
        response = requests.get(hris_url)

        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            result = data["result"]  # Access the 'result' key
            res = ""
            for x in result:
                if x["MACH201_MACHNO"] == self.read_machno():
                    res = 1
                    break
            if res == 1:
                showwarning(
                    "TICKET ALERT!",
                    "Attention! The machine is temporarily unavailable.",
                )
                # self.stop_btn["state"] = "disabled"
                self.hide_start_and_stop_btn()

            else:
                self.log_event("START")

                # self.start_btn["state"] = "normal"
                self.show_start_btn()

    def check_total_finished(self):
        with open("data/mo_logs.json", "r") as json_file:
            json_data = json.load(json_file)

        # Now you can access the data within the JSON structure
        data = json_data["data"]

        # Accessing the values within the data
        for entry in data:
            wip_entity_name = entry.get("wip_entity_name")
            running_qty = entry["running_qty"]
            total_finished = entry["total_finished"]
            remaining_qty = entry["remaining_qty"]

            if wip_entity_name == self.wip_entity_name:
                if self.running_qty == total_finished:
                    self.show_label_completed()
                    self.hide_start_and_stop_btn()

                    showinfo("MO COMPLETED!", "MO Alredy Completed!")
                    self.mo_data = MOData()
                    self.mo_data.perform_check_and_swap()
                    self.root.destroy()

            # print('wip_entity_name: ', wip_entity_name)

        # if self.wip_entity_name in entry:
        #     print('self.wip_entity_name: ', self.wip_entity_name)
        #     print('wip_entity_name: ', wip_entity_name)

    def show_input_dialog(self):
        dateTimeNow = self.currentDateTime
        person_assigned = self.extracted_fullname

        total_finished = simpledialog.askstring(
            "Enter Total Number of finished",
            "Please enter the total number of finished items",
        )

        if os.stat("data/mo_logs.json").st_size == 0:
            if total_finished is not None and total_finished.strip() != "":
                total_finished = int(total_finished)
                extracted_running_qty = int(self.running_qty)

                if total_finished <= extracted_running_qty:
                    if total_finished == extracted_running_qty:
                        status = "COMPLETED"
                        self.hide_start_and_stop_btn()
                        self.show_label_completed()
                    else:
                        status = "NOT COMPLETED"
                        self.show_start_btn()

                    self.data_dict[self.wip_entity_name] = {
                        "wip_entity_name": self.wip_entity_name,
                        "running_qty": self.running_qty,
                        "total_finished": total_finished,
                        "remaining_qty": extracted_running_qty - total_finished,
                        "transaction_date": dateTimeNow,
                        "last_person_assigned": person_assigned,
                        "status": status,  # Set the status here
                    }

                    with open("data/mo_logs.json", "w") as json_output_file:
                        json.dump(
                            {"data": list(self.data_dict.values())},
                            json_output_file,
                            indent=4,
                        )

                    # self.show_start_btn()
                    self.get_remaining_qty_from_logs()
                    # self.toggle_refresh()
                    self.log_event("STOP")
                else:
                    messagebox.showinfo(
                        title="Warning",
                        message="Input exceeded the set running Quantity: "
                        + str(extracted_running_qty),
                    )

        else:

            if total_finished is not None and total_finished.strip() != "":
                total_finished = int(total_finished)
                extracted_running_qty = int(self.running_qty)
                if self.wip_entity_name not in self.data_dict:
                    self.data_dict[self.wip_entity_name] = {
                        "wip_entity_name": self.wip_entity_name,
                        "running_qty": self.running_qty,
                        "total_finished": 0,
                        "remaining_qty": extracted_running_qty,
                    }

                try:
                    with open("data/mo_logs.json", "r") as json_file:
                        data = json.load(json_file)
                        self.data_dict = {
                            item["wip_entity_name"]: item for item in data["data"]
                        }
                        print("data_dict: ", self.data_dict)

                except FileNotFoundError:
                    self.data_dict = {}

                if self.wip_entity_name in self.data_dict:
                    current_entry = self.data_dict[self.wip_entity_name]
                    self.current_total_finished = current_entry["total_finished"]

                    if (self.current_total_finished + total_finished <= extracted_running_qty):
                        if (self.current_total_finished + total_finished == extracted_running_qty):
                            status = "COMPLETED"
                            self.hide_start_and_stop_btn()
                            self.show_label_completed()

                        else:
                            status = "NOT COMPLETED"
                            self.show_start_btn()

                        current_entry["total_finished"] += total_finished
                        current_entry["remaining_qty"] -= total_finished
                        current_entry["transaction_date"] = dateTimeNow
                        current_entry["last_person_assigned"] = person_assigned
                        current_entry["status"] = status
                        self.log_event("STOP")

                    else:
                        messagebox.showinfo(
                            title="Warning",
                            message="Input exceeded the set running Quantity: "
                            + str(extracted_running_qty),
                        )
                        print(
                            "Total finished is not less than or equal to extracted running qty."
                        )

                else:
                    if extracted_running_qty == total_finished:
                        status = "COMPLETED" if extracted_running_qty - \
                            total_finished == 0 else "NOT COMPLETED"
                        self.data_dict[self.wip_entity_name] = {
                            "wip_entity_name": self.wip_entity_name,
                            "running_qty": self.running_qty,
                            "total_finished": total_finished,
                            "remaining_qty": extracted_running_qty - total_finished,
                            "transaction_date": dateTimeNow,
                            "last_person_assigned": person_assigned,
                            "status": status,  # Set the status here
                        }
                        self.hide_start_and_stop_btn()
                        self.show_label_completed()
                        # self.toggle_refresh()

                    elif extracted_running_qty < total_finished:
                        self.show_stop_btn()

                        messagebox.showinfo(
                            title="Warning",
                            message="Input exceeded the set running Quantity: "
                            + str(extracted_running_qty),
                        )
                    else:
                        self.show_start_btn()

                        status = "COMPLETED" if extracted_running_qty - \
                            total_finished == 0 else "NOT COMPLETED"
                        self.data_dict[self.wip_entity_name] = {
                            "wip_entity_name": self.wip_entity_name,
                            "running_qty": self.running_qty,
                            "total_finished": total_finished,
                            "remaining_qty": extracted_running_qty - total_finished,
                            "transaction_date": dateTimeNow,
                            "last_person_assigned": person_assigned,
                            "status": status,  # Set the status here
                        }

                with open("data/mo_logs.json", "w") as json_output_file:
                    json.dump(
                        {"data": list(self.data_dict.values())},
                        json_output_file,
                        indent=4,
                    )

            self.get_remaining_qty_from_logs()

            # self.root.destroy()

    def show_label_completed(self):
        self.lbl_mo_status = tk.Label(self.root)
        self.lbl_mo_status["bg"] = "#5fb878"
        ft = tkFont.Font(family="Times", size=23)
        self.lbl_mo_status["font"] = ft
        self.lbl_mo_status["fg"] = "#ffffff"
        self.lbl_mo_status["justify"] = "center"
        self.lbl_mo_status["text"] = "COMPLETED"
        self.lbl_mo_status.place(x=1000, y=540, width=245, height=97)

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MoDetails(root)
    root.mainloop()
