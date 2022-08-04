import json
import socket
import threading

HEADER = 64
PORT = 5052
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    encoded_msg = msg.encode(FORMAT)
    msg_length = len(encoded_msg)
    send_message_lenght = str(msg_length).encode(FORMAT)
    send_message_lenght += b' ' * (HEADER - len(send_message_lenght))
    client.send(send_message_lenght)
    client.send(encoded_msg)

def send_json(dict):
    data = json.dumps(dict)
    client.sendall(bytes(data, encoding=FORMAT))

send_json({"id": 2})