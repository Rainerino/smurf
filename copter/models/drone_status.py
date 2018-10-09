import time
import traceback

from django.db import models
from copter.models.aerial_position import AerialPosition
from dronekit import Vehicle
from django.conf import settings
from copter.models.aerial_position import AerialPosition
from copter.models.gps_position import GpsPosition

class DroneStatus(models.Model):
	# TODO: check interop client!
	"""
	These are the states of the copter, read only
	"""
	is_armed = models.BooleanField(default=False)
	is_arming = models.BooleanField(default=False)
	is_connected = models.BooleanField(default=False)
	is_connecting = models.BooleanField(default=False)
	is_armable = models.BooleanField(default=False)

	arm_status_message = models.TextField(default="")
	connection_status_message = models.TextField(default="")

	"""
	Read only telemetry data, Should mirrow AUVSI's 
	"""
	# this will always be the aerial locaiton pk= 1
	current_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="current_location")
	# this will always be the aerial locaiton pk= 2
	home_location = models.ForeignKey(AerialPosition, on_delete=models.CASCADE, related_name="home_location")
	heading = models.TextField(default="")
	last_heartbeat = models.FloatField(default=0)
	_heartbeat_lastreceived = models.FloatField(default=0)
	_heartbeat_timeout = models.BooleanField(default=True)

	vehicle = None

	# velocity = models.TextField(default="")
	# # this is the gps message data
	# gps = models.TextField(default="")
	# groundspeed = models.TextField(default="")
	# airspeed = models.TextField(default="")
	# ekf_ok = models.TextField(default="")
	# battery = models.TextField(default="")
	#
	#
	#
	# mode = models.TextField(default="")
	# armed = models.TextField(default="")
	# system_status = models.TextField(default="")

	# this is a unique dronekit object


	def __str__(self):
		pass

	def get_data_as_dict(self):
		return self.__dict__

	def refresh_current_and_home_location(self):
		"""

		:return:
		"""
		current_aerial = AerialPosition.objects.get(pk=1)
		home_aerial = AerialPosition.objects.get(pk=2)

		current_aerial.relative_altitude = self.vehicle.location.global_relative_frame.alt
		current_aerial.gps_position.longitude = self.vehicle.location.global_relative_frame.lon
		current_aerial.gps_position.latitude = self.vehicle.location.global_relative_frame.lat

		current_aerial.save()

		home_aerial.relative_altitude = self.vehicle.home_location.alt
		home_aerial.gps_position.latitude = self.vehicle.home_location.lat
		home_aerial.gps_position.longitude = self.vehicle.home_location.lon

		home_aerial.save()

	def update_status_from_vehicle(self):
		"""
		This function will update the all data:
			current_location, home_location, heading, last_heartbeart, __heartbeart_lastreceived, _headtbeat_timeout
		"""
		if self.get_vehicle():
			new_data = dict()
			new_data['heading'] = self.vehicle.heading
			new_data['last_heartbeart'] = self.vehicle.last_heartbeat
			new_data['_heartbeat_lastreceived'] = self.vehicle._heartbeat_lastreceived
			new_data['_heartbeat_timeout'] = self.vehicle._heartbeat_timeout
			self.refresh_status(new_data)
			self.refresh_current_and_home_location()
			if settings.COPTER_DEBUG:
				print("All Status Updated!")
		else:
			if settings.COPTER_DEBUG:
				print("Failed updating status: vehicle not connected")

	def refresh_status(self, new_data_dict):
		"""
		Refresh all the status data
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

	def check_home_location(self):
		"""
		This function should have been wrapped in check_connection()!
		Check the home location and see if it's valid.
		precondition:
		Returns:
			bool of if the home location is valid o not
		"""
		try:
			count = 0
			while not self.vehicle.home_location and count < settings.HOME_LOCATION_TIMEOUT:
				cmds = self.vehicle.commands
				cmds.download()
				cmds.wait_ready(timeout=5)
				if not self.vehicle.home_location:
					if settings.ENGINE_DEBUG:
						print(" Waiting for home location ...")
				time.sleep(1)
				count += 1

		except Exception as e:
			traceback.print_tb(e.__traceback__)
			raise e

		# We have a home location, so print it!

	def check_connection(self):
		"""This function will check if the drone is connected to the physical vehicle or not
			check:
			last_heartbeat
			_heartbeat_lastreceived
			_heartbeat_timeoutelse:
			return True
		precondition: home_location is received, and also vehicle is armable!
		postcondition: if the vehicle is no longer connected, all signal bits will be erased.

		Return:
			bool to indicate if the connection is valid or not

		"""

		still_connected = True

		if not self.is_connected:
			still_connected = False
		elif not self.check_home_location():
			still_connected = False
		elif not isinstance(self.vehicle.last_heartbeat, float):
			# vehicle is not initiated
			"""
			z = dronekit.Vehicle.last_heartbeat
			isinstance(z, float)
			Out[13]: False
			"""
			still_connected = False
		elif self.vehicle.last_heartbeat == self.last_heartbeat:
			# the vehicle forzed
			still_connected = False
		elif self.vehicle._heartbeat_lastreceived == self._heartbeat_lastreceived:
			still_connected = False
		elif self.vehicle._heartbeat_timeout:
			# copter disconnected, tested using simulator manual disconnect
			still_connected = False
		elif self.vehicle is None:
			still_connected = False

		# post processing
		if still_connected:
			return True
		else:
			self.is_connected = False
			self.is_armed = False
			self.is_arming = False
			self.is_connecting = False
			self.is_armable = False
			self.vehicle = None
			self.save()
			return False