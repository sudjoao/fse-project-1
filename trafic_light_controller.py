import time
from trafic_light import TraficLight
class TraficLightController:
    def __init__(self, gpio, lights: list):
        self.gpio = gpio
        self.states = ['001001', '100001', '010001', '001001', '001100', '001010']
        self.lights = lights.copy()
        self.current_state_index = 0
        self.min_time_locked = True
    
    def turn_off_lights_list(self, lights):
        for light in lights:
            self.gpio.output(light, self.gpio.LOW)

    def turn_on_lights_list(self, lights):
        for light in lights:
            self.gpio.output(light, self.gpio.HIGH)

    def turn_off_all_lights(self):
            self.turn_off_lights_list([
                self.lights[0].green_light.port,
                self.lights[1].green_light.port,
                self.lights[0].yellow_light.port,
                self.lights[1].yellow_light.port,
                self.lights[0].red_light.port,
                self.lights[1].red_light.port,
            ])
            time.sleep(1)

    def turn_on_lights(self):
        if self.states[self.current_state_index] == '001001':
            self.turn_off_lights_list([self.lights[0].yellow_light.port, self.lights[1].yellow_light.port])
            self.turn_on_lights_list([self.lights[0].red_light.port, self.lights[1].red_light.port])
            time.sleep(1)
            self.min_time_locked = False
            
        elif self.states[self.current_state_index] == '100001':
            self.turn_off_lights_list([self.lights[0].red_light.port])
            self.turn_on_lights_list([self.lights[0].green_light.port, self.lights[1].red_light.port])
            self.min_time_locked = True
            time.sleep(self.lights[0].green_light.min_time)
            self.min_time_locked = False
            time.sleep(self.lights[0].green_light.max_time - self.lights[0].green_light.min_time)
    
        elif self.states[self.current_state_index] == '010001':
            self.turn_off_lights_list([self.lights[0].green_light.port])
            self.turn_on_lights_list([self.lights[0].yellow_light.port, self.lights[1].red_light.port])
            self.min_time_locked = True
            time.sleep(self.lights[0].yellow_light.min_time)
            self.min_time_locked = False
            time.sleep(self.lights[0].yellow_light.max_time - self.lights[0].yellow_light.min_time)

        elif self.states[self.current_state_index] == '001100': 
            self.turn_off_lights_list([self.lights[1].red_light.port])
            self.turn_on_lights_list([self.lights[1].green_light.port, self.lights[0].red_light.port])
            self.min_time_locked = True
            time.sleep(self.lights[1].green_light.min_time)
            self.min_time_locked = False
            time.sleep(self.lights[1].green_light.max_time - self.lights[1].green_light.min_time)

        elif self.states[self.current_state_index] == '001010':
            self.turn_off_lights_list([self.lights[1].green_light.port])
            self.turn_on_lights_list([self.lights[1].yellow_light.port, self.lights[0].red_light.port])
            self.min_time_locked = True
            time.sleep(self.lights[1].yellow_light.min_time)
            self.min_time_locked = False
            time.sleep(self.lights[1].yellow_light.max_time - self.lights[1].yellow_light.min_time)
        
        if self.current_state_index < len(self.states)-1:
            self.current_state_index+=1
        else:
            self.current_state_index = 0
    
    def is_red(self, port):
        if self.current_state_index == 0 or self.current_state_index == 3:
            return True
        print(port)
        if port == 18:
            main_red_states = ['001100', '001010']
            return self.states[self.current_state_index] in main_red_states
        if port == 24:
            secondary_red_states = ['100001', '010001']
            return self.states[self.current_state_index] in secondary_red_states
    
    def get_min_time_locked(self):
        return self.min_time_locked