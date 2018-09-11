from django.db import models


class MavlinkConnect(models.Model):
    """

    """
    connected = models.BooleanField(default=False)

    connection_baud_rate = models.IntegerField(default=115200)

    attempt_connect = models.BooleanField(default=False)

    connection_port = models.TextField(default="tcp:127.0.0.1:5760")

    connection_status_message = models.TextField(default="Not connected")

    def __str__(self):
        return "Attempt: %s Connected %s, port: %s baud: %s " % \
               (self.attempt_connect, self.connected, self.connection_port, self.connection_baud_rate)
