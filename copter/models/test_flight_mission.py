from django.core.management import call_command
from django.test import TestCase

from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus
from copter.models.flight_mission import FlightMission

class TestFlightMission(TestCase):
	def setUp(self):
		call_command('loaddata', 'copter_test')
		cmd = DroneCommand.objects.get(pk=1)
		cmd.is_attempt_connect = True
		cmd.save()
		cmd.connect_to_vehicle()

	def test_str(self):
		print(FlightMission.objects.get(pk=1).__str__())

	def test_operation_get_next_waypoint(self):
		pass

	def test_start_mission(self):
		pass

	def test_check_mission_status(self):
		pass
