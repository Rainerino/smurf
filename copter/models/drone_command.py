import sys
import traceback

import dronekit
from django.core.management import call_command
from django.db import models
from preconditions import preconditions
from copter.models.copter_message import Messages
from copter.models.copter_error import *
from copter.apps import Settings
from copter.models.drone_status import DroneStatus


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

	# current_mission = mission blah
	def __str__(self):
		return "Vehicle at connection_port"

	@preconditions(lambda self: self.is_attempt_connect)
	def connect_to_vehicle(self):
		"""This function will connect to a physical drone
			if vehicle is already connected, the function will return false with is_attempt_connect off, and not
				modifying anything
			precondition:
			is_attempt_connect is set to True
			the physical drone that is connected to the port should be ABSOLUTELY READY TO GO
				checklist include: gps lock, armable,

			postcondition:
			is_attempt_connect is set to False
			is_attempt_disconnect is set to False
			is_attempt_arm is False
			is_attempt_disarm is False
			The vehicle object is has passed all the checks


			Args:
			Return:
				Boolean Connection result. If failed it will print an error message
		"""
		if DroneStatus.objects.get(pk=1).is_connected:
			if Settings.ENGINE_DEBUG:
				print("The copter is already connected")
			self.is_attempt_connect = False
			return False
		if Settings.ENGINE_DEBUG:
			print("starting to connect vehicle")

		connect_object = DroneStatus.objects.get(pk=1)
		connect_object.connection_status_message = Messages.INITIALIZATION
		connect_object.is_connecting = True
		connect_object.is_connected = False
		connect_object.is_armed = False
		connect_object.is_arming = False
		connect_object.save()

		no_error = True

		try:
			connection_port = self.connection_port
			connect_object.connection_status_message = Messages.CONNECTING % connection_port
			connect_object.save()

			if Settings.ENGINE_DEBUG:
				print("Connecting to %s " % connection_port)
			# for some reason the connection fails some times

			# there are some really hard requirements for this
			connect_object.vehicle = dronekit.connect(connection_port, wait_ready=True, heartbeat_timeout=10)
			connect_object.save()

		except:
			no_error = False
		finally:
			if no_error:
				# Connection is success
				connect_object.connection_status_message = Messages.CONNECTED % self.connection_port

				connect_object.is_connected = True

				connect_object.is_connecting = False

				connect_object.is_armed = False

				connect_object.is_arming = False

				connect_object.save()

				self.is_attempt_connect = False
				self.is_attempt_arm = False
				self.is_attempt_disarm = False
				self.is_attempt_disconnect = False

				self.save()

				if Settings.ENGINE_DEBUG:
					print("Connected to %s " % self.connection_port)

				return True
			else:
				connect_object.is_connecting = False

				connect_object.is_connected = False

				connect_object.vehicle = None

				connect_object.connection_status_message = Messages.FAILED_CONNECTION % self.connection_port

				connect_object.save()

				self.is_attempt_connect = False
				self.is_attempt_arm = False
				self.is_attempt_disarm = False
				self.is_attempt_disconnect = False

				self.save()

				if Settings.ENGINE_DEBUG:
					print("=====================================================================")
					print("ERROR WAS HANDLED")

				return False

	@preconditions(lambda self, delay: self.is_attempt_arm and not self.is_attempt_disarm and isinstance(delay, int))
	def arm_vehicle(self, delay=0):
		""""
		Arm vehicle function

		precondition: vehicle is connected, and user is attempt arm
		postcondition: vehicle is armed

		Args:
			delay: the duration of the delay to wait before arming
		Return:
			bool indicate if arming failed or not
		"""
		pass

	def disarm_vehicle(self):
		""""Disarm vehicle function
		precondition: vehicle is connected, and user is attempt arm
		postcondition: vehicle is armed

		Args:
			delay: the duration of the delay to wait before arming
		Return:
			bool indicate if arming failed or not
		"""
		pass

	def disconnect_from_vehicle(self):
		"""This function will disconnect from a connected vehicle
		precondition: connected to a vehicle
		postcondition:


		"""
		pass
