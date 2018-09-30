from django.core.management import call_command
from django.test import TestCase
from copter.models.drone_command import DroneCommand


class TestDroneCommand(TestCase):

	def setUp(self):
		call_command('loaddata', 'copter_test')
		pass

	def test_str(self):
		DroneCommand.objects.get(pk=1).__str__()

	def test_connect_to_vehicle(self):
		"""
		test precondition
		test good port and baud to connect, if true is returned
		test bad port
		test bad baud
		test bad attempt signals
		:return:
		"""
		cmd_obj = DroneCommand.objects.get(pk=1)
		cmd_obj.is_attempt_connect = True
		cmd_obj.save()

		result = DroneCommand.objects.get(pk=1).connect_to_vehicle()

		self.assertFalse(result)

	def test_arm_vehicle(self):
		pass

	def test_disarm_vehicle(self):
		pass
