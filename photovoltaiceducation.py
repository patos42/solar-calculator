from datetime import datetime
import math
from pysolar.solar import *
from solarcalculator import SolarCalculator, SolarResult

# Implementation as described on:
# https://www.pveducation.org/pvcdrom/welcome-to-pvcdrom
class PhotoVoltaicEducation(SolarCalculator):
    # Returns power density in W/m^2.
    def radiant_power_density(self, day_of_year: int) -> float:
        return (1+ 0.033*self.cos(360*(day_of_year - 2)/365)) * 1.353 * 1000
    
    #The air mass represents the proportion of atmosphere that the 
    #light must pass through before striking the Earth relative to 
    # its overhead path length
    def air_mass_approx(self, zenith : float) -> float:
        return 1/self.cos(zenith)

    def air_mass(self, zenith : float) -> float:
        inverse : float = self.cos(zenith) + 0.50572 * (96.07995 - zenith)**(-1.6364) # type: ignore
        return 1/inverse

    # The intensity of the direct component of sunlight throughout 
    # each day can be determined as a function of air mass
    # W/m^2
    def intensity_direct(self, airmass : float) -> float:
        s : float = 1.353 * 1000 # solar_constant
        e : float = 0.7 # radiation_incident_efficiency
        AM : float = airmass
        return s * e**(AM**0.678) # type: ignore
    
    def intensity_direct_elivation(self, airmass : float, elivation_km : float) -> float:
        s : float = 1.353 * 1000 # solar_constant
        e : float = 0.7 # radiation_incident_efficiency
        a : float = 0.14 # fitted parameter?
        h : float = elivation_km
        AM: float = airmass
        return s*((1-a*h)*e**(AM**0.678) + a*h) # type: ignore

    def intensity_global(self, intensity_direct : float) -> float:
        return intensity_direct * 1.1

    #The Local Standard Time Meridian (LSTM) is a reference meridian used for a particular 
    #time zone and is similar to the Prime Meridian, which is used for Greenwich Mean Time.
    # returns degrees
    #https://www.pveducation.org/pvcdrom/properties-of-sunlight/the-suns-position
    def local_standard_time_meridian(self, gmt_time_difference: float) -> float:
        return gmt_time_difference * 15
    
    #The equation of time (EoT) (in minutes) is an empirical equation that corrects for 
    # the eccentricity of the Earth's orbit and the Earth's axial tilt.
    # returns minutes
    def equation_of_time(self, day_of_year: int) -> float:
        d : float = day_of_year
        B : float = (360/365)*(d - 81)
        return 9.87 * self.sin(2 * B) - 7.53 * self.cos(B) - 1.5 * self.sin(B)
    
    #The net Time Correction Factor (in minutes) accounts for the variation of the Local Solar 
    # Time (LST) within a given time zone due to the longitude variations within the time zone 
    # and also incorporates the EoT above.
    # returns minutes
    def time_correction_factor(self, longitude : float, LSTM : float, EoT : float) -> float:
        return 4 * (longitude - LSTM) + EoT
    
    def local_solar_time(self, local_time : float, time_correction : float) -> float:
        LT : float = local_time
        TC : float = time_correction
        return LT + TC/60
    
    #The Hour Angle converts the local solar time (LST) into the number of degrees which the sun 
    # moves across the sky. By definition, the Hour Angle is 0° at solar noon. Since the Earth 
    # rotates 15° per hour, each hour away from solar noon corresponds to an angular motion of 
    # the sun in the sky of 15°. In the morning the hour angle is negative, in the afternoon the 
    # hour angle is positive.
    def hour_angle(self, local_solar_time : float) -> float:
        return 15 * (local_solar_time - 12)

    # The declination of the sun is the angle between the equator and a line drawn from the centre 
    # of the Earth to the centre of the sun.
    # day is the number of days since the start of the year.
    def declination(self, day : int) -> float:
        return 23.45 * self.sin((360/365)*(day - 81))

    #The elevation angle (used interchangeably with altitude angle) is the angular height of the 
    # sun in the sky measured from the horizontal. 
    def elivation(self, declination : float, latitude : float, hour_angle : float) -> float:
        sin_a : float = self.sin(declination) * self.sin(latitude) + self.cos(declination) * self.cos(latitude) * self.cos(hour_angle)
        a = math.asin(sin_a)
        return math.degrees(a)
    
    def azimuth(self, declination : float, latitude : float, hour_angle : float, elivation: float) -> float:
        a = self.sin(declination) * self.cos(latitude) - self.cos(declination) * self.sin(latitude) * self.cos(hour_angle)
        azimuth_radians = math.acos(a / self.cos(elivation))
        degrees : float = math.degrees(azimuth_radians)
        if (hour_angle > 0):
            return 360 - degrees
        return degrees

    def calculate(self, latitude: float, longitude: float, panel_elivation : float, local_time: datetime, timezone_adjustment : float) -> SolarResult:
        lstm : float = self.local_standard_time_meridian(timezone_adjustment)
        day_of_year : int = local_time.timetuple().tm_yday
        eot : float = self.equation_of_time(day_of_year)
        tc : float = self.time_correction_factor(longitude, lstm, eot)
        lst : float = self.local_solar_time(local_time.hour + local_time.minute/60, tc)
        hra : float = self.hour_angle(lst)
        declination : float = self.declination(day_of_year)
        solar_elivation : float = self.elivation(declination, latitude, hra)
        azimuth : float  = self.azimuth(declination, latitude, hra, solar_elivation)
        
        # Night time - no need to calculate intensity.
        if (solar_elivation < 0):
            return SolarResult(0, solar_elivation, azimuth)    
        
        zenith : float = 90 - solar_elivation
        airmass : float = self.air_mass(zenith)
        intensity_direct : float = self.intensity_direct_elivation(airmass, panel_elivation)
        intensity_total : float = self.intensity_global(intensity_direct)
        return SolarResult(intensity_total, solar_elivation, azimuth)
