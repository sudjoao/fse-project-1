import json
import socket
import threading

HEADER = 1024
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)



class CentralServer:
    def __init__(self) -> None:
        self.car_pass = 0
        self.red_cars = 0
        self.fast_cars = 0
        self.speed_cars = 0   
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR) 

    def handle_client(self, conn, addr):
        print(f'[NEW CONNECTION] {addr} connected')
        while True:
            json_msg = conn.recv(HEADER).decode(FORMAT)
            print(f'json_msg: {json_msg}')
            print(type(json_msg))
            msg = json.loads(json_msg)
            if msg['type'] == 'car_pass':
                self.car_pass+=1
            elif msg['type'] == 'red_light':    
                self.red_cars+=1
            elif msg['type'] == 'fast_car':
                self.fast_cars+=1


    def start(self):
        print('[LISTENING] server is listening')
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'[ACTIVES CONNECTIONS] {threading.active_count() - 1}')

    def menu(self):
        while True:
            option = input('Digite uma das seguintes opções:\n1. Verificar carros por minuto\n2. Verificar velocidade média\n3.Números de Infrações\n4. Modo de emergência\n5. Modo noturno\n')
            while option != '1' and option != '2' and option != '3' and option != '4' and option != '5':
                option = input('Opção inválida. Digite uma das seguintes opções:\n1. Verificar carros por minuto\n2. Verificar velocidade média\n3.Números de Infrações\n4. Modo de emergência\n5. Modo noturno\n')
            if option == '1':
                print(f'Quantidade de carros que passaram nos últimos minutos: {self.car_pass}')
            elif option == '2':
                print(f'Velocidade média: {self.speed_cars / self.car_pass}')
            elif option == '3':
                print(f'Quantidade que ultrapassaram o sinal vermelho: {self.red_cars}')
                print(f'Quantidade que ultrapassaram a velocidade da via: {self.fast_cars}')


central_server = CentralServer()
thread = threading.Thread(target=central_server.menu, args=[])
thread.start()
print('[STARTING] server is starting...')
central_server.start()