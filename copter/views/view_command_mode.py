from django.http import JsonResponse
from rest_framework.response import Response

from copter.serializers.drone import DroneCommandSerializer
from copter.models.drone_command import DroneCommand
from rest_framework import generics


class DroneCommandListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = DroneCommand.objects.all()
	serializer_class = DroneCommandSerializer

	def retrieve(self, request, *args, **kwargs):
		serializer = DroneCommandSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

		copter = serializer.validated_data
		# TODO more conditions
		if copter.get('is_attempt_connect'):
			DroneCommand.objects.get(pk=1).connect_to_vehicle()

		return Response(serializer.data, status=200)