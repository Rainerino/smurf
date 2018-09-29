from django.db import models
from preconditions import preconditions


class DroneCommand(models.Model):
	"""
	These are the variables for controlling drone, abstract manual copter control
	Command data can be read and write
	"""

	# this is connected to a connection button on the GUI
	is_attempt_connect = models.BooleanField(default=False)

	# this is connected to a disconnection button on the GUI
	is_attempt_disconnect = models.BooleanField(default=False)

	#
	is_attempt_arm = models.BooleanField(default=False)
	is_attempt_disarm = models.BooleanField(default=True)

	connection_port = models.TextField(default="tcp:127.0.0.1:5760")
	connection_baud_rate = models.IntegerField(default=115200)

	# current_mission = mission blah
	def __str__(self):
		return "Vehicle at connection_port"

	@preconditions(lambda self: self.is_attempt_connect)
	def connect_to_vehicle(self):
		"""This function will connect to a physical drone
			precondition:
			is_attempt_connect is set to True


		"""


	def arm_vehicle(self):
		""""Arm vehicle function"""
		pass

	def disarm_vehicle(self):
		""""Disarm vehivle function"""
		pass

	def disconnect_from_vehicle(self):
		"""This function will disconnect from a connected vehicle"""
		pass
