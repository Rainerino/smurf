import math

from django.conf import settings
from django.db import models

import dronekit
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
			return self.coordinate_to_coordinate(self.gps_position.latitude, self.gps_position.longitude,
			                                     self.relative_altitude,
			                                     other.gps_position.latitude, other.gps_position.longitude,
			                                     other.relative_altitude)
		elif type(other) is dronekit.LocationGlobalRelative:
			return self.coordinate_to_coordinate(self.gps_position.latitude, self.gps_position.longitude,
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
			return settings.GOTO_PRECISION > self.coordinate_to_coordinate(
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

	@staticmethod
	def coordinate_to_coordinate(latitude_1, longitude_1, altitude_1, latitude_2, longitude_2,
	                             altitude_2):
		"""Get the distance in feet between the two positions.

		Args:
			latitude_1: The latitude of the first position.
			longitude_1: The longitude of the first position.
			altitude_1: The altitude in feet of the first position.
			latitude_2: The latitude of the second position.
			longitude_2: The longitude of the second position.
			altitude_2: The altitude in feet of the second position.
		"""
		gps_dist_m = GpsPosition.gps_coordinate_distance(latitude_1, longitude_1, latitude_2, longitude_2)
		alt_dist_m = abs(altitude_2 - altitude_1)
		return math.hypot(gps_dist_m, alt_dist_m)
