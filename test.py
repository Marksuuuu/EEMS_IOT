import csv
import json
import datetime

class YourClassName:
    def __init__(self):
        # Initialize self.idle_started here or in your constructor
        self.idle_started = self.load_idle_state()
    
    def check_last_data(self):
        with open('data/time.csv', 'r') as file:
            csv_reader = csv.reader(file)
            data = list(csv_reader)
            return data[-1][0]
        
    def trigger_idle_in_main(self):
        # You need to define self.checking_data_in_time_csv
        if self.checking_data_in_time_csv == 'STOP':
            print('go here')
            if not self.idle_started:
                print('go here, if')  # Fixed typo here
                self.idle_started = True
                self.log_event("IDLE_START")
                print(self.checking_data_in_time_csv)
        else:
            if self.idle_started:
                print('go here, else')  # Fixed typo here
                self.idle_started = False
                self.log_event("IDLE_STOP")
        self.root.after(10000, self.trigger_idle_in_main)
        
    # Rest of your methods

    def save_idle_state(self):
        with open('config/idle_state.json', 'w') as state_file:
            json.dump({'idle_started': self.idle_started}, state_file)
