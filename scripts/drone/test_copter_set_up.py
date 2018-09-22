# coding=utf-8
import dronekit_sitl
from django.test import TestCase

from copter.models.connection import MavlinkConnect
from copter.models.models import *
from copter.models.guided_waypoint import MavlinkGoTo
from copter.models.mission import MavlinkMission
from copter.models.aerial_position import AerialPosition
from copter.models.gps_position import GpsPosition

from django.core.management import call_command

from scripts.drone.copter import Copter
import preconditions
from scripts.drone.copter_error import *

from scripts.drone.message import Messages


class TestCopterSetupFunction(TestCase):
    """Test cases for copter setting up functions
    1. received connect signal
    2. connect to drone
    3. arm check
    4. home location check
    """

    def setUp(self):
        """First populate the database"""
        call_command('loaddata', 'mavlinks')

    def test_attempt_connect(self):
        pass

        # self.attempt_connect_success()
        # self.attempt_connect_port_fail()
        # self.attempt_connect_baud_fail()


    def test_attempt_connect_success(self):
        """Test If the drone can be connected under the correct configurations"""
        connect = MavlinkConnect.objects.get(pk=1)
        # # this works, we can only have one sitl running, so make this count

        drone = Copter()

        connect.connection_port = "127.0.0.1:14550"
        connect.connection_baud_rate = 115200
        connect.attempt_connect = True
        connect.save()

        drone.received_connect_signal()

        # IMPORTANT! need to fetch the instance again, beacuase each instance is different?
        connect = MavlinkConnect.objects.get(pk=1)

        self.assertTrue(connect.connected)
        self.assertFalse(connect.attempt_connect)
        self.assertEqual(Messages.CONNECTED % connect.connection_port, connect.connection_status_message)
        drone.vehicle.close()

    def test_attempt_connect_port_fail(self):
        """Use wrong port and catch General exceptions"""
        drone = Copter()
        m = MavlinkConnect.objects.get(pk=1)
        m.connection_port = 'Whatever port'
        m.attempt_connect = True
        m.save()
        # if the connection failed, it's a weird error
        with self.assertRaises(Exception):
            drone.received_connect_signal()

        m = MavlinkConnect.objects.get(pk=1)
        self.assertEqual(m.connection_status_message, Messages.FAILED_CONNECTION % m.connection_port)

        if drone.vehicle is not None:
            drone.vehicle.close()

    def test_attempt_connect_baud_fail(self):
        """Use wrong port and catch General exceptions"""
        drone = Copter()
        m = MavlinkConnect.objects.get(pk=1)
        m.connection_port = 'tcp:127.0.0.1:5760'
        m.connection_baud_rate = 100
        m.attempt_connect = True
        m.save()
        # IT should time out
        with self.assertRaises(CopterConnectTimeoutError):
            drone.received_connect_signal()

        m = MavlinkConnect.objects.get(pk=1)

        self.assertFalse(m.connected)

        self.assertFalse(m.attempt_connect)

        self.assertEqual(m.connection_status_message, Messages.FAILED_CONNECTION % m.connection_port)

        if drone.vehicle is not None:
            drone.vehicle.close()

    def test_connect_to_drone_pass(self):
        # use multiple thread to test this...
        pass

