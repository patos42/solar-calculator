from unittest import TestCase
from optimiser import Optimiser

class TestAnalysis(TestCase):
    def test_find_optimal_angle_annual(self) -> None:
        optimiser : Optimiser = Optimiser()
        optimiser.calculate_optimal_angle()

    def test_find_optimal_angle_june(self) -> None:
        optimiser : Optimiser = Optimiser()
        optimiser.calculate_max_june_angle()

    def test_show_monthly(self) -> None:
        optimiser : Optimiser = Optimiser()
        optimiser.print_monthly_output(40)
    
    def test_find_optimal_angle_cost(self) -> None:
        optimiser : Optimiser = Optimiser()
        optimiser.solve_max_power_cost()

    def test_find_optimal_angle_cost(self) -> None:
        optimiser : Optimiser = Optimiser()
        optimiser.print_annual_power_degrees()

        