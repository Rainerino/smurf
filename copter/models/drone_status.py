import traceback

from django.db import models
from copter.models.aerial_position import AerialPosition
from dronekit import Vehicle


class DroneStatus(models.Model):
	# TODO: check interop client!
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

	def get_data_as_dict(self):
		return self.__dict__

	def refresh_status(self, new_data_dict):
		"""Refresh all the status data
			Precondition: all the inputs are valid in the dictionary. Not all inputs has to be covered, but
						the naming convention should be the same.
			Postcondition: the database should be refreshed
		 Args:
		 	new_data_dict: the dictionary of the status. It should be key and value paired

		Return:
			bool refresh success or not
		 """
		try:
			for key, value in new_data_dict.items():
				if key in self.get_data_as_dict() and isinstance(value, type(self.get_data_as_dict()[key])):
					self.get_data_as_dict()[key] = value
					self.save()

			return True

		except Exception as e:
			traceback.print_tb(e.__traceback__)
			return False

	def get_vehicle(self):
		"""Return the dronekit.vehicle object, which is frequently used

		Return:
			dronekit.vehicle object that is valid.
			None is it doesn't exist or if it's invalid

		"""

		# check if the vehicle is valid

		if self.check_connection():
			return DroneStatus.objects.get(pk=1).vehicle
		else:
			return None

	def check_connection(self):
		"""This function will check if the drone is connected to the physical vehicle or not

		Return:
			bool to indicate if the connection is valid or not

		"""
		return False
