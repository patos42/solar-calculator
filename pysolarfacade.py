from threading import local
from pysolar import solar
from pysolar import radiation
from datetime import datetime, timedelta, timezone
from solarcalculator import SolarResult
import math

from solarcalculator import SolarCalculator

class PySolarFacade(SolarCalculator):
    def calculate(self, latitude: float, longitude: float, panel_elivation : float, local_time: datetime, timezone_adjustment : float) -> SolarResult:
        
        whole_hours : int = math.floor(timezone_adjustment)
        minutes : int = int(round((timezone_adjustment - whole_hours) * 60,0))
        utc_time = local_time - timedelta(hours = whole_hours, minutes= minutes)
        utc_time = utc_time.replace(tzinfo=timezone.utc)
        alt : float = self.altitude(latitude, longitude, utc_time)
        az : float = self.azimuth(latitude, longitude, utc_time)
        if (alt < 0):
            return SolarResult(0, alt, az)
        radiation_direct : float = self.radiation_direct(latitude, longitude, alt, utc_time)
        return SolarResult(radiation_direct * 1.1, alt, az) # *1.1 to convert direct to total.

    def altitude(self, latitude : float, longitude : float, date : datetime) -> float:
        return solar.get_altitude(latitude, longitude, date) # type: ignore
    
    def azimuth(self, latitude : float, longitude : float, date : datetime) -> float:
        return solar.get_azimuth(latitude, longitude, date) # type: ignore

    def radiation_direct(self, latitude : float, longitude : float, altitude: float, date : datetime) -> float:
        return radiation.get_radiation_direct(date, altitude) # type: ignore