#!/usr/bin/env bash
# install the python environement
pipenv install --dev

# set up the database if it's not set up.
./setup_db.sh