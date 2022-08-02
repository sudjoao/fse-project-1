import time
from light import Light
from main_controller import MainController

from trafic_light import TraficLight
from trafic_light_controller import TraficLightController
def main():
    option = input('Qual configuração de GPIO você deseja usar? Digite 1 para GPIO 1 e 2 para GPIO 2:\n')
    while option != '1' and option !='2':
        option = input('Opção inválida. Digite 1 para GPIO 1 e 2 para GPIO 2')
    main_controller = MainController(int(option))
    main_controller.config()
    main_controller.run_lights()

main()
