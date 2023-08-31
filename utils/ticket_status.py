import requests
import json

class TicketChecker:
    def __init__(self):
        self.checking()

    def read_machno(self):
        with open("data/main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_machno = data["machno"]
        return extracted_machno

    def checking(self):
        hris_url = "http://lams.teamglac.com/lams/api/job_order/active_jo.php"
        response = requests.get(hris_url)

        if response.status_code == 200:
            data = response.json() 
            result = data["result"]  
            for x in result:
                if x["MACH201_MACHNO"] == self.read_machno():
                    return True
        return False

if __name__ == "__main__":
    TicketChecker()
