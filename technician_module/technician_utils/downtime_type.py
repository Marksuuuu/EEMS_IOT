import json

import requests


class DownTimeType:
    def __init__(self):
        self.downtime_type = []
        self.machno_string = ""
        self.machno_string_status = ""
        self.ticket = ""
        self.ticket_status = ""
        self.checking()

    def read_machno(self):
        with open("data\main.json", "r") as json_file:
            data = json.load(json_file)
            extracted_machno = data["machno"]
        return extracted_machno

    def checking(self):
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
                self.getDownTimeType('1')
                self.machno_string = ", ".join(machno_alerts)
                self.machno_string_status = ", ".join(machno_status)
                self.ticket = self.machno_string
                self.ticket_status = self.machno_string_status

        # time.sleep(15)

    def getDownTimeType(self, downtimeType):
        cmms_url = 'http://cmms.teamglac.com/main_downtime_type.php'
        response = requests.get(cmms_url)
        data = response.json()
        result = data["result"]
        if response.status_code == 200:
            for item in result:
                if downtimeType in item['ID']:
                    downtime_type = item["DOWNTIME_TYPE"]
                    break
                else:
                    pass


if __name__ == "__main__":
    DownTimeType()
