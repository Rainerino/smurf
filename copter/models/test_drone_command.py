from django.core.management import call_command
from django.test import TestCase
from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus

class TestDroneCommand(TestCase):

	def setUp(self):
		call_command('loaddata', 'copter_test')
		pass

	def test_str(self):
		DroneCommand.objects.get(pk=1).__str__()

	def test_connect_to_vehicle_success(self):
		"""
		test precondition
		test good port and baud to connect, if true is returned
		test bad port
		test bad attempt signals
		:return:
		"""
		cmd_obj = DroneCommand.objects.get(pk=1)
		cmd_obj.is_attempt_connect = True
		cmd_obj.save()
		connection_port = "tcp:127.0.0.1:5760"
		result = DroneCommand.objects.get(pk=1).connect_to_vehicle(connection_port=connection_port)

		self.assertEqual(result, 0)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_armed)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_arming)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, connection_port)

	def test_connect_to_vehicle_fail(self):
		pass

	def test_arm_vehicle(self):
		pass

	def sim_test_disarm_vehicle(self):
		pass
