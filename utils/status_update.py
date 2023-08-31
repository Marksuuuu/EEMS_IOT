import csv
import os


class StatusUpdate:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def get_last_log_value(self):
        try:
            with open(self.log_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                last_row = None
                for row in csv_reader:
                    last_row = row
                if last_row:
                    last_value = last_row[0]
                    return last_value
                else:
                    return "No logs available"
        except FileNotFoundError as e:
            print(e)
            return "File not found"


def get_last_log_value_from_file():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    log_folder = os.path.join(script_directory, log_file_path)
    log_file_path = os.path.join(log_folder, 'logs.csv')

    log_reader = StatusUpdate(log_file_path)
    last_value = log_reader.get_last_log_value()
    return last_value


if __name__ == "__main__":
    last_value = get_last_log_value_from_file()
    print("Last log value:", last_value)
