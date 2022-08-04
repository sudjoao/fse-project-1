import time
from client_controller import ClientController
from trafic_light import TraficLight
class TraficLightController:
    def __init__(self, gpio, lights: list):
        self.gpio = gpio
        self.states = ['001001', '100001', '010001', '001001', '001100', '001010']
        self.lights = lights.copy()
        self.current_state_index = 0
        self.min_time_locked = True
        self.button_was_pressed = False
        self.client = ClientController()

    def turn_trafic_lights(self, trafic_type, turn, red=False, yellow=False, green=False):
        if trafic_type == 'main':
            trafic1 = 0
        else:
            trafic1 = 1

        if turn == 'off':
            turn_type = self.gpio.LOW
        else:
            turn_type = self.gpio.HIGH
        
        if red:
            self.gpio.output(self.lights[trafic1].red_light.port, turn_type)
        if yellow:
            self.gpio.output(self.lights[trafic1].yellow_light.port, turn_type)
        if green:
            self.gpio.output(self.lights[trafic1].green_light.port, turn_type)


    def turn_off_all_lights(self):
            self.turn_trafic_lights('secondary', 'off', red=True, yellow=True, green=True)
            self.turn_trafic_lights('main', 'off', red=True, yellow=True, green=True)
            time.sleep(1)

    def turn_on_lights(self):
        if self.states[self.current_state_index] == '001001':
            self.turn_trafic_lights('main', turn='off',  yellow=True, green=True)
            self.turn_trafic_lights('main', turn='on',  red=True)
            self.turn_trafic_lights('secondary', turn='off', yellow=True, green=True)
            self.turn_trafic_lights('secondary', turn='on', red=True)
            time.sleep(1)
            self.min_time_locked = False
            if self.button_was_pressed:
                self.button_was_pressed = False
            
        elif self.states[self.current_state_index] == '100001':
            self.turn_trafic_lights('main', turn='off', red=True)
            self.turn_trafic_lights('main', turn='on', green=True)
            self.turn_trafic_lights('secondary', turn='on', red=True)
            self.min_time_locked = True
            time.sleep(self.lights[0].green_light.min_time)
            self.min_time_locked = False
            current_time = 1
            while current_time < self.lights[0].green_light.max_time - self.lights[0].green_light.min_time:
                if not self.button_was_pressed:
                    time.sleep(1)
                    current_time+= 1
                else:
                    break
        elif self.states[self.current_state_index] == '010001':
            self.turn_trafic_lights('main', turn='off', green=True)
            self.turn_trafic_lights('main', turn='on', yellow=True)
            self.turn_trafic_lights('secondary', turn='on', red=True)
            self.min_time_locked = True
            time.sleep(self.lights[0].yellow_light.min_time)
            self.min_time_locked = False
            current_time = 1
            while current_time < self.lights[0].yellow_light.max_time - self.lights[0].yellow_light.min_time:
                if not self.button_was_pressed:
                    time.sleep(1)
                    current_time+= 1
                else:
                    break
        elif self.states[self.current_state_index] == '001100':
            self.turn_trafic_lights('secondary', turn='off', red=True)
            self.turn_trafic_lights('secondary', turn='on', green=True) 
            self.turn_trafic_lights('main', turn='on', red=True)
            self.min_time_locked = True
            time.sleep(self.lights[1].green_light.min_time)
            self.min_time_locked = False
            current_time = 1
            while current_time < self.lights[1].green_light.max_time - self.lights[1].green_light.min_time:
                if not self.button_was_pressed:
                    time.sleep(1)
                    current_time+= 1
                else:
                    break
        elif self.states[self.current_state_index] == '001010':
            self.turn_trafic_lights('secondary', turn='off', green=True)
            self.turn_trafic_lights('secondary', turn='on', yellow=True) 
            self.turn_trafic_lights('main', turn='on', red=True)
            self.min_time_locked = True
            time.sleep(self.lights[1].yellow_light.min_time)
            self.min_time_locked = False
            current_time = 1
            while current_time < self.lights[1].yellow_light.max_time - self.lights[1].yellow_light.min_time:
                if not self.button_was_pressed:
                    time.sleep(1)
                    current_time+= 1
                else:
                    break
        if self.current_state_index < len(self.states)-1:
            self.current_state_index+=1
        else:
            self.current_state_index = 0
    
    def is_red(self, port):
        if self.current_state_index == 0 or self.current_state_index == 3:
            self.client.send_json({'type': 'red_light'})
            return True
        print(port)
        if port == 18 or port == 22:
            main_red_states = ['001100', '001010']
            self.client.send_json({'type': 'red_light'})
            return self.states[self.current_state_index] in main_red_states
        if port == 24 or port == 19:
            secondary_red_states = ['100001', '010001']
            self.client.send_json({'type': 'red_light'})
            return self.states[self.current_state_index] in secondary_red_states
    
    def get_min_time_locked(self):
        return self.min_time_locked