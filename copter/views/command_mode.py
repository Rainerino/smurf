from copter.serializers.drone import DroneCommandSerializer
from copter.models.drone_command import DroneCommand
from rest_framework import generics


class DroneCommandListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = DroneCommand.objects.all()
	serializer_class = DroneCommandSerializer
