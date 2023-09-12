import os
import json


class MOData:
    def __init__(self):
        self.perform_check_and_swap()

    def read_mo_logs(self):
        with open('data/mo_logs.json', 'r') as json_file:
            mo_logs = json.load(json_file)
        return mo_logs

    def read_main_json(self):
        with open('data/main.json', 'r') as json_file:
            main_json = json.load(json_file)
        return main_json

    def edit_and_write_main_json(self, main_json):
        with open('data/main.json', 'w') as json_file:
            json.dump(main_json, json_file, indent=4)


    def perform_check_and_swap(self):
        mo_logs = self.read_mo_logs()
        main_json = self.read_main_json()
 
        main_array = main_json['data']
        mo_logs_array = mo_logs['data']

        first_wip_entity_name = main_array[0]['wip_entity_name']
        first_running_qty = main_array[0]['running_qty']

        print('first_wip_entity_name: ', first_wip_entity_name)
        print('first_running_qty: ', first_running_qty)
        for entry in mo_logs_array:
            if first_wip_entity_name in entry.get('wip_entity_name'):
                if int(first_running_qty) == entry.get('total_finished'):
                    first_element = main_array.pop(0)  # Remove the first element
                    main_array.append(first_element)    
                    self.edit_and_write_main_json(main_json)
                    print('COMPLETED')
                    break
                else:
                    print('NOT COMPLETED')

if __name__ == '__main__':
    MOData()