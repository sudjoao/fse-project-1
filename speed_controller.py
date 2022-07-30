from datetime import datetime
import time


class SpeedController:
    def __init__(self, sensor1, sensor2) -> None:
        self.sensor1a_time = 0
        self.sensor1b_time = 0
        self.sensor1 = sensor1
        self.sensor2 = sensor2
    
    def speed_callback(self, button):
        if button == self.sensor1:
            self.sensor1a_time = datetime.now()
        elif button == self.sensor2:
            self.sensor1b_time = datetime.now()
            self.get_time_difference()

    def get_time_difference(self):
        time_difference = self.sensor1b_time- self.sensor1a_time
        print(f'A diferença de tempo entre a passagem 1 e 2 foi de: {time_difference.total_seconds()}')
        self.sensor1a_time = 0
        self.sensor1b_time = 0
