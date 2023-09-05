import json
import os


class QuantityData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.total_running_qty()
        self.total_remaining_qty()

    def get_script_directory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def total_running_qty(self):
        log_file_path = os.path.join(
            self.get_script_directory(), self.file_path, 'main.json')

        try:
            with open(log_file_path, "r") as json_file:
                data = json.load(json_file)['data']
        except FileNotFoundError:
            print("File not found:", log_file_path)
            return 0
        except json.JSONDecodeError:
            print("Invalid JSON data in file:", log_file_path)
            return 0

        total_running_qty = 0

        for item in data:
            if item is None or item is False:
                running_qty = 0
                total_running_qty += running_qty
            else:
                running_qty = int(item['running_qty'])
                total_running_qty += running_qty

        # print("Total Running Quantity:", total_running_qty)
        return total_running_qty

    def total_remaining_qty(self):
        log_file_path = os.path.join(
            self.get_script_directory(), self.file_path, 'mo_logs.json')

        try:
            with open(log_file_path, "r") as json_file:
                data = json.load(json_file)['data']
        except FileNotFoundError:
            print("File not found:", log_file_path)
            return 0
        except json.JSONDecodeError:
            print("Invalid JSON data in file:", log_file_path)
            return 0
        total_remaining_qty = 0

        for item in data:
            if item is None or item is False:
                total_finished = 0
                total_remaining_qty += total_finished
            else:
                total_finished = int(item['total_finished'])
                total_remaining_qty += total_finished

        # print("Total Remaining Quantity:", total_remaining_qty)
        return total_remaining_qty


if __name__ == "__main__":
    LogsData()
