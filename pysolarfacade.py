from pysolar import solar
from pysolar import radiation
import datetime

class PySolarFacade:
    def altitude(self, latitude : float, longitude : float, date : datetime) -> float:
        return solar.get_altitude(latitude, longitude, date)
    
    def azimuth(self, latitude : float, longitude : float, date : datetime) -> float:
        return solar.get_azimuth(latitude, longitude, date)

    def radiation_direct(self, latitude : float, longitude : float, altitude: float, date : datetime) -> float:
        altitude_deg = solar.get_altitude(latitude, longitude, date)
        return radiation.get_radiation_direct(date, altitude_deg)