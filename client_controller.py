import json
import socket
import threading

HEADER = 1024
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())


class ClientController:
    def __init__(self) -> None:
        thread = threading.Thread(target=self.config_socket, args=[])
        thread.start()

    def config_socket(self):
        addr = (SERVER, PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(addr)

    def send_json_thread(self, dict):
        thread = threading.Thread(target=self.send_json, args=[dict])
        thread.start()

    def send_json(self, dict):
        data = json.dumps(dict)
        self.client.sendall(bytes(data, encoding=FORMAT))
    
    def send_very_fast_cart(self):
        self.send_json_thread({'type': 'fast_cars'})
