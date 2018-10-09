from rest_framework.response import Response

from copter.serializers.drone import *
from rest_framework import generics
from copter.models.drone_status import DroneStatus


class DroneStatusListCreate(generics.RetrieveAPIView):
	"""
		200: Data is from the actual aircraft
		204: The content is not valid
		500: internel server error, most of the time indicate a connection problem
		501: method not implemented, usually means you have reached a branch that is not
			supposed to be reached
	"""

	def get(self, request, *args, **kwargs):
		status = DroneStatus.objects.get(pk=1)
		status_serializer = DroneStatusSerializer(status)
		if status.get_vehicle() is None:
			return Response(status_serializer.data, status=204)
		else:
			# send the drone data

			return Response(status_serializer.data, status=200)