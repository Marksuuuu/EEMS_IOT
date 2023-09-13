import csv
import json
import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class TimeData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.get_available_hrs()
        self.calculate_oee()
        self.calculate_total_downtime()
        self.calculate_total_idle()

    def get_script_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    def calculate_oee(self):
        try:
            productiveHrs = self.calculate_total_productive_time().total_seconds() / 3600
            
            # Convert timedelta objects to strings and then split them
            availableHrs_str = str(self.get_available_hrs())
            availableHrs_parts = availableHrs_str.split(':')
            
            if len(availableHrs_parts) != 3:
                raise ValueError("Invalid format for available hours")
            
            available_hours = int(availableHrs_parts[0])
            available_minutes = int(availableHrs_parts[1])
            available_seconds = int(availableHrs_parts[2])

            availableHrs = available_hours + (available_minutes / 60) + (available_seconds / 3600)
            
            # Convert timedelta objects to strings and then split them
            downtimeHrs_str = str(self.calculate_total_downtime())
            downtimeHrs_parts = downtimeHrs_str.split(':')
            
            if len(downtimeHrs_parts) != 3:
                raise ValueError("Invalid format for downtime hours")
            
            downtime_hours = int(downtimeHrs_parts[0])
            downtime_minutes = int(downtimeHrs_parts[1])
            downtime_seconds = int(downtimeHrs_parts[2])

            downtimeHrs = downtime_hours + (downtime_minutes / 60) + (downtime_seconds / 3600)

            if availableHrs > 0:
                oee_percentage = (productiveHrs / (availableHrs - downtimeHrs)) * 100
                return round(oee_percentage, 5)
            else:
                return 0
        except Exception as e:
            print(f"Error calculating OEE: {e}")
            return 0

    # def get_available_hrs(self):
    #     script_directory = os.path.dirname(os.path.abspath(__file__))
    #     log_folder = os.path.join(script_directory, self.file_path)
    #     log_file_path = os.path.join(log_folder, 'logs/logs.csv')
    #     data = []
    #     total_available_seconds = 0
        
    #     with open(log_file_path, 'r') as csvfile:
    #         csvreader = csv.reader(csvfile)
    #         for row in csvreader:
    #             data.append(row)
    #     previous_event_time = None
    #     for event in data:
    #         event_type = event[0]
    #         event_date = event[1]
    #         event_time = event[2]
    #         event_datetime = datetime.strptime(
    #             event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")
    #         if previous_event_time and event_type == "OFFLINE":
    #             time_difference = event_datetime - previous_event_time
    #             total_available_seconds += time_difference.total_seconds()
    #         previous_event_time = event_datetime
    #     if not any(event[0].startswith("OFFLINE") for event in data):
    #         current_datetime = datetime.now()
    #         if previous_event_time:
    #             time_difference = current_datetime - previous_event_time
    #         else:
    #             time_difference = current_datetime - \
    #                 datetime.strptime("2000-01-01 00:00:00",
    #                                   "%Y-%m-%d %H:%M:%S")
    #         total_available_seconds += time_difference.total_seconds()
    #     formatted_time = self.format_time(total_available_seconds)
    #     return formatted_time

    def get_available_hrs(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, self.file_path)
        log_file_path = os.path.join(log_folder, 'logs/logs.csv')
        data = []
        total_available_seconds = 0

        with open(log_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        
        if not data:
            # If there is no data in the CSV, return 0 as formatted time
            return "00:00:00"

        previous_event_time = None
        for event in data:
            event_type = event[0]
            event_date = event[1]
            event_time = event[2]
            event_datetime = datetime.strptime(
                event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")
            if previous_event_time and event_type == "OFFLINE":
                time_difference = event_datetime - previous_event_time
                total_available_seconds += time_difference.total_seconds()
            previous_event_time = event_datetime
        if not any(event[0].startswith("OFFLINE") for event in data):
            current_datetime = datetime.now()
            if previous_event_time:
                time_difference = current_datetime - previous_event_time
            else:
                time_difference = current_datetime - \
                    datetime.strptime("2000-01-01 00:00:00",
                                    "%Y-%m-%d %H:%M:%S")
            total_available_seconds += time_difference.total_seconds()
        formatted_time = self.format_time(total_available_seconds)
        return formatted_time

    def calculate_total_productive_time(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, self.file_path)
        log_file_path = os.path.join(log_folder, 'time.csv')

        data = []
        with open(log_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(tuple(row))

        downtime_hours = {}
        start_time = None

        for action, date_str, time_str in data:
            dt = datetime.strptime(
                date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")

            if action == "START":
                start_time = dt
            elif action == "STOP" and start_time is not None:
                productive_time = dt - start_time
                day = dt.date()
                if day not in downtime_hours:
                    downtime_hours[day] = productive_time
                else:
                    downtime_hours[day] += productive_time
                start_time = None

        total_productive_time = timedelta()

        for day, productive_time in downtime_hours.items():
            total_productive_time += productive_time

        return total_productive_time

    def calculate_total_downtime(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, self.file_path)
        log_file_path = os.path.join(log_folder, 'logs/downtime.csv')

        data = []
        with open(log_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        total_idle_time = 0
        previous_event_time = None
        downtime_started = False

        for event in data:
            event_type = event[0]
            event_date = event[1]
            event_time = event[2]

            event_datetime = datetime.strptime(
                event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")

            if event_type == "DOWNTIME_START":
                downtime_started = True
                previous_event_time = event_datetime
            elif event_type == "DOWNTIME_STOP":
                if downtime_started:
                    time_difference = event_datetime - previous_event_time
                    total_idle_time += time_difference.total_seconds()
                    downtime_started = False
            elif downtime_started:
                time_difference = event_datetime - previous_event_time
                total_idle_time += time_difference.total_seconds()

        if downtime_started:
            current_datetime = datetime.now()
            time_difference = current_datetime - previous_event_time
            total_idle_time += time_difference.total_seconds()

        formatted_time = self.format_time(total_idle_time)
        return formatted_time
    
    
    def calculate_total_idle(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        log_folder = os.path.join(script_directory, self.file_path)
        log_file_path = os.path.join(log_folder, 'logs/idle.csv')

        data = []
        with open(log_file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        total_idle_time = 0
        previous_event_time = None
        idle_started = False

        for event in data:
            event_type = event[0]
            event_date = event[1]
            event_time = event[2]

            event_datetime = datetime.strptime(
                event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")

            if event_type == "IDLE_START":
                idle_started = True
                previous_event_time = event_datetime
            elif event_type == "IDLE_STOP":
                if idle_started:
                    time_difference = event_datetime - previous_event_time
                    total_idle_time += time_difference.total_seconds()
                    idle_started = False
            elif idle_started:
                time_difference = event_datetime - previous_event_time
                total_idle_time += time_difference.total_seconds()

        if idle_started:
            current_datetime = datetime.now()
            time_difference = current_datetime - previous_event_time
            total_idle_time += time_difference.total_seconds()

        formatted_time = self.format_time(total_idle_time)
        # print(f"==>> formatted_time: {formatted_time}")
        return formatted_time

if __name__ == "__main__":
    TimeData()