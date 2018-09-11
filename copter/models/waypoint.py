from django.db import models

from copter.models.aerial_position import AerialPosition


class Waypoint(models.Model):
    """A waypoint consists of an aerial position and its order in a set.

    Attributes:
        position: Aerial position.
        order: Waypoint relative order number. Should be unique per waypoint
            set.
    """
    aerial_position = models.ForeignKey(AerialPosition, on_delete=models.CASCADE)
    order = models.IntegerField(db_index=True)
    accomplished = models.BooleanField(default=False)

    def __str__(self):
        return "order %s, arrived: %s, going to: %s" % (self.order, self.accomplished, self.aerial_position.__str__())

    def duplicate(self, other):
        """Check if the two waypoint objects are dupliated
        :param other:
        :return:
        """
        return self.aerial_position.duplicate(other.aerial_position)
