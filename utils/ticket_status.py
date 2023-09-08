import json
import requests

class TicketChecker:
    def __init__(self):
        self.checking()

    def read_machno(self):
        try:
            with open("data/main.json", "r") as json_file:
                data = json.load(json_file)
                extracted_machno = data.get("machno")  # Use .get() to handle missing key gracefully
                return extracted_machno
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None  # Return None if there's an issue reading the JSON or no "machno" found

    def checking(self):
        hris_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
        response = requests.get(hris_url)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result", [])  # Use .get() to handle missing key gracefully
            for x in result:
                machno = self.read_machno()
                if machno is not None and x.get("MACH201_MACHNO") == machno:
                    return True
        return False

if __name__ == "__main__":
    TicketChecker()
