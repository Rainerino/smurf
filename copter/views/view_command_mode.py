from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from rest_framework.response import Response

from copter.serializers.drone import DroneCommandSerializer
from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus
from rest_framework import generics


class DroneCommandListCreate(generics.RetrieveUpdateAPIView):
	"""
		202: accepted and processed
		400: Bad input configuration
		500: internel server error, most of the time indicate a connection problem
		501: method not implemented, usually means you have reached a branch that is not
			supposed to be reached
	"""
	queryset = DroneCommand.objects.all()
	serializer_class = DroneCommandSerializer

	def put(self, request, *args, **kwargs):
		serializer = DroneCommandSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

		# If the attempt connect bit is triggered
		if serializer.validated_data.get('is_attempt_connect'):
			# save the attempt connect bit to Database call connect_to_vehicle
			connection_port = serializer.validated_data.get("connection_port")
			copter = DroneCommand.objects.get(pk=1)
			copter.is_attempt_connect = True
			copter.save()

			return_code = copter.connect_to_vehicle(connection_port=connection_port)

			if return_code is 0:
				# 202
				return Response(serializer.data, status=202)
			elif return_code is 1:
				# 400
				return HttpResponseBadRequest("Bad inputs")
			elif return_code is 2:
				# 500
				return HttpResponseServerError("Connection to the copter failed")
			else:
				# 501
				return Response(serializer.data, status=501)

		elif serializer.validated_data.get('is_attempt_arm'):
			# check if the copter trying to arm. This will supress the following signals
			copter = DroneCommand.objects.get(pk=1)
			copter.is_attempt_arm = True
			copter.is_attempt_disarm = False
			copter.save()
			result = copter.arm_vehicle()
			if result == 0:
				return Response(serializer.data, status=202)
			elif result == 1:
				return HttpResponseBadRequest("Check input data and configuration for arming")
			elif result == 2:
				return HttpResponseServerError("Arming failed!")
			else:
				return Response(serializer.data, status=501)

		elif serializer.validated_data.get('is_attempt_disarm'):
			pass
		elif serializer.validated_data.get('is_attempt_disconnect'):
			pass
		else:
			# if not connected, we should just save the data and do nothing.
			# the data will be suppressed
			return Response(serializer.data, status=501)
