from datetime import datetime, timedelta
from photovoltaiceducation import PhotoVoltaicEducation
from solarcalculator import SolarResult
import scipy.optimize
from typing import Callable
from solarcalculator import SolarCalculator

class Optimiser:
    def __init__(self, calculator : SolarCalculator) -> None:
        self.calculator = calculator
        
    def optimal_angle(self,longitude : float, latitude : float, altitude : float, timezone : float) -> float:
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        total_light : float = 0
        time_delta_minutes : float = 30.0
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor : float = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, 32, 7)
            total_light += result.solar_radiation * oreintation_factor * time_delta_minutes / 60
            date = date + timedelta(minutes=time_delta_minutes)
        return total_light
    
    def calculate_optimal_angle(self, longitude : float, latitude : float, altitude : float, timezone : float) -> float:
        func: Callable[[float], float] = lambda x: -self.calculate_annual_power(longitude, latitude, altitude, timezone, x)
        guess : float = abs(latitude)
        max_x : float = scipy.optimize.fmin(func, guess, maxiter=5)[0].item() # type: ignore
        return max_x

    def calculate_optimal_june_angle(self, longitude : float, latitude : float, altitude : float, timezone : float) -> float:
        func: Callable[[float], float] = lambda x: -self.calculate_monthly_power(longitude, latitude, altitude, timezone, x)[6]
        max_x : float = scipy.optimize.fmin(func, 30)[0].item() # type: ignore
        return max_x

    def calculate_annual_power(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float) -> float:
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        total_light : float = 0
        delta : int = 30
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor : float = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, tilt, 7)
            total_light += result.solar_radiation * oreintation_factor * delta/60
            date = date + timedelta(minutes=delta)
        return total_light

    def solve_max_power_cost(self, longitude : float, latitude : float, altitude : float, timezone : float, cost_table : list[float]) -> float:
        func: Callable[[float], float] = lambda x: -self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, x, cost_table)
        max_x : float = scipy.optimize.fmin(func, 30, maxiter=6)[0].item() # type: ignore
        return max_x

    def calculate_annual_power_cost(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float, cost_table : list[float]) -> float:
        array = self.calculate_monthly_power(longitude, latitude, altitude, timezone, tilt)
        total : float = 0
        for i in range(0,13):
            total+= array[i] * cost_table[i]
        return total

    def calculate_monthly_power(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float) -> list[float]:
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        delta : int = 10
        months : list[float] = [0] * 13
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor : float = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, tilt, 7)
            months[date.month] += result.solar_radiation * oreintation_factor * delta/60
            date = date + timedelta(minutes=delta)
        return months
        
        
