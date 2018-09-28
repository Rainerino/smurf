from django.db import models
from preconditions import preconditions


class DroneCommand(models.Model):
	"""
	These are the variables for controlling drone, abstract manual copter control
	Command data can be read and write
	"""

	is_attempt_connect = models.BooleanField(default=False)
	is_attempt_arm = models.BooleanField(default=False)
	is_attempt_disarm = models.BooleanField(default=False)

	connection_port = models.TextField(default=False)
	connection_baud_rate = models.IntegerField(default=115200)

	# current_mission = mission blah
	@preconditions(lambda is_attempt_connect: DroneCommand.objects.get(pk=1).is_attempt_connect)
	def connect_to_vehicle(self):
		"""This function will connect to a physical drone"""
		pass

	def arm_vehicle(self):
		""""Arm vehicle function"""
		pass

	def disarm_vehicle(self):
		""""Disarm vehivle function"""
		pass

	def disconnect_from_vehicle(self):
		"""This function will disconnect from a connected vehicle"""
		pass
