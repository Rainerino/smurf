from django.http import JsonResponse
from rest_framework.response import Response

from copter.serializers.drone import DroneCommandSerializer
from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus
from rest_framework import generics

# https://www.google.ca/imgres?imgurl=https%3A%2F%2Fwww.steveschoger.com%2Fstatus-code-poster%2Fimg%2Fstatus-code.png&imgrefurl=https%3A%2F%2Fwww.steveschoger.com%2Fstatus-code-poster%2F&docid=3kGsGg01rqjQxM&tbnid=0JKfplsTmQaMIM%3A&vet=10ahUKEwiih9Dm-vDdAhUprVQKHSQTDvkQMwhFKAEwAQ..i&w=1224&h=1710&client=ubuntu&bih=904&biw=1920&q=http%20code&ved=0ahUKEwiih9Dm-vDdAhUprVQKHSQTDvkQMwhFKAEwAQ&iact=mrc&uact=8

class DroneCommandListCreate(generics.RetrieveUpdateAPIView):
	queryset = DroneCommand.objects.all()
	serializer_class = DroneCommandSerializer

	def put(self, request, *args, **kwargs):
		serializer = DroneCommandSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

		# First save everything

		if serializer.validated_data.get('is_attempt_connect'):
			print("======================")
			connection_port = serializer.validated_data.get("connection_port")
			copter = DroneCommand.objects.get(pk=1)
			copter.connection_port = connection_port
			copter.is_attempt_connect = True
			copter.save()

			copter.connect_to_vehicle()

		if DroneStatus.objects.get(pk=1).is_connected:
			print("Connected!")
			return Response(serializer.data, status=202)
		else:
			print("Failed")
			return Response(serializer.data, status=503)
