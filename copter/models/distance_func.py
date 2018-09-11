# coding=utf-8
import math
from geopy.distance import great_circle


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
    gps_dist_m = gps_coordinate_distance(latitude_1, longitude_1, latitude_2, longitude_2)
    alt_dist_m = abs(altitude_2 - altitude_1)
    return math.hypot(gps_dist_m, alt_dist_m)
