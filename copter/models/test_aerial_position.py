# coding=utf-8
"""Tests for the aerial_position module."""
import dronekit
from copter.models.aerial_position import AerialPosition
from copter.models.gps_position import GpsPosition
from django.test import TestCase
from django.conf import settings


class TestAerialPositionModel(TestCase):
    """Tests the AerialPosition model."""

    def assertDistanceEqual(self, pos1, pos2, dist):
        """AerialPosition distances are within threshold (ft)."""
        self.assertAlmostEqual(pos1.distance_to(pos2), dist, delta=settings.GOTO_PRECISION)
        self.assertAlmostEqual(pos2.distance_to(pos1), dist, delta=settings.GOTO_PRECISION)

    def evaluate_distance_inputs(self, io_list):
        """Evaluates the distance_to calc with the given input list."""
        for (lat1, lon1, alt1, lat2, lon2, alt2, dist_actual) in io_list:
            gps1 = GpsPosition(latitude=lat1, longitude=lon1)
            gps1.save()

            gps2 = GpsPosition(latitude=lat2, longitude=lon2)
            gps2.save()

            pos1 = AerialPosition(gps_position=gps1, relative_altitude=alt1)
            pos2 = AerialPosition(gps_position=gps2, relative_altitude=alt2)

            self.assertDistanceEqual(pos1, pos2, dist_actual)

    def test_distance_to_vehicle(self):
        """Test using vehicle location object instead of aerial position"""
        gps1 = GpsPosition(latitude=38.145306, longitude=-76.428709)
        gps1.save()
        gps2 = GpsPosition(latitude=38.145305, longitude=-76.428759)
        gps2.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)

        location1 = dronekit.LocationGlobalRelative(38.145306, -76.428709, 0)
        location2 = dronekit.LocationGlobalRelative(38.145305, -76.428759, 4)

        distance = pos1.distance_to(location2)
        self.assertAlmostEqual(distance, 5.9, delta=1)
        distance = pos2.distance_to(location2)
        self.assertAlmostEqual(distance, 4, delta=0.5)
        distance = pos1.distance_to(location1)
        self.assertAlmostEqual(distance, 0, delta=0.5)

    def test_distance_zero(self):
        """Tests distance calc for same position."""
        self.evaluate_distance_inputs([
            # (lat1, lon1, alt1, lat2, lon2, alt2, dist_actual)
            (0, 0, 0, 0, 0, 0, 0),
            (1, 2, 3, 1, 2, 3, 0),
            (-30, 30, 100, -30, 30, 100, 0),
        ])  # yapf: disable

    def test_distance_competition_amounts(self):
        """Tests distance calc for competition amounts."""
        self.evaluate_distance_inputs([
            # (lat1,     lon1,      alt1, lat2,       lon2,      alt2, dist_actual)
            (38.145306, -76.428709, 0, 38.146146, -76.426375, 0, 224.46),
            (38.145399, -76.428537, 0, 38.144686, -76.427818, 100, 142.27),
            (38.142471, -76.434261, 100, 38.147838, -76.418876, 800, 1629.96),
            (49.259203, -123.242116, 0, 49.258979, -123.239620, 0, 182.8)

        ])  # yapf: disable

    def test_duplicate_unequal(self):
        """Tests the duplicate function with unequal positions."""
        gps1 = GpsPosition(latitude=0, longitude=0)
        gps1.save()
        gps2 = GpsPosition(latitude=1, longitude=1)
        gps2.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)
        pos3 = AerialPosition(gps_position=gps1, relative_altitude=1)

        self.assertFalse(pos1.duplicate(pos2))
        self.assertFalse(pos1.duplicate(pos3))

    def test_duplicate_equal(self):
        """Tests the duplicate function with equal positions."""
        gps1 = GpsPosition(latitude=0, longitude=0)
        gps1.save()
        gps2 = GpsPosition(latitude=0, longitude=0)
        gps2.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)
        pos3 = AerialPosition(gps_position=gps1, relative_altitude=0)

        self.assertTrue(pos1.duplicate(pos2))
        self.assertTrue(pos1.duplicate(pos3))

    def test_not_within_arrive_range(self):
        """Reference: https://www.movable-type.co.uk/scripts/latlong.html"""
        """Test within range function with within range positions"""
        gps1 = GpsPosition(latitude=38.145306, longitude=-76.428709)
        gps1.save()
        gps2 = GpsPosition(latitude=38.145305, longitude=-76.428759)
        gps2.save()
        gps3 = GpsPosition(latitude=38.145305, longitude=-76.428799)
        gps3.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)
        pos3 = AerialPosition(gps_position=gps3, relative_altitude=0)
        pos4 = AerialPosition(gps_position=gps2, relative_altitude=4)

        self.assertFalse(pos1.within_arrive_range(pos2))
        self.assertFalse(pos2.within_arrive_range(pos1))
        self.assertFalse(pos1.within_arrive_range(pos3))
        self.assertFalse(pos1.within_arrive_range(pos4))
        self.assertFalse(pos2.within_arrive_range(pos4))

    def test_within_arrive_range(self):
        """Test within range function with not within rnage positions"""
        gps1 = GpsPosition(latitude=49.259203, longitude=-123.242116)
        gps1.save()
        gps2 = GpsPosition(latitude=49.259205, longitude=-123.242116)
        gps2.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)
        pos3 = AerialPosition(gps_position=gps1, relative_altitude=0.5)

        self.assertTrue(pos1.within_arrive_range(pos2))
        self.assertTrue(pos2.within_arrive_range(pos1))
        self.assertTrue(pos1.within_arrive_range(pos3))

    def test_within_arrive_range_vehicle(self):
        """Test within range with vehicle objects"""
        location1 = dronekit.LocationGlobalRelative(49.259203, -123.242116, 0)
        location2 = dronekit.LocationGlobalRelative(49.259205, -123.242116, 0)
        location3 = dronekit.LocationGlobalRelative(49.259205, -123.242116, 0.8)

        gps1 = GpsPosition(latitude=49.259203, longitude=-123.242116)
        gps1.save()
        gps2 = GpsPosition(latitude=49.259205, longitude=-123.242116)
        gps2.save()

        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        pos2 = AerialPosition(gps_position=gps2, relative_altitude=0)

        # TODO use better points to test
        self.assertTrue(pos1.within_arrive_range(location1))
        self.assertTrue(pos1.within_arrive_range(location2))
        self.assertTrue(pos1.within_arrive_range(location3))
        self.assertTrue(pos2.within_arrive_range(location1))

    def test_type_error(self):
        """Test distance in using wrong object"""
        gps1 = GpsPosition(latitude=38.145306, longitude=-76.428709)
        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)

        with self.assertRaises(TypeError):
            pos1.distance_to(gps1)

    def test_within_arrive_range_type_error(self):
        """Test within range functions using wrong objects"""
        gps1 = GpsPosition(latitude=38.145306, longitude=-76.428709)
        pos1 = AerialPosition(gps_position=gps1, relative_altitude=0)
        with self.assertRaises(TypeError):
            pos1.within_arrive_range(gps1)
