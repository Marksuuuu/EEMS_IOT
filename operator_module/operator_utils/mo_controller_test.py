import tkinter as tk
import os
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import ttk
import requests
from io import BytesIO
import tkinter.font as tkFont
import csv
import json
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showwarning, showerror
import datetime
from threading import Timer

from .mo_transaction import MOData


class MoDetailsTest:
    def __init__(
            self,
            root,
            extracted_fullname,
            extracted_employee_no,
            extracted_photo_url,
            extracted_username,
            data,
            update_table_function,
            assets_dir
            ):
        
        self.root = root
        self.extracted_employee_no = extracted_employee_no
        self.extracted_photo_url = extracted_photo_url
        self.extracted_username = extracted_username
        self.extracted_fullname = extracted_fullname
        self.assets_dir = assets_dir
        self.root.title("MO DETAILS")
        self.root.geometry("933x563")
        self.root.configure(bg="#FFFFFF")
        self.center_window()
        # self.root.overrideredirect(True)

      

        self.customer = data[1]
        self.device = data[2]
        self.main_opt = data[3]
        self.package = data[4]
        self.running_qty = data[5]
        self.formatted_running_qty = "{:,}".format(self.running_qty)

        self.wip_entity_name = data[6]
        self.data_dict = {}

        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")
        self.currentDateTime = f"{date} {time}"

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

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_folder = os.path.join(script_directory, "../../data")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.csv_file_path = os.path.join(self.log_folder, "time.csv")

        self.image = ImageTk.PhotoImage(pil_image)        


        # FUNCTIONS
        # ///////////////////////////////////////////////////////////////..       
        self.initialize_gui()
        self.idle_function()
        self.idle_started = self.load_idle_state()
        self.update_table_function = update_table_function
        self.check_total_finished()
        self.get_last_person_assigned()
        self.get_remaining_qty_from_logs()


        root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.resizable(False, False)
        self.root.mainloop()


    def initialize_gui(self):
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=563,
            width=933,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)


        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            243.0,
            68.0,
            image=self.image_image_1
        )

        # OPERATOR IMAGE
        # ///////////////////////////////////////////////////////////////
        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            556.0,
            68.0,
            image=self.image
        )

        # MO NUMBER
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            104.0,
            37.0,
            anchor="nw",
            text=self.wip_entity_name,
            fill="#FFFFFF",
            font=("ArialMT", 48 * -1)
        )


        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            465.0,
            265.0,
            image=self.image_image_3
        )

        # OPERATOR FULL NAME
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            597.0,
            57.0,
            anchor="nw",
            text=self.extracted_fullname,
            fill="#343A40",
            font=("Roboto Bold", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.stop_btn = Button(
            self.root,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.stop_command,
            relief="flat"
        )
        self.stop_btn.place(
            x=712.0,
            y=467.0,
            width=172.0,
            height=58.0
        )

        self.canvas.create_text(
            66.0,
            147.0,
            anchor="nw",
            text="Main Operation",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        # MAIN OPT
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            64.0,
            173.0,
            anchor="nw",
            text=self.main_opt,
            fill="#868E96",
            font=("ArialMT", 24 * -1)
        )
        # DEVICE
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            68.0,
            267.0,
            anchor="nw",
            text="Device",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            66.0,
            295.0,
            anchor="nw",
            text= self.device,
            fill="#868E96",
            font=("ArialMT", 24 * -1)
        )

        # PACKAGE
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            526.0,
            143.0,
            anchor="nw",
            text="Package",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            526.0,
            170.0,
            anchor="nw",
            text=self.package,
            fill="#868E96",
            font=("ArialMT", 24 * -1)
        )


        # CUSTOMER
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            528.0,
            268.06951904296875,
            anchor="nw",
            text="Customer",
            fill="#343A40",
            font=("Arial BoldMT", 24 * -1)
        )

        self.canvas.create_text(
            528.0,
            296.0,
            anchor="nw",
            text=self.customer,
            fill="#868E96",
            font=("ArialMT", 24 * -1)
        )

        # LAST PERSON ASSIGNED
        # ///////////////////////////////////////////////////////////////

       

        self.image_image_4 = PhotoImage(
            file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(
            163.0,
            474.0,
            image=self.image_image_4
        )


        # MO QUANTITY
        self.canvas.create_text(
            129.0,
            434.0,
            anchor="nw",
            text="MO Qty.",
            fill="#FFFFFF",
            font=("ArialMT", 20 * -1)
        )

        self.canvas.create_text(
            64.0,
            457.0,
            anchor="nw",
            text=self.formatted_running_qty,
            fill="#FFFFFF",
            font=("Arial BoldMT", 48 * -1)
        )

        

        self.image_image_5 = PhotoImage(
            file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(
            479.0,
            474.0,
            image=self.image_image_5
        )


        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        
        self.start_btn = Button(
            self.root,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_command,
            relief="flat"
        )
        self.start_btn.place(
            x=712.0,
            y=467.0,
            width=172.0,
            height=58.0
        )


        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.root,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_close,
            relief="flat"
        )
        self.button_3.place(
            x=884.0,
            y=0.0,
            width=49.0,
            height=37.0
        )


        # REMAINING MO QUANTITY
        # ///////////////////////////////////////////////////////////////
        self.canvas.create_text(
            400.0,
            439.0,
            anchor="nw",
            text="Remaining MO Qty.",
            fill="#FFFFFF",
            font=("ArialMT", 19 * -1)
        )


        lbl_remaining_qty = tk.Label(self.root)
        lbl_remaining_qty["bg"] = "#FF6B6B"  
        ft = tkFont.Font(family="ArialMT", size=35)
        lbl_remaining_qty["font"] = ft
        lbl_remaining_qty["fg"] = "white"  # Set font color to white
        lbl_remaining_qty["justify"] = "center"
        lbl_remaining_qty.place(x=383.0, y=458.0, width=200, height=55)
        self.lbl_remaining_qty = lbl_remaining_qty


        self.last_person_ass = self.canvas.create_text(
            435.0,
            388.0,
            anchor="nw",
            fill="#D45151",
            font=("Arial BoldMT", 15 * -1, "italic")
        )




    def relative_to_assets(self, filename):
        # No need to go up one directory since we changed the working directory
        full_path = os.path.join(self.assets_dir, "frame_mo_details", filename)
        return full_path

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2      

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def update_table_display(self):
        # Call the update_table function when needed
        self.update_table_function()

    # def get_last_person_assigned(self):
    #     try:
    #         with open("data/mo_logs.json", "r") as json_file:
    #             data = json.load(json_file)
    #             for entry in data["data"]:
    #                 if "wip_entity_name" in entry and entry["wip_entity_name"] == self.wip_entity_name:
    #                     last_person_assigned = entry["last_person_assigned"]
    #                     print('last_person_assigned: ', last_person_assigned)
    #                     self.canvas.itemconfig(self.last_person_ass, text=f"LAST PERSON ASSIGNED: {last_person_assigned}")
    #     except FileNotFoundError:
    #         pass
    #     # If no matching entry is found, return None
    #     return None

    def get_last_person_assigned(self):
        try:
            with open("data/mo_logs.json", "r") as json_file:
                # Read the contents of the file and check if it's empty
                file_contents = json_file.read()
                if not file_contents:
                    return  # File is empty, no need to proceed

                json_data = json.loads(file_contents)

            data = json_data["data"]

            for entry in data:
                if "wip_entity_name" in entry and entry["wip_entity_name"] == self.wip_entity_name:
                    last_person_assigned = entry["last_person_assigned"]
                    print('last_person_assigned: ', last_person_assigned)
                    self.canvas.itemconfig(self.last_person_ass, text=f"LAST PERSON ASSIGNED: {last_person_assigned}")
                    break  # Exit the loop once the matching entry is found

        except FileNotFoundError:
            pass  # Handle the case where the file is not found

        # If no matching entry is found, return None
        return None    



    
    def get_remaining_qty_from_logs(self):
        self.lbl_remaining_qty["text"] = f" "

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
                        if ("wip_entity_name" in entry and entry["wip_entity_name"] == self.wip_entity_name):
                            self.lbl_remaining_qty["text"] = f"{entry['running_qty']}"
                            
                            return entry["running_qty"]
            except FileNotFoundError:
                pass

            self.lbl_remaining_qty["text"] = " "
            return None
        formatted_remaining_qty = "{:,}".format(remaining_qty)
        self.lbl_remaining_qty["text"] = formatted_remaining_qty
        # self.lbl_remaining_qty["text"] = f"{remaining_qty}"
        return remaining_qty



    def log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open(self.csv_file_path, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def show_start_btn(self):

        self.start_btn.place(x=712.0, y=467.0, width=172.0, height=58.0)
        self.stop_btn.place_forget()

    def show_stop_btn(self):
        self.stop_btn.place(x=712.0, y=467.0, width=172.0, height=58.0)
        self.start_btn.place_forget()

    def hide_start_and_stop_btn(self):
        self.start_btn.place_forget()
        self.stop_btn.place_forget()

    def start_command(self):

        self.log_event("START")
        self.checking() #comment this if there is a ticket for testing

        self.show_stop_btn()  

    def stop_command(self):

        # TESTING PURPOSES ONLY
        # ///////////////////////////////////////////////////////////////
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
                # self.stop_btn["state"] = "disabled"
                self.root.iconify()
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
                self.hide_start_and_stop_btn()

                showwarning(
                    "TICKET ALERT!",
                    "Attention! The machine is temporarily unavailable.",
                )
                self.root.destroy()
                # self.stop_btn["state"] = "disabled"

            else:
                print("ELSE")
                self.log_event("START")
                # self.start_btn["state"] = "normal"
                self.show_stop_btn()  

                # self.show_start_btn()

    # def check_total_finished(self):
    #     with open("data/mo_logs.json", "r") as json_file:
    #         json_data = json.load(json_file)

    #     # Now you can access the data within the JSON structure
    #     data = json_data["data"]

    #     # Accessing the values within the data
    #     for entry in data:
    #         wip_entity_name = entry.get("wip_entity_name")
    #         # running_qty = entry["running_qty"]
    #         total_finished = entry["total_finished"]
    #         # remaining_qty = entry["remaining_qty"]
            
    #         test = entry.get("last_person_assigned")
    #         if wip_entity_name == self.wip_entity_name:
    #             if self.running_qty == total_finished:

    #                 self.show_label_completed()
    #                 self.hide_start_and_stop_btn()

    #                 showinfo("MO COMPLETED!", "MO Already Completed!")


    #                 # self.mo_data = MOData()
    #                 # self.mo_data.perform_check_and_swap()

    #                 self.root.destroy()
    #         else:
    #             pass
                
    def check_total_finished(self):
        try:
            with open("data/mo_logs.json", "r") as json_file:
                # Read the contents of the file and check if it's empty
                file_contents = json_file.read()
                if not file_contents:
                    return  # File is empty, no need to proceed

                # Parse the JSON data
                json_data = json.loads(file_contents)

            # Now you can access the data within the JSON structure
            data = json_data["data"]

            # Accessing the values within the data
            for entry in data:
                wip_entity_name = entry.get("wip_entity_name")
                total_finished = entry["total_finished"]

                if wip_entity_name == self.wip_entity_name:
                    if self.running_qty == total_finished:
                        self.show_label_completed()
                        self.hide_start_and_stop_btn()
                        showinfo("MO COMPLETED!", "MO Already Completed!")
                        return  # No need to continue processing
        except FileNotFoundError:
            pass

    # If the file was empty or not found, you can handle it here


    def show_input_dialog(self):

        total_finished = simpledialog.askstring(
            "Enter Total Number of finished",
            "Please enter the total number of finished items",
        )

        dateTimeNow = self.currentDateTime
        person_assigned = self.extracted_fullname


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
                    self.mo_data = MOData()
                    self.mo_data.perform_check_and_swap()
                    self.get_remaining_qty_from_logs()
                    self.update_table_display()
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
            self.mo_data = MOData()
            self.mo_data.perform_check_and_swap()
            self.get_remaining_qty_from_logs()
            self.update_table_display()
            self.get_last_person_assigned()

            self.log_event("STOP")

            # self.root.destroy()

    def show_label_completed(self):
        self.lbl_mo_status = tk.Label(self.root)
        self.lbl_mo_status["bg"] = "#5fb878"
        ft = tkFont.Font(family="ArialMT", size=23)
        self.lbl_mo_status["font"] = ft
        self.lbl_mo_status["fg"] = "#ffffff"
        self.lbl_mo_status["justify"] = "center"
        self.lbl_mo_status["text"] = "COMPLETED"
        self.lbl_mo_status.place(x=712.0, y=467.0, width=200.0, height=58.0)

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def are_buttons_shown(self):
        try:
            return self.start_btn is not None and self.start_btn.winfo_ismapped()
        except tk.TclError as e:
            return False

    def idle_function(self):
        Timer(10, self.tick).start()
        self.root.after(10000, self.idle_function)

    def tick(self):
        if self.are_buttons_shown():
            if self.start_btn["state"] == "normal":
                if self.idle_started:
                    self.idle_started = False
                    self.log_event_idle("IDLE_START")
                    print('idle')
        else:
            if not self.idle_started:
                self.idle_started = True
                self.log_event_idle("IDLE_STOP")
                print('not idle')
            
    
    def log_event_idle(self, msg):
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
    app = MoDetailsTest(root)
