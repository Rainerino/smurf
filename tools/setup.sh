#!/usr/bin/env bash



echo "Checking migrations..."
yes | sudo -u "${USER}" pipenv run python ../manage.py makemigrations
sudo -u "${USER}" pipenv run python ../manage.py migrate


