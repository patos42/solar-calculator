from re import L
from unittest import TestCase
from optimiser import Optimiser
from photovoltaiceducation import PhotoVoltaicEducation
from pysolarfacade import PySolarFacade

class TestAnalysis(TestCase):
    def test_find_optimal_angle_annual(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())
        result : float = optimiser.calculate_optimal_angle(longitude, latitude, altitude, timezone)
        print(result) #32.1
        self.assertAlmostEqual(result, 32.1, 1)

    def test_find_optimal_angle_june(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())
        result : float = optimiser.calculate_optimal_june_angle(longitude, latitude, altitude, timezone)
        print(result)
        self.assertAlmostEqual(result, 64.7, 1) # seems high - should be around 50?

    def test_compare_optimal_to_average_optimal(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())
        result_32 : list[float] = optimiser.calculate_monthly_power(longitude, latitude, altitude, timezone, 32)
        result_15 : list[float] = optimiser.calculate_monthly_power(longitude, latitude, altitude, timezone, 15)
        result_49 : list[float] = optimiser.calculate_monthly_power(longitude, latitude, altitude, timezone, 49)
        for idx, x in enumerate(result_15):
            print(str(x) + "," + str(result_32[idx]) + "," + str(result_49[idx]))
        # Looks like an array of 15 degrees and another equal sized array of 49 degrees will give 4% less power than 32 degrees.
        # but with a similar annual power profile to 32 degrees. 

    def test_show_monthly(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())
        result : list[float] = optimiser.calculate_monthly_power(longitude, latitude, altitude, timezone, 50)
        for a in result:
            print(a)
    
    def test_find_optimal_angle_cost(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())

        cost_table : list[float] = [0]*13
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

        result : float = optimiser.solve_max_power_cost(longitude, latitude, altitude, timezone, cost_table)
        print(result)
        self.assertAlmostEqual(result, 37.875,2)

    def print_angle_vs_cost(self) -> None:
        longitude : float = 144.9631
        latitude : float = -37.8136
        altitude : float = 0
        timezone : float = 10

        cost_table : list[float] = [0]*13
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
        optimiser : Optimiser = Optimiser(PhotoVoltaicEducation())
        print(str(15)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 15, cost_table)))
        print(str(20)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 20, cost_table)))
        print(str(25)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 25, cost_table)))
        print(str(30)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 30, cost_table)))
        print(str(35)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 35, cost_table)))
        print(str(40)+ "\t" + str(optimiser.calculate_annual_power_cost(longitude, latitude, altitude, timezone, 40, cost_table)))

        