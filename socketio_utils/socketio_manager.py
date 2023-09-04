# socketio_manager.py

import socketio
import os
import uuid
import re
import json
import csv

class SocketIOManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocketIOManager, cls).__new__(cls)
            cls._instance.setup_socket_io()
        return cls._instance

    def setup_socket_io(self):
        self.sio = socketio.Client(reconnection=True, reconnection_attempts=5,
                                   reconnection_delay=1, reconnection_delay_max=5)
        self.client = str(uuid.uuid4())

        @self.sio.event
        def connect():
            print('Connected to server')
            self.sio.emit('client_connected', {'machine_name': self.filename, 'client': self.client})
            self.sio.emit('controller', {'machine_name': self.filename})
            self.sio.emit('client', {'machine_name': self.filename, 'client': self.client})

        @self.sio.event
        def disconnect():
            print('Disconnected from server')

        @self.sio.event
        def my_message(data):
            print('Message received with', data)
            to_pass_data = data['dataToPass']
            machno = data['machno']
            remove_py = re.sub('.py', '', self.filename)
            fileNameWithIni = remove_py + '.json'
            folder_path = 'data'
            file_path = f'{folder_path}/{fileNameWithIni}'

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(file_path, 'w') as file:
                data = {
                    'machno': machno,
                    'filename': remove_py,
                    'data': to_pass_data
                }
                json.dump(data, file)
            self.sio.emit('my_response', {'response': 'my response'})

        @self.sio.event
        def getMatrixfromServer(data):
            print('Message received with', data)
            to_pass_data = data['dataToPass'][0]

            flattened_data = ', '.join(to_pass_data).replace("'", "")
            print(f"==>> toPassData: {flattened_data}")

            filename = 'matrix.csv'
            folder_path = 'data'
            file_path = os.path.join(folder_path, filename)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_exists = os.path.exists(file_path)
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)

                if not file_exists:
                    header_row = [f'data{i}' for i in range(1, len(to_pass_data) + 1)]
                    writer.writerow(header_row)

                writer.writerow(to_pass_data)

        def connect(self, url, filename):
            self.filename = filename
            self.sio.connect(url)

        def disconnect(self):
            self.sio.disconnect()

        def emit(self, event_name, data):
            self.sio.emit(event_name, data)
