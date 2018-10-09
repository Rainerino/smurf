from copter.models.aerial_position import AerialPosition
from rest_framework import serializers

from copter.models.gps_position import GpsPosition
from copter.models.waypoint import Waypoint
from copter.models.flight_mission import FlightMission

class AerailPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = AerialPosition
		fields = '__all__'


class WaypointSerializer(serializers.ModelSerializer):
	class Meta:
		model = Waypoint
		fields = '__all__'


class GpsPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = GpsPosition
		fields = '__all__'



class FlightMissionSerializer(serializers.ModelSerializer):
	guided_waypoint_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Waypoint.objects.all(), required=False)

	class Meta:
		model = FlightMission
		fields = '__all__'
