from datetime import datetime
from typing import Final

class SolarResult:
    def __init__(self, solar_radiation : float, elivation : float, azimuth : float) -> None:
        self.solar_radiation : Final = solar_radiation
        self.elivation : Final = elivation
        self.azimuth : Final = azimuth

class SolarCalculator:
    def calculate(self, latitude : float, longitude : float, panel_elivation : float, local_time : datetime, timezone_adjustment : float) -> SolarResult:
        pass

