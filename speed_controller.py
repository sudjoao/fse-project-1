from datetime import datetime
import time


class SpeedController:
    def __init__(self, sensor1, sensor2) -> None:
        self.sensor1a_time = 0
        self.sensor1b_time = 0
        self.sensor1 = sensor1
        self.sensor2 = sensor2
    
    def speed_callback(self, button):
        print(button)
        if button == self.sensor1:
            self.sensor1a_time = datetime.now()
        elif button == self.sensor2:
            self.sensor1b_time = datetime.now()
            if self.sensor1a_time != 0:
                self.get_time_difference()

    def get_time_difference(self):
        time_difference = self.sensor1b_time- self.sensor1a_time
        velocity_in_ms = 1 / time_difference.total_seconds()
        velocity_in_kmh = int(velocity_in_ms * 3.6)
        print(f'A velocidade do carro foi: {velocity_in_kmh} km/h')
        self.sensor1a_time = 0
        self.sensor1b_time = 0
