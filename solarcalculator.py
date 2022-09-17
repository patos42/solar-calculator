from datetime import datetime
from typing import Final
import math

class SolarResult:
    def __init__(self, solar_radiation : float, elivation : float, azimuth : float) -> None:
        self.solar_radiation : Final = solar_radiation
        self.elivation : Final = elivation
        self.azimuth : Final = azimuth

class SolarCalculator:
    def calculate(self, latitude : float, longitude : float, panel_elivation : float, local_time : datetime, timezone_adjustment : float) -> SolarResult:
        pass
    
    # Cosine function that accepts degrees as input.
    def cos(self, degrees: float) -> float:
        return math.cos(math.radians(degrees))

    # Sine function that accepts degrees as input.
    def sin(sle, degrees: float) -> float:
        return math.sin(math.radians(degrees))

    def tilted_surface_radiation_factor(self, elivation : float, tilt_angle : float) -> float:
        return self.sin(elivation + tilt_angle)

    def orientation_tilt_factor(self, elivation : float, azimuth : float, module_tilt : float, module_angle : float) -> float:
        return self.cos(elivation) * self.sin(module_tilt) * self.cos(module_angle - azimuth) + self.sin(elivation) * self.cos(module_tilt)

