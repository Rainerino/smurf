from django.core.management import call_command
from django.test import TestCase
from copter.models.drone_status import DroneStatus


class TestDroneStatus(TestCase):
	def setUp(self):
		call_command('loaddata', 'copter_test')

	def test_str(self):
		"""
		Test the str function
		"""
		return DroneStatus.objects.get(pk=1).__str__()

	def test_refresh_status(self):
		"""
		Test the refresh status

		use dict to modify 1 of them
		use dict to modify 3 of them

		reject dictionary
		"""
		copter = DroneStatus.objects.get(pk=1)

		test_dict = {
			"is_armed": True
		}
		result = copter.refresh_status(test_dict)

		self.assertTrue(result)
		self.assertEqual(DroneStatus.objects.get(pk=1).is_armed, test_dict.get("is_armed"))

		test_dict = {
			"is_armed": False,
			"is_arming": True
		}
		result = copter.refresh_status(test_dict)

		self.assertEqual(DroneStatus.objects.get(pk=1).is_armed, test_dict.get("is_armed"))
		self.assertEqual(DroneStatus.objects.get(pk=1).is_arming, test_dict.get("is_arming"))
		self.assertTrue(result)

		test_dict = {
			"current_location": 1
		}
		copter.refresh_status(test_dict)

		self.assertEqual(DroneStatus.objects.get(pk=1).current_location_id, test_dict.get("current_location"))

		test_dict = {
			"is_armed": True,
			"whatever is this": "What"
		}
		copter.refresh_status(test_dict)

		self.assertEqual(DroneStatus.objects.get(pk=1).is_armed, test_dict.get("is_armed"))

		test_dict = {
			"is_armed": "No this is not right",
		}
		copter.refresh_status(test_dict)

		self.assertEqual(DroneStatus.objects.get(pk=1).is_armed, True)

		test_dict = {
			"is_armed": 1,
			"current_location": "True"
		}
		result = copter.refresh_status(test_dict)

		self.assertEqual(DroneStatus.objects.get(pk=1).is_armed, True)
		self.assertEqual(DroneStatus.objects.get(pk=1).current_location_id, 1)

		self.assertTrue(result)

	def test_get_vehicle(self):
		"""
		There is no vehicle, so get vehcile will return None as API suggested
		:return:
		"""
		self.assertEqual(None, DroneStatus.objects.get(pk=1).get_vehicle())

	def test_check_connection(self):
		"""
		Nothing is connected, so the check connection will fail
		:return:
		"""
		self.assertEqual(False, DroneStatus.objects.get(pk=1).check_connection())
