from light import Light
from speed_controller import SpeedController
from trafic_light import TraficLight
from trafic_light_controller import TraficLightController


class MainController:
    def __init__(self, gpio) -> None:
        self.gpio = gpio
        self.lights_ports = [1, 26, 21, 20, 16, 12]
        # self.lights_min_times = [10, 3, 5, 5, 3, 1]
        # self.lights_max_times = [20, 3, 10, 10, 3, 20]
        self.lights_min_times = [3, 3, 2, 2, 3, 1]
        self.lights_max_times = [5, 3, 3, 3, 3, 2]
        self.buttons = [8, 7]
        self.speed_sensors = [[23, 18], [25, 24]]
        self.pass_sensors = [14, 15]
        self.speed_controllers = []

    def config(self):
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
        
        self.trafic_light_controller = TraficLightController(self.gpio, trafic_lights)

        for button in self.buttons:
            self.gpio.add_event_detect(button, self.gpio.RISING, self.button_callback)
        for sensors in self.speed_sensors:
            self.speed_controllers.append(SpeedController(self.trafic_light_controller.is_red))
        for sensor in self.pass_sensors:
            self.gpio.add_event_detect(sensor, self.gpio.RISING, self.button_callback)
        for i, sensors in enumerate(self.speed_sensors):
            for sensor in sensors:
                self.gpio.add_event_detect(sensor, self.gpio.RISING, self.speed_controllers[i].speed_callback)
        self.trafic_light_controller.turn_off_all_lights()
    def button_callback(self, button):
        while self.trafic_light_controller.min_time_locked:
            print('travado')
        print('destravou')
        self.trafic_light_controller.turn_off_all_lights() 
        if button == 8 or button == 14:
            self.trafic_light_controller.current_state_index = 2
        else:
            self.trafic_light_controller.current_state_index = 5
        self.gpio.remove_event_detect(button)
        self.gpio.add_event_detect(button, self.gpio.FALLING, self.button_callback_down)

    def button_callback_down(self, button):
        if self.trafic_light_controller.is_red(button):
            print('furou o sinal vermelho')
        self.gpio.remove_event_detect(button)
        self.gpio.add_event_detect(button, self.gpio.RISING, self.button_callback)


    def run_lights(self):
        while True:
            self.trafic_light_controller.turn_on_lights()