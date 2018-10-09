import time

from django.core.management import call_command
from django.test import TestCase
from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus

class TestDroneCommand(TestCase):

	def setUp(self):
		call_command('loaddata', 'copter_test')
		status = DroneStatus.objects.get(pk=1)
		status.is_connected = False
		status.save()

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

	def test_arm_vehicle_result(self):
		"""
		Test the arm vecile function
		:return:
		"""
		# first connect to the vehicle
		cmd_obj = DroneCommand.objects.get(pk=1)
		cmd_obj.is_attempt_connect = True
		cmd_obj.save()
		connection_port = "tcp:127.0.0.1:5760"
		result = DroneCommand.objects.get(pk=1).connect_to_vehicle(connection_port=connection_port)
		self.assertEqual(0, result)

		copter_cmd = DroneCommand.objects.get(pk=1)
		copter_cmd.is_attempt_arm = True
		copter_cmd.save()
		result = DroneCommand.objects.get(pk=1).arm_vehicle(0)

		self.assertEqual(0, result)
		self.assertTrue(DroneStatus.objects.get(pk=1).is_armed)
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "tcp:127.0.0.1:5760")

	def test_arm_vehicle_test_delay(self):
		"""
		Arm the vehicle with delay. The time it took must be at least longer than the expeceted delay time
		Although arm check could take a while, we are not considering it.
		"""
		cmd_obj = DroneCommand.objects.get(pk=1)
		cmd_obj.is_attempt_connect = True
		cmd_obj.save()

		connection_port = "tcp:127.0.0.1:5760"
		result = DroneCommand.objects.get(pk=1).connect_to_vehicle(connection_port=connection_port)
		self.assertEqual(0, result)

		copter_cmd = DroneCommand.objects.get(pk=1)
		copter_cmd.is_attempt_arm = True
		copter_cmd.save()

		start = time .time()
		result = DroneCommand.objects.get(pk=1).arm_vehicle(5)
		end = time.time()
		self.assertTrue((end - start) >= 5)
		self.assertEqual(0, result)
		self.assertTrue(DroneStatus.objects.get(pk=1).is_armed)
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)

	def test_arm_vehicle_not_connected(self):
		"""
		Test arming when vehicle is not connected.
		"""
		copter_object = DroneStatus.objects.get(pk=1)
		copter_object.is_connected = False
		copter_object.save()
		copter_cmd = DroneCommand.objects.get(pk=1)
		copter_cmd.is_attempt_arm = True
		copter_cmd.save()

		result = DroneCommand.objects.get(pk=1).arm_vehicle(5)
		self.assertEqual(1, result)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_armed)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_arming)


	def test_disarm(self):
		pass

	def test_disconnect(self):
		pass


