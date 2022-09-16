from datetime import datetime, timedelta
from photovoltaiceducation import PhotoVoltaicEducation
from solarcalculator import SolarResult
import scipy.optimize

class Optimiser:
    def __init__(self) -> None:
        self.calculator = PhotoVoltaicEducation()
    
    def optimal_angle(self):
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        total_light : float = 0
        count = 0
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, 32, 7)
            total_light += result.solar_radiation * oreintation_factor
            date = date + timedelta(minutes=30)
        print()
        print(total_light)
    
    def calculate_optimal_angle(self):
        max_x : float = scipy.optimize.fmin(lambda x: -self.f(x), 30)
        print(max_x)

    def calculate_max_june_angle(self):
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        max_x : float = scipy.optimize.fmin(lambda x: -self.calculate_monthly_power(longitude, latitude, altitude, timezone, x)[6], 30)
        print(max_x)

    def f(self, tilt : float) -> float:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        return self.calculate_annual_power(longitude, latitude, altitude, timezone, tilt)

    def calculate_annual_power(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float) -> float:
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        total_light : float = 0
        delta : int = 10
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, tilt, 7)
            total_light += result.solar_radiation * oreintation_factor * delta/60
            date = date + timedelta(minutes=delta)
        return total_light

    def print_monthly_output(self, angle : float)-> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        array = self.calculate_monthly_power(longitude, latitude, altitude, timezone, angle)
        for a in array:
            print(a)

    def solve_max_power_cost(self):
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        max_x : float = scipy.optimize.fmin(lambda x: -self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, x), 30)
        print(max_x)

    def print_annual_power_degrees(self):
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 15))
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 20))
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 25))
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 30))
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 35))
        print(self.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 40))

    def calculate_annual_power_cost(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float):
        cost_table = [0]*13
        cost_table[1] = 1.1
        cost_table[2] = 1
        cost_table[3] = 1.4
        cost_table[4] = 1.54
        cost_table[5] = 2.8
        cost_table[6] = 3.9
        cost_table[7] = 3.1
        cost_table[8] = 1.47
        cost_table[9] = 1.06
        cost_table[10] = 1.08
        cost_table[11] = 1.7
        cost_table[12] = 2.27
        array = self.calculate_monthly_power(longitude, latitude, altitude, timezone, tilt)
        total : float = 0
        for i in range(0,13):
            total+= array[i] * cost_table[i]
        return total



    def calculate_monthly_power(self, longitude : float, latitude : float, altitude: float, timezone : float, tilt : float):
        date : datetime = datetime(2022,1,1)
        end_date : datetime = datetime(2023,1,1)
        delta : int = 10
        months = [0] * 13
        while date < end_date:
            result : SolarResult = self.calculator.calculate(latitude, longitude, altitude, date, timezone)
            oreintation_factor = self.calculator.orientation_tilt_factor(result.elivation, result.azimuth, tilt, 7)
            months[date.month] += result.solar_radiation * oreintation_factor * delta/60
            date = date + timedelta(minutes=delta)
        return months
        #print(str(result.elivation) + "\t" + str(result.azimuth) + "\t" + str(result.solar_radiation))
        
