from copter.serializers.drone import *
from rest_framework import generics
from copter.models.drone_status import DroneStatus


class DroneStatusListCreate(generics.RetrieveUpdateDestroyAPIView):
	queryset = DroneStatus.objects.all()
	serializer_class = DroneStatusSerializer


