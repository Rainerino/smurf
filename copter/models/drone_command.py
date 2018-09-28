from django.db import models

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

