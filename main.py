import RPi.GPIO as GPIO
import time
from light import Light
from main_controller import MainController

from trafic_light import TraficLight
from trafic_light_controller import TraficLightController
def main():
    GPIO.setmode(GPIO.BCM)
    main_controller = MainController(GPIO)
    GPIO.setup(main_controller.lights_ports, GPIO.OUT)
    GPIO.setup(main_controller.buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(main_controller.speed_sensors[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(main_controller.speed_sensors[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(main_controller.pass_sensors[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(main_controller.pass_sensors[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    main_controller.config()
    main_controller.run_lights()

main()
