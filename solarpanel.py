from typing import Final

class Efficiency:
    def __init__(self, mpp_power : float, irradiance : float, panel_size : float):
        self.mpp_power : Final = mpp_power
        self.irradiance : Final = irradiance
        self.panel_size : Final = panel_size

class SolarPanel:
    # panel_size in m^2
    def __init__(self, efficiency : Efficiency, panel_size : float):
        self.efficiency : Final = efficiency
        self.panel_size : Final = panel_size
       
    # Returns w/m^2 power generated from w/m^2 solar insolation
    # Assume power output is linear. This is within 2% margin of error.
    def calculate_power(self, irradiance : float) -> float:
        return (irradiance / self.efficiency.irradiance) * self.efficiency.mpp_power

class PanelArray:
    def __init__(self, panel : SolarPanel, azimuth : float, tilt : float, number_of_panels : int):
        self.panel : Final = panel
        self.azimuth : Final = azimuth
        self.tilt : Final = tilt
        self.number_of_panels : Final = number_of_panels