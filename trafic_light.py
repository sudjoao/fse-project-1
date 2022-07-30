from light import Light

class TraficLight:
    def __init__(self, green_light: Light, yellow_light: Light, red_light: Light):
        self.green_light = green_light
        self.yellow_light = yellow_light
        self.red_light = red_light
    def __str__(self) -> str:
        return f"red: {self.red_light.port} yellow: {self.yellow_light.port} green: {self.green_light.port}"