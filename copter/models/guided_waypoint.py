from django.db import models

from copter.models.aerial_position import AerialPosition
from preconditions import preconditions


class GuidedWaypoint(models.Model):
	is_guided_running = models.BooleanField(default=False)
	is_attempt_guided = models.BooleanField(default=False)
	current_guided_waypoint = models.ForeignKey(AerialPosition, on_delete=models.CASCADE,
	                                            related_name="guided_waypoint")
	guided_status_message = models.TextField(default="No message")

	def __str__(self):
		pass

	def arrived_at_current_waypoint(self):
		"""check if copter has arrived at the assigned waypoint"""
		pass

	@preconditions(lambda destination: GuidedWaypoint.objects.get(pk=1).is_attempt_guided and isinstance(destination, AerialPosition))
	def guided_go_to_waypoint(self, destination):
		"""go to the point assigned"""
		pass
