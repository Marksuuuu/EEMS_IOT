# socketio_manager.py

import socketio
import os
import uuid
import re
import json
import csv

class SocketIOManager:
    def __init__(self):
        self.sio = socketio.Client(reconnection=True, reconnection_attempts=5,
                                   reconnection_delay=1, reconnection_delay_max=5)
        self.client = str(uuid.uuid4())
        self.filename = os.path.basename(__file__)
        self.removeExtension = re.sub('.py', '', self.filename)

    def connect(self):
        @self.sio.event
        def on_connect():
            print('Connected to server')
            self.sio.emit('client_connected', {'machine_name': self.filename, 'client': self.client})
            self.sio.emit('controller', {'machine_name': self.filename})
            self.sio.emit('client', {'machine_name': self.filename, 'client': self.client})

        @self.sio.event
        def on_disconnect():
            print('Disconnected from server')
            
        @self.sio.event
        def my_message(data):
            print('Message received with', data)
            toPassData = data['dataToPass']
            machno = data['machno']
            remove_py = re.sub('.py', '', filename)
            fileNameWithIni = 'main.json'
            folder_path = 'data'
            file_path = f'{folder_path}/{fileNameWithIni}'

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(file_path, 'w') as file:
                data = {
                    'machno': machno,
                    'filename': remove_py,
                    'data': toPassData
                }
                json.dump(data, file)
            sio.emit('my_response', {'response': 'my response'})

        self.sio.connect('http://10.0.2.150:8083')

def main():
    manager = SocketIOManager()
    manager.connect()

if __name__ == "__main__":
    main()
