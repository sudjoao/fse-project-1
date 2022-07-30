import RPi.GPIO as GPIO
import time
from light import Light

from trafic_light import TraficLight
from trafic_light_controller import TraficLightController

trafic_lights_outputs = [[1, 26, 21], [20, 16, 12]]
buttons = [8, 7]
GPIO.setmode(GPIO.BCM)
GPIO.setup([1, 26, 21, 20, 16, 12], GPIO.OUT)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
trafic_lights = []

def button_callback(button):
    while trafic_light_controller.min_time_locked:
        print('travado')
    print('destravou')
    trafic_light_controller.turn_off_all_lights()
    if button == 8:
        trafic_light_controller.current_state_index = 2
    else:
        trafic_light_controller.current_state_index = 5


for  trafic_light in trafic_lights_outputs:
    lights = []
    for i, light_port in enumerate(trafic_light):
        light = Light(light_port, 2-i, 3-i)
        lights.append(light)
    trafic_lights.append(TraficLight(*lights))
    
trafic_light_controller = TraficLightController(GPIO, trafic_lights)
for button in buttons:
    GPIO.add_event_detect(button, GPIO.RISING, button_callback)
i = 0
while i < 5:
    trafic_light_controller.turn_on_lights()
    i+=1
trafic_light_controller.turn_off_all_lights()
