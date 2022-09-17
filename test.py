from unittest import TestCase
from photovoltaiceducation import PhotoVoltaicEducation
from pysolarfacade import PySolarFacade
from datetime import datetime, timezone

from solarcalculator import SolarResult

class TestFormulas(TestCase):
    def test_power_density(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.radiant_power_density(3)
        self.assertAlmostEqual(result, 1397.6, 1)

    def test_simple_airmass(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.air_mass_approx(30)
        self.assertAlmostEqual(result, 1.1547, 4)

    def test_compelex_airmass(self) -> None:
            formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
            result : float = formulas.air_mass(30)
            print(result)

    def test_intensity_direct(self) -> None:
            formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
            result : float = formulas.intensity_direct(1.5)
            self.assertAlmostEqual(result, 846, 0)

    def test_intensity_direct_elivation(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.intensity_direct_elivation(1.5, 0)
        self.assertAlmostEqual(result, 846, 0)

    def test_intensity_global(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.intensity_direct(1.5)
        total : float = formulas.intensity_global(result)
        self.assertAlmostEqual(total, 930.6, 0)
    
    def test_pysolar_sun_altitude(self) -> None:
        formulas : PySolarFacade = PySolarFacade()
        date : datetime = datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=timezone.utc)
        result : float = formulas.altitude(42.206, -71.381, date)
        self.assertAlmostEqual(result, 30.9144, 3)

    def test_pysolar_sun_azimuth(self) -> None:
        formulas : PySolarFacade = PySolarFacade()
        date : datetime = datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=timezone.utc)
        result : float = formulas.azimuth(42.206, -71.381, date)
        self.assertAlmostEqual(result, 149.24, 1)

    def test_pysolar_radiation(self) -> None:
        formulas : PySolarFacade = PySolarFacade()
        date : datetime = datetime(2007, 2, 18, 15, 13, 1, 130320, tzinfo=timezone.utc)
        result : float = formulas.radiation_direct(42.206, -71.381, 0,date)
        #self.assertAlmostEqual(result, 909.582292149944, 1)

    def test_lst(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        longitude : float = 150
        timezone: float = 10
        lstm : float = formulas.local_standard_time_meridian(timezone)
        self.assertAlmostEqual(lstm,150, 1)
        eot : float = formulas.equation_of_time(5)
        self.assertAlmostEqual(eot,-5.45, 2)
        tc : float = formulas.time_correction_factor(longitude, lstm, eot)
        self.assertAlmostEqual(tc,-5.45, 2)
        lst : float = formulas.local_solar_time(12.5, tc) # 12:30
        self.assertAlmostEqual(lst,12.4, 1)

    def test_elivation(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        date : datetime = datetime(2022, 1, 25, 12, 00, 0)
        longitude : float = 144.9631
        latitude : float = -37.8136
        timezone: float = 10
        lstm : float = formulas.local_standard_time_meridian(timezone)
        self.assertAlmostEqual(lstm,150, 1)
        day_of_year : int = date.timetuple().tm_yday
        eot : float = formulas.equation_of_time(day_of_year)
        self.assertAlmostEqual(eot,-12.31, 2)
        tc : float = formulas.time_correction_factor(longitude, lstm, eot)
        self.assertAlmostEqual(tc,-32.46, 2)
        lst : float = formulas.local_solar_time(date.hour + date.minute/60, tc)
        self.assertAlmostEqual(lst,11.460, 2)
        hra : float = formulas.hour_angle(lst)
        self.assertAlmostEqual(hra,-8.114, 2)
        declination : float = formulas.declination(day_of_year)
        self.assertAlmostEqual(declination,-19.26, 2)
        elivation : float = formulas.elivation(declination, latitude, hra)
        self.assertAlmostEqual(elivation,70.149, 2)
        azimuth : float  = formulas.azimuth(declination, latitude, hra, elivation)
        self.assertAlmostEqual(azimuth,23.103, 2)

    def test_all_pve(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        date : datetime = datetime(2022, 1, 25, 12, 00, 0)
        longitude : float = 144.9631
        latitude : float = -37.8136
        timezone: float = 10
        result : SolarResult = formulas.calculate(latitude, longitude, 0, date, timezone)
        pysolar : PySolarFacade = PySolarFacade()
        pysolar_result : SolarResult = pysolar.calculate(latitude, longitude, 0, date, 10)
        self.assertAlmostEqual(result.azimuth, pysolar_result.azimuth, 0)
        self.assertAlmostEqual(result.elivation, pysolar_result.elivation, 0)
        #self.assertAlmostEqual(result.solar_radiation, pysolar_result.solar_radiation, 0) # 10% off.



        


    def test_tilt(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        tilt : float = 15
        latitude : float = 30
        declination : float = formulas.declination(30)
        hra : float = formulas.hour_angle(12)
        elivation : float = formulas.elivation(declination, latitude, hra)
        factor : float = formulas.tilted_surface_radiation_factor(elivation, tilt)
        self.assertAlmostEqual(factor,0.8383, 4)

    def test_orientation(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        tilt : float = 15
        latitude : float = 30
        declination : float = formulas.declination(30)
        hra : float = formulas.hour_angle(12)
        elivation : float = formulas.elivation(declination, latitude, hra)
        factor : float = formulas.orientation_tilt_factor(elivation, 90, tilt, 90)
        self.assertAlmostEqual(factor,0.8383, 4)
