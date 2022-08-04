from light import Light
from speed_controller import SpeedController
from trafic_light import TraficLight
from trafic_light_controller import TraficLightController
import RPi.GPIO as GPIO

class MainController:
    def __init__(self, config) -> None:
        GPIO.setmode(GPIO.BCM)
        self.lights_ports = [1, 26, 21, 20, 16, 12] if config == 1 else [2, 3, 11, 0, 5, 6]
        # self.lights_min_times = [10, 3, 5, 5, 3, 1]
        # self.lights_max_times = [20, 3, 10, 10, 3, 20]
        self.lights_min_times = [3, 3, 2, 2, 3, 1]
        self.lights_max_times = [5, 3, 3, 3, 3, 2]
        self.buttons = [8, 7]if config == 1 else [10, 9]
        self.speed_sensors = [[23, 18], [25, 24]] if config == 1 else [[27, 22], [13, 19]]
        self.pass_sensors = [14, 15] if config == 1 else  [4, 17]
        self.speed_controllers = []
    

    def config(self):
        GPIO.setup(self.lights_ports, GPIO.OUT)
        GPIO.setup(self.buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for sensors in self.speed_sensors:
            GPIO.setup(sensors, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pass_sensors, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
        lights = []
        for i, port in enumerate(self.lights_ports):
            lights.append(Light(port, self.lights_min_times[i], self.lights_max_times[i]))

        lights_tuple = []
        i = 3
        while i <= len(lights)+1:
            lights_tuple.append(lights[i-3: i])
            i+=3

        trafic_lights = []

        for i, lights_list in enumerate(lights_tuple):
            trafic_lights.append(TraficLight(*lights_list))
        
        self.trafic_light_controller = TraficLightController(GPIO, trafic_lights)

        for button in self.buttons:
            GPIO.add_event_detect(button, GPIO.RISING, self.button_callback)
        for sensors in self.speed_sensors:
            self.speed_controllers.append(SpeedController(self.trafic_light_controller.is_red, self.trafic_light_controller.client.send_very_fast_cart))
        for sensor in self.pass_sensors:
            GPIO.add_event_detect(sensor, GPIO.RISING, self.button_callback)
        for i, sensors in enumerate(self.speed_sensors):
            for sensor in sensors:
                GPIO.add_event_detect(sensor, GPIO.RISING, self.speed_controllers[i].speed_callback)
        self.trafic_light_controller.turn_off_all_lights()

    def button_callback(self, button):
        while self.trafic_light_controller.min_time_locked:
            pass
        self.trafic_light_controller.button_was_pressed = True
        GPIO.remove_event_detect(button)
        GPIO.add_event_detect(button, GPIO.FALLING, self.button_callback_down)

    def button_callback_down(self, button):
        if self.trafic_light_controller.is_red(button):
            print('furou o sinal vermelho')
        GPIO.remove_event_detect(button)
        GPIO.add_event_detect(button, GPIO.RISING, self.button_callback)


    def run_lights(self):
        while True:
            self.trafic_light_controller.turn_on_lights()