from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse

from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus

command_url = reverse('copter_command', args=[1])


class TestDroneCommandConnect(TestCase):
	def setUp(self):
		"""

		:return:
		"""
		call_command("loaddata", "copter_test")
		copter_data = DroneStatus.objects.get(pk=1)
		copter_data.is_connected = False
		copter_data.save()

	def test_connect_success_4(self):
		"""

		:return:
		"""
		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': False,
			'is_attempt_arm': True,
			'is_attempt_disarm': False,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(
			command_url, data=command_input, content_type='application/json')
		self.assertEqual(202, response.status_code)

		# check if any of the command object got overridden
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "127.0.0.1:14550")

		# check if the status objects are right
		# TOD: the whole thing should get wiped
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)

	def test_connect_success_3(self):
		"""

		:return:
		"""
		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': False,
			'is_attempt_arm': False,
			'is_attempt_disarm': True,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(command_url, data=command_input, content_type='application/json')
		self.assertEqual(202, response.status_code)
		# check if any of the command object got overridden
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "127.0.0.1:14550")
		# check if the status objects are right
		# TOD: the whole thing should get wiped
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)

	def test_connect_success_2(self):
		"""

		:return:
		"""
		# Cases 2: some other data is presented. but attempt connect is set and not connected. Could be shadows
		# if the copter is not connected, all inputs should be subpressed except the connect
		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': True,
			'is_attempt_arm': False,
			'is_attempt_disarm': False,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(
			command_url, data=command_input, content_type='application/json')
		self.assertEqual(202, response.status_code)

		# check if any of the command object got overridden
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "127.0.0.1:14550")

		# check if the status objects are right
		# TOD: the whole thing should get wiped
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)

	def test_connect_success_1(self):
		"""
		This function test if the data are correct in the cases where the
		inputs and conditions are rights
		case 1: All as expected
		case 2: ignored input data will be set
		"""
		# Case 1
		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': False,
			'is_attempt_arm': False,
			'is_attempt_disarm': False,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(
			command_url, data=command_input, content_type='application/json')
		self.assertEqual(202, response.status_code)

		# check if any of the command object got overridden
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "127.0.0.1:14550")
		# check if the status objects are right
		# TOD: the whole thing should get wiped
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)

	def test_connected_is_attempt_connect_status(self):
		"""Check the status of trigger attempt connect after already connected
			Nothing should be changed to the status
		"""
		copter_data = DroneStatus.objects.get(pk=1)
		copter_data.is_connected = True
		copter_data.save()

		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': False,
			'is_attempt_arm': False,
			'is_attempt_disarm': False,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(
			command_url, data=command_input, content_type='application/json')
		self.assertEqual(403, response.status_code)

		# check if any of the command object got overridden
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_connect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disarm)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_disconnect)
		self.assertFalse(DroneCommand.objects.get(pk=1).is_attempt_arm)
		# connection should fail, so port is not written
		self.assertEqual(DroneCommand.objects.get(pk=1).connection_port, "tcp:127.0.0.1:5760")

	def test_connected_is_attempt_connect_command(self):
		"""Check the command of trigger attempt connect after already connected
			The expected outcome is that all the command will be ignored and unchanged
		"""
		copter_data = DroneStatus.objects.get(pk=1)
		copter_data.is_connected = True
		copter_data.save()

		command_input = {
			'is_attempt_connect': True,
			'is_attempt_disconnect': True,
			'is_attempt_arm': False,
			'is_attempt_disarm': False,
			'connection_port': "127.0.0.1:14550",
		}
		response = self.client.put(
			command_url, data=command_input, content_type='application/json')
		self.assertEqual(403, response.status_code)

		# check if the status objects are right
		# TOD: the whole thing should get wiped
		self.assertTrue(DroneStatus.objects.get(pk=1).is_connected)
		self.assertFalse(DroneStatus.objects.get(pk=1).is_connecting)

	#TODO: we need to test failed connection somehow

