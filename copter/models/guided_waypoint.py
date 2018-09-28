from django.db import models

from copter.models.aerial_position import AerialPosition


class GuidedWaypoint(models.Model):
	is_guided_running = models.BooleanField(default=False)
	is_attempt_guided = models.BooleanField(default=False)
	current_guided_waypoint = models.ForeignKey(AerialPosition, on_delete=models.CASCADE,related_name="guided_waypoint")
	guided_status_message = models.TextField(default="No message")
