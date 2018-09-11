# coding=utf-8
from django.db import models

from copter.models.distance_func import gps_coordinate_distance


class GpsPosition(models.Model):
    """GPS position consisting of a latitude and longitude degree value.
    This can be used for fly zone, drop location which represents an area or point on map

    Attributes:
        latitude: Latitude in degrees.
        longitude: Longitude in degrees.
    """
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __str__(self):
        return "pk %d with lat: %f lon: %f" % (self.pk, self.latitude, self.longitude)

    def distance_to(self, other):
        """

        :param other:
        :return:
        """
        return gps_coordinate_distance(self.latitude, self.longitude,
                                       other.latitude, other.longitude)

    def duplicated(self, other):
        """

        :param other:
        :return:
        """
        return (self.latitude == other.latitude and
                self.longitude == other.longitude)
