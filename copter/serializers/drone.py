from copter.models.drone_command import DroneCommand
from copter.models.drone_status import DroneStatus
from rest_framework import serializers

class DroneCommandSerializer(serializers.ModelSerializer):
	class Meta:
		model = DroneCommand
		fields = '__all__'


class DroneStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = DroneStatus
		fields = '__all__'
