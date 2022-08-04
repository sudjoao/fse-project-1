from datetime import datetime
import time


class SpeedController:
    def __init__(self, is_red, send_fast_car_infract) -> None:
        self.sensor_time = 0
        self.is_red = is_red
        self.cars_qtt = 0
        self.red_pass_qtt = 0
        self.send_fast_car_infract = send_fast_car_infract

    def speed_callback(self, button):
        print(button)
        if self.sensor_time == 0:
            self.sensor_time = datetime.now()

        else:
            self.cars_qtt +=1
            self.get_time_difference(datetime.now())
            if self.is_red(button):
                self.red_pass_qtt +=1
                print('furou o sinal vermelho')


    def get_time_difference(self, time):
        time_difference = time- self.sensor_time # s
        velocity_in_ms = 1 / time_difference.total_seconds() # 1 m/ s
        velocity_in_kmh = int(velocity_in_ms * 3.6)
        if velocity_in_kmh > 60:
            print('Ultrapassou o limite da via')
            self.send_fast_car_infract()
        print(f'A velocidade do carro foi: {velocity_in_kmh} km/h')
        self.sensor_time = 0
