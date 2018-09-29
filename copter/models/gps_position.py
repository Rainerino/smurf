# coding=utf-8
import math

from django.db import models


from geopy.distance import great_circle


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
        return  self.gps_coordinate_distance(self.latitude, self.longitude,
                                       other.latitude, other.longitude)

    def duplicated(self, other):
        """
        Check if the gps position of the two objects are the same
        :param other:
        :return:
        """
        return (self.latitude == other.latitude and
                self.longitude == other.longitude)

    @staticmethod
    def gps_coordinate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees).

        Reference:
        https://pypi.org/project/geopy/

        https://www.movable-type.co.uk/scripts/latlong.html
        """
        p1 = (lat1, lon1)
        p2 = (lat2, lon2)
        return great_circle(p1, p2).m


