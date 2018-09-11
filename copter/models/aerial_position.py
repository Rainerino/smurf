from django.conf import settings
from django.db import models

import dronekit

from copter.models.distance_func import coordinate_to_coordinate
from copter.models.gps_position import GpsPosition


class AerialPosition(models.Model):
    """Aerial position which consists of a GPS position and an altitude.
    This is useful as guided mode waypoint point, or current drone location
    Attributes:
        gps_position: GPS position.
        altitude_msl: Altitude (MSL) in feet.
    """
    gps_position = models.ForeignKey(GpsPosition, on_delete=models.CASCADE)
    relative_altitude = models.FloatField()

    def __str__(self):
        return "%s aerial at %s %s %s" % (
            self.pk, self.gps_position.latitude, self.gps_position.longitude, self.relative_altitude)

    def distance_to(self, other):
        """
        :param other:
        :return:
        """
        if type(other) is AerialPosition:
            if self.relative_altitude == other.relative_altitude and self.gps_position.duplicated(other.gps_position):
                return 0
            return coordinate_to_coordinate(self.gps_position.latitude, self.gps_position.longitude,
                                            self.relative_altitude,
                                            other.gps_position.latitude, other.gps_position.longitude,
                                            other.relative_altitude)
        elif type(other) is dronekit.LocationGlobalRelative:
            return coordinate_to_coordinate(self.gps_position.latitude, self.gps_position.longitude,
                                            self.relative_altitude,
                                            other.lat,
                                            other.lon,
                                            other.alt)
        else:
            raise TypeError

    def within_arrive_range(self, other):
        """
        :param other:
        :return:
        """
        if type(other) is AerialPosition:
            return settings.GOTO_PRECISION > self.distance_to(other)
        elif type(other) is dronekit.LocationGlobalRelative:
            return settings.GOTO_PRECISION > coordinate_to_coordinate(
                self.gps_position.latitude, self.gps_position.longitude, self.relative_altitude,
                other.lat,
                other.lon,
                other.alt)
        else:
            raise TypeError

    def duplicate(self, other):
        """

        :param other:
        :return:
        """
        return self.relative_altitude == other.relative_altitude and self.gps_position.duplicated(other.gps_position)
