from django.db import models
from copter.models.aerial_position import AerialPosition
from dronekit import Vehicle


class DroneStatus(models.Model):
	"""
	These are the states of the copter, read only
	"""
	is_armed = models.BooleanField(default=False)
	is_arming = models.BooleanField(default=False)
	is_connected = models.BooleanField(default=False)
	is_connecting = models.BooleanField(default=False)

	arm_status_message = models.TextField(default="")
	connection_status_message = models.TextField(default="")

	"""
	Read only telemetry data
	"""

	current_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="current_location")

	home_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="home_location")

	velocity = models.TextField(default="")
	# this is the gps message data
	gps = models.TextField(default="")
	groundspeed = models.TextField(default="")
	airspeed = models.TextField(default="")
	ekf_ok = models.TextField(default="")
	battery = models.TextField(default="")
	last_heartbeat = models.TextField(default="")
	heading = models.TextField(default="")
	mode = models.TextField(default="")
	armed = models.TextField(default="")
	system_status = models.TextField(default="")

	# this is a unique dronekit object
	vehicle = Vehicle

	def __str__(self):
		pass

	def refresh_status(self, new_data_dict):
		"""Refresh all the status data """
		pass

	def get_vehicle(self):
		"""Return the dronekit.vehicle object, which is frequently used"""
		# check if the vehicle is valid
		if self.check_connection():
			return DroneStatus.objects.get(pk=1).vehicle
		else:
			return None

	def check_connection(self):
		"""This function will check if the drone is connected to the physical vehicle or not"""
		pass





