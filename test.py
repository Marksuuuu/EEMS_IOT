
sio = socketio.Client(
    reconnection=True,
    reconnection_attempts=5,
    reconnection_delay=1,
    reconnection_delay_max=5,
)
client = str(uuid.uuid4())
filename = os.path.basename(__file__)
removeExtension = re.sub(".py", "", filename)
@sio.event
def connect():
    print("Connected to server")
    sio.emit("client_connected", {"machine_name": filename, "client": client})
    sio.emit("controller", {"machine_name": filename})
    sio.emit("client", {"machine_name": filename, "client": client})
@sio.event
def disconnect():
    print("disconnected to server")
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
        self.root.configure(bg="#FBFBFB")
        current_year = datetime.datetime.now().year
        self.root.title(f"EEMS_IOT - © {current_year}")

    def on_closing(self):
        try:
            self.idle_log_event("IDLE_STOP")
            self.save_idle_state(False)

            # self.led.turn_off_all()
            self.root.destroy()  
        except tk.TclError:
            # Handle the exception when the window is closed
            # self.led.turn_off_all()
            self.idle_log_event("IDLE_STOP")
            self.root.destroy()  
            print("Window closed Unexpectedly")


    def makeCenter(self):
        self.width = 1024
        self.height = 600
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            self.width,
            self.height,
            (self.screenwidth - self.width) / 2,
            (self.screenheight - self.height) / 2,
        )
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

    def create_gui_elements(self):
        self.canvas = Canvas(
            self.root,
            bg="#FBFBFB",
            height=600,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0, 0.0, 1024.0, 100.0, fill="#FFFFFF", outline=""
        )

        self.canvas.create_rectangle(
            31.0, 10.0, 282.0, 86.97332763671875, fill="#D3F9D8", outline=""
        )

        self.image_1 = self.canvas.create_image(516.0, 49.0, image=self.tk_image_1)

        # self.image_2 = self.canvas.create_image(864.0,66.0, image=self.tk_image_2)

        entry_bg_1 = self.canvas.create_image(533.5, 50.0, image=self.tk_entry_1)
        self.employee_id = Entry(
            self.root,
            bd=0,
            bg="#EFEFEF",
            
            fg="#000716",
            highlightthickness=0,
            font=("arial", 30),
            justify="center",  # Set text alignment to center
        )
        self.employee_id.focus_set()


        self.employee_id.place(x=378.0, y=28.0, width=311.0, height=42.0)

        self.employee_id.bind("<KeyPress>", self.validate_employee_number)

        # image_3 = self.canvas.create_image(815.0, 66.0,image=self.tk_image_3)

        self.clock = self.canvas.create_text(
            825.0, 60.0, anchor="nw", fill="#343A40", font=("Roboto Regular", 9 * -1)
        )

        image_4 = self.canvas.create_image(64.0, 47.0, image=self.tk_image_4)

        image_5 = self.canvas.create_image(64.0, 47.0, image=self.tk_image_5)

        image_6 = self.canvas.create_image(512.0, 259.0, image=self.tk_image_6)

        self.canvas.create_text(
            97.0,
            27.0,
            anchor="nw",
            text="MACHINE",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1),
        )

        self.canvas.create_text(
            97.0,
            44.0,
            anchor="nw",
            text="ONLINE",
            fill="#343A40",
            font=("Roboto Medium", 24 * -1),
        )

        image_7 = self.canvas.create_image(167.0, 259.0, image=self.tk_image_7)

        self.image_8 = self.canvas.create_image(166.0, 260.0, image=self.oee_img)

        image_9 = self.canvas.create_image(340.0, 509.0, image=self.tk_image_9)

        self.machine_data_lbl = self.canvas.create_text(
            24.0, 442.0, anchor="nw", fill="#343A40", font=("Roboto Medium", 20 * -1)
        )

        image_10 = self.canvas.create_image(855.0, 509.0, image=self.tk_image_10)

        image_11 = self.canvas.create_image(856.0, 259.0, image=self.tk_image_11)

        self.canvas.create_text(
            700.0,
            435.0,
            anchor="nw",
            # text="LOGS",
            fill="#343A40",
            width=100,
            font=("Roboto Medium", 14 * -1),
        )

        self.canvas.create_text(
            689.0,
            112.0,
            anchor="nw",
            text="Total Quantity",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1),
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
            font=("Roboto Medium", 14 * -1),
        )

        image_12 = self.canvas.create_image(362.0, 49.0, image=self.tk_image_12)

        self.button_1 = Button(
            image=self.tk_btn_1, borderwidth=0, highlightthickness=0, relief="flat"
        )


        self.button_3= Button(image=self.tk_btn_3,borderwidth=0, highlightthickness=0, relief="flat", command=self.refresh_clicked)
        self.button_3.place(
            x=800.0,
            y=63.0,
            width=128.54547119140625,
            height=28.0
        )
        self.image_13 = self.canvas.create_image(857.0, 259.0, image=self.total_img)

        image_14 = self.canvas.create_image(512.0, 264.0, image=self.line_graph_img)

        self.set_logs = self.canvas.create_text(
            709.0, 435.0,                   
            anchor="nw",                   
            fill="#343A40",                
            font=("Roboto Medium", 10 * -1),  
            width=300                    
        )
        
        self.lbl_graphs = self.canvas.create_text(
            688.0,
            97.0,
            anchor="nw",
            # text="GRAPHS LAST UPDATED AS OF:  28-08-23  | 11:25 :00  ",
            fill="#FF0000",
            font=("RobotoItalic Regular", 13 * -1, "italic")
        )

    def update_graphs_label(self):
        current_time = time.strftime("%I:%M %p")  # Format time in 12-hour with AM/PM
        current_date = time.strftime("%b/%d/%Y")

        dateNTime = current_date + " " + current_time
        self.canvas.itemconfig(self.lbl_graphs, text=f"LAST UPDATED AS OF: {dateNTime}")

    def refresh_clicked(self):
        self.update_chart()
        # self.update_graphs_label()


    def get_script_directory(self):
        return os.path.dirname(os.path.abspath(__file__))

    # def update_clock(self):
    #     current_time = time.strftime("%I:%M %p")  # Format time in 12-hour with AM/PM
    #     current_date = time.strftime("%b/%d/%Y")

    #     dateNTime = current_date + " " + current_time
    #     self.canvas.itemconfig(self.clock, text=dateNTime)
    #     self.root.after(60000, self.update_clock)

    def create_total_qty_graph(self):
        self.quantity_data = QuantityData("../data")
        if (
            self.quantity_data.total_running_qty() == 0
            and self.quantity_data.total_remaining_qty() == 0
        ):
            return None

        result_qty = (
            self.quantity_data.total_running_qty()
            - self.quantity_data.total_remaining_qty()
        )
        data = [self.quantity_data.total_remaining_qty(), result_qty]
        labels = ["", ""]
        colors = ["#4CAF50", "#e74c3c"]
        explode = (0.05, 0)

        figure = Figure(figsize=(3, 2.5), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        autotexts = plot.pie(
            data,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.85,
            explode=explode,
        )

        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        plot.add_artist(centre_circle)

        plot.set_facecolor("none")
        plot.axis("equal")

        autopct_values = [f"{p}" for p in autotexts]
        legend_labels = ["QUANTITY COMPLETED", "PROCESS QUANTITY"]

        # Move the legend outside the plot
        plot.legend(
            legend_labels, loc="center right", bbox_to_anchor=(1, 0.5), fontsize=6.5
        )

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            "RGB", canvas.get_width_height(), canvas.tostring_rgb()
        )
        img = ImageTk.PhotoImage(image=pil_image)
        return img


    def update_chart(self):
        self.update_graphs_label()

        # Create a separate thread for creating the OEE graph
        threading.Thread(target=self.create_oee_graph_threaded).start()

        # Schedule the function to run again after 300000 milliseconds (5 minutes)
        self.root.after(300000, self.update_chart)

    def create_oee_graph_threaded(self):
        oee_img = self.create_oee_graph()

        # Update the GUI in the main thread with the OEE graph image
        self.root.after(0, self.update_oee_graph, oee_img)

    def update_oee_graph(self, oee_img):

        
        self.oee_img = oee_img
        self.image_8 = self.canvas.create_image(166.0, 260.0, image=self.oee_img)


    def create_oee_graph(self):
        self.get_data = TimeData("../data")
        calculated_oee = self.get_data.calculate_oee()
        calculated_oee = max(0, min(calculated_oee, 100))

        total = 100 - calculated_oee
        data = [calculated_oee, total]
        labels = ["", ""]
        colors = ["#4CAF50", "#e74c3c"]
        explode = (0.05, 0)

        figure = Figure(figsize=(3, 2.5), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        autotexts = plot.pie(
            data,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.85,
            explode=explode,
            textprops={'fontsize': 12} 
        )


        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        plot.add_artist(centre_circle)

        plot.set_facecolor("none")
        plot.axis("equal")

        

        autopct_values = [f"{p}" for p in autotexts]
        legend_labels = ["EFFECTIVENESS", "INEFFECTIVENESS"]

        # Move the legend outside the plot
        plot.legend(
            legend_labels, loc="center right", bbox_to_anchor=(1, 0.5), fontsize=6.5
        )

        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        canvas.draw()
        pil_image = Image.frombytes(
            "RGB", canvas.get_width_height(), canvas.tostring_rgb()
        )
        img = ImageTk.PhotoImage(image=pil_image)


        return img

    def create_line_chart(self):
        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        days = np.arange(1, 8)
        values = [10, 0, 2, 11, 4, 2, 15]

        ax.plot(days, values, marker="o", label="7-Day Data")
        plt.rcParams.update({"font.size": 6})
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
            self.get_script_directory(), "data/logs", "activity_log.txt"
        )
        try:
            with open(log_file_path, "r") as file:
                log_content = file.read()
            lines = log_content.split("\n")
            last_5_logs = "\n".join(lines[-6:])
            self.canvas.itemconfig(self.set_logs, text=last_5_logs)

        except FileNotFoundError:
            self.logs["text"] = "Log file not found."
            
        # self.root.after(10000, self.update_logs)
        

    def online_status_card(self):
        self.canvas.create_rectangle(
            31.0, 10.0, 282.0, 86.97332763671875, fill="#D3F9D8", outline=""
        )
        self.canvas.create_text(
            97.0, 
            27.0,
            anchor="nw",
            text="MACHINE",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1),
        )
        self.canvas.create_text(
            97.0,
            44.0,
            anchor="nw",
            text="ONLINE",
            fill="#343A40",
            font=("Roboto Medium", 24 * -1),
        )
        self.image_image_2 = self.canvas.create_image(64.0, 47.0, image=self.tk_image_5)

    def offline_status_card(self):
        self.canvas.create_rectangle(
            31.0, 10.0, 282.0, 86.97332763671875, fill="#FFCECE", outline=""
        )
        self.canvas.create_text(
            97.0,
            27.0,
            anchor="nw",
            text="MACHINE",
            fill="#343A40",
            font=("Roboto Medium", 14 * -1),
        )
        self.canvas.create_text(
            97.0,
            44.0,
            anchor="nw",
            text="OFFLINE",
            fill="#343A40",
            font=("Roboto Medium", 24 * -1),
        )
        self.image_image_1 = self.canvas.create_image(64.0, 47.0, image=self.tk_image_4)

    def update_status(self):
        statusHere = StatusUpdate("data/logs/logs.csv")
        getStatus = statusHere.get_last_log_value()
        if getStatus is None or False:
            pass
        elif getStatus == "ONLINE":
            self.online_status_card()
            self.verify_ticket_status()
            # self.downtime_started = False
        else:
            self.offline_status_card()
          
            self.delete_file_data()
        self.root.after(1000, self.update_status)

    def disable_label(self):
        self.button_1.place_forget()

    def enable_label(self):

        self.button_1.place(x=710.0, y=10.0, width=313.64697265625, height=43.0)

    def checking_ticket(self):
        pass

    def verify_ticket_status(self):
        if self.ticket_present:
            self.enable_label()
            if not self.downtime_started:
                self.downtime_started = True
        else:
            self.disable_label()
            if self.downtime_started:
                self.downtime_started = False
                self.log_event("DOWNTIME_STOP")
        self.root.after(1000, self.verify_ticket_status)
        
    def log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open("data/logs/downtime.csv", mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def load_downtime_state(self):
        try:
            with open("config/downtime_state.json", "r") as state_file:
                state = json.load(state_file)
                return state.get("downtime_started", False)
        except FileNotFoundError:
            return False

    def save_downtime_state(self):
        with open("config/downtime_state.json", "w") as state_file:
            json.dump({"downtime_started": self.downtime_started}, state_file)

    def socketio_path(self):
        path_here = os.path.join(self.get_script_directory(), "data", "main.json")
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
            hris_url = (
                f"http://hris.teamglac.com/api/users/emp-num?empno={employee_number}"
            )
            response = requests.get(hris_url)

            if response.status_code == 200:
                try:
                    data = json.loads(response.text)["result"]

                    # Check if data is a dictionary before accessing its values
                    if isinstance(data, dict):
                        user_department = data.get("employee_department")
                        fullname = data.get("fullname")
                        user_position = data.get("employee_position")
                        employee_no = data.get("employee_no")
                        employee_department = data.get("employee_department")
                        photo_url = data.get("photo_url")
                        username = data.get("username")

                        data = [
                            user_department,
                            fullname,
                            employee_no,
                            employee_department,
                            photo_url,
                            user_position,
                            username,
                        ]
                        dataJson = {"data": data}

                        if user_department and user_position:
                            self.validate_permissions(
                                user_department, user_position, dataJson
                            )
                        else:
                            pass
                    else:
                        pass
                except KeyError:
                    pass
            else:
                print("Error accessing HRIS API:", response.status_code)
        except ValueError:
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a valid integer employee number."
            )

    def validate_offline_employee(self, employee_number):
        log_file_path = os.path.join(self.get_script_directory(), "config", "hris.json")

        with open(log_file_path, "r") as json_file:
            data = json.load(json_file)["result"]

        matching_employee = None
        for employee in data:
            if employee.get("employee_id_no") == employee_number:
                matching_employee = employee
                break

        if matching_employee:
            user_department = matching_employee.get("employee_department")
            user_position = matching_employee.get("employee_position")
            self.validate_permissions(user_department, user_position)
        else:
            print("Employee not found.")

    def validate_permissions(self, user_department, user_position, dataJson):
        self.employee_number = self.employee_id.get()
        permissions = self.load_permissions()
        if permissions.is_department_allowed(
            user_department
        ) and permissions.is_position_allowed(user_position):
            if permissions.is_technician(user_position):
                self.show_tech_dashboard(user_department, user_position, dataJson)
            elif permissions.is_operator(user_position):
                print(f"{user_position} is an operator.")
                self.show_operator_dashboard(user_department, user_position, dataJson)
                data = {
                    "msg": f"User login successful. ID NUM: {self.employee_number}",
                    "emp_id": self.employee_number,
                }
                
                sio.emit("activity_log", {"data": data})
                self.log_activity(
                    logging.INFO,
                    f"User login successful. ID NUM: {self.employee_number}",
                )
                sio.emit("activity_log", {"data": data})

            else:
                self.log_activity(
                    logging.INFO,
                    f"User login successful. ID NUM: {self.employee_number}",
                )
                data = {
                    "msg": f"User's department or position is not allowed. Please check, Current Department / Position: {user_department} {user_position}",
                    "emp_id": self.employee_number,
                }
                sio.emit("activity_log", {"data": data})
                showerror(
                    title="Login Failed",
                    message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}",
                )

        else:
            self.log_activity(
                logging.INFO, f"User login unsuccessful. ID NUM: {self.employee_number}"
            )
            data = {
                "msg": f"User's department or position is not allowed. Please check, Current Department / Position: {user_department} {user_position}",
                "emp_id": self.employee_number,
            }
            sio.emit("activity_log", {"data": data})
            showerror(
                title="Login Failed",
                message=f"User's department or position is not allowed. Please check, Current Department / Possition  {user_department + ' ' + user_position}",
            )

    def load_permissions(self):
        log_file_path = os.path.join(
            self.get_script_directory(), "config", "settings.json"
        )
        permissions = UserPermissions(log_file_path)
        permissions.load_permissions()
        return permissions

    def checking_allowed_user(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, "config")
        log_file_path = os.path.join(log_folder, "settings.json")
        try:
            with open(log_file_path, "r") as file:
                log_content = file.read()
                result = log_content["allowed_users"]
        except FileNotFoundError as e:
            print(e)

    def init_logging(self):
        log_file = "data/logs/activity_log.txt"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filemode="a",
        )

    def log_activity(self, level, message):
        logging.log(level, message)
 
    def show_operator_dashboard(self, user_department, user_position, data_json):
        if not self.ope_dashboard_open:
            self.ope_dashboard_open = True

            OpeDashboard = tk.Toplevel(self.root)
            OpeDashboard.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
            assets_dir = "assets"
            ope_dashboard = OperatorDashboardTest(OpeDashboard, user_department, user_position, data_json, assets_dir, sio)
            self.root.withdraw()

    def on_dashboard_close(self):
        self.ope_dashboard_open = False
        self.root.deiconify()

    def show_tech_dashboard(self, user_department, user_position, dataJson):
        techDashboard = tk.Toplevel(self.root)   
        assets_dir = "assets"
        tech_dashboard = TechnicianDashboardTest(
            techDashboard, user_department, user_position, dataJson, assets_dir)
        self.root.withdraw()

    def mch_label(self):
        # Create a separate thread for calculating machine details
        threading.Thread(target=self.calculate_machine_details).start()

    def calculate_machine_details(self):
        productive_time = self.get_data.calculate_total_productive_time()
        total_idle_time = self.get_data.calculate_total_idle()
        total_downtime = self.get_data.calculate_total_downtime()
        available_hours = self.get_data.get_available_hrs()
        processed_qty = '{:,}'.format(self.total_remaining_qty_value)
        total_qty_to_process = '{:,}'.format(self.total_running_qty)

        machine_details = f"""\tPRODUCTIVE HRS: \t{productive_time}
              TOTAL IDLE HRS: \t\t{total_idle_time}
              DOWNTIME HRS: \t\t{total_downtime}
              AVAIL HRS: \t\t{available_hours}
              QTY PROCESSED:\t\t{processed_qty}
              TTL QTY TO PROCESS: \t{total_qty_to_process}"""

        # Update the GUI label in the main thread
        self.root.after(0, self.update_machine_details, machine_details)

    def update_machine_details(self, machine_details):
        self.canvas.itemconfig(self.machine_data_lbl, text=machine_details)
        self.root.after(60000, self.mch_label)
        
    def insert_idle_start_after_delay(self):
        # Schedule the check_idle_condition function to run after 10 seconds
        self.root.after(10000, self.insert_idle_start_after_delay)
        self.check_idle_condition()

    def check_idle_condition(self):
        # create an instance of the StatusUpdate class
        statusHere = StatusUpdate("data/logs/logs.csv")
        # get the last value in the log file
        getStatus = statusHere.get_last_log_value()
        # check that the log file is not empty
        if getStatus is None or False:
            pass
        # if the last value is ONLINE, and no ticket is present, load the idle state
        elif getStatus == "ONLINE":
            if not self.ticket_present:
                self.load_idle_state()
            else:
                self.save_idle_state(False)
    def load_idle_state(self):
        try:
            # Open the idle_state.json file for reading
            with open('config/idle_state.json', 'r') as idle_state_val:
                # Load the data from the idle_state.json file
                data = json.load(idle_state_val)
                # Get the idle_started value from the data
                idle_started = data['idle_started']
                if idle_started == False:
                    self.idle_log_event("IDLE_START")
                    self.save_idle_state(True)
                    sio.emit('light_change', {'data': 'TURN_ON_ORANGE'})
                    print('idle_started: ', idle_started)
        except FileNotFoundError:
            return False
        
    def save_idle_state(self, val):
        with open('config/idle_state.json', 'w') as state_file:
            json.dump({'idle_started': val}, state_file)     

    def idle_log_event(self, msg):
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        time = current_time.strftime("%H:%M:%S")

        with open('data/logs/idle.csv', mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([msg, date, time])

    def delete_file_data(self):
        idle = os.path.join(self.get_script_directory(), "data/logs", "idle.csv")
        downtime = os.path.join(
            self.get_script_directory(), "data/logs", "downtime.csv"
        )
        productive_hrs = os.path.join(self.get_script_directory(), "data", "time.csv")
        total_avail_hrs = os.path.join(self.get_script_directory(), "data/logs", "logs.csv")
        try:
            with open(idle, "w") as file:
                file.truncate(0)
            with open(productive_hrs, "w") as file:
                file.truncate(0)
            with open(downtime, "w") as file:
                file.truncate(0)
            with open(total_avail_hrs, "w") as file:
                file.truncate(0)
        except IOError:
            print(f"Error deleting data in '{filename}'.")

    def send_files_in_folder(self, folder_path):
        try:
            items = os.listdir(folder_path)
            for item in items:
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    with open(item_path, 'rb') as file:
                        file_data = file.read()
                        sio.emit('file_upload', {'file_data': file_data, 'file_name': item})
                elif os.path.isdir(item_path):
                    self.send_files_in_folder(item_path)
        except Exception as e:
            print(f"Error sending files in folder {folder_path}: {str(e)}")

    def send_file(self):
        if not self.sending_files:
            self.sending_files = True
            for root_folder in self.root_folders:
                self.send_files_in_folder(root_folder)
            self.sending_files = False
        self.root.after(180000, self.send_file)  # Adjust the interval as needed

   