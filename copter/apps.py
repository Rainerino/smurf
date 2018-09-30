# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CopterConfig(AppConfig):
    name = 'copter'

class Settings:
    ENGINE_DEBUG = 1
    TIMEOUT = 30
    HEARTBEAT_TIMEOUT = 10