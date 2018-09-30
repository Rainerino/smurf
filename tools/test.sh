#!/usr/bin/env bash
coverage run --source='copter/models/test_drone_command.py' ./manage.py test copter --keepdb

#coverage run --source='.' manage.py test copter --keepdb

coverage html