#!/usr/bin/env bash

# Make sure script is run as root
if [ "${EUID}" -ne 0 ]; then
    echo "Error: Please run with root."
    exit 1
fi

# Check programs are installed
if [ ! -x "$(command -v git)" ]; then
    echo "Git is not installed. Installing..."
    apt install git -y
    echo "Git installed"
fi
if [ ! -x "$(command -v python3)" ]; then
    echo "Python 3.6 is not installed. Installing..."
    apt install python3.6 python3.6-dev -y
    echo "Python 3.6 installed"
fi
if [ ! -x "$(command -v pip3)" ]; then
    echo "Python3-pip is not installed. Installing..."
    apt install python3-pip -y
    echo "Python3-pip installed"
fi
if [ ! -x "$(command -v pipenv)" ]; then
    echo "Pipenv is not installed. Installing..."
    pip3 install pipenv
    echo "Pipenv installed"
fi

# Get root directory of project
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && cd .. && pwd)"

sudo -u "${USER}" git submodule update --init --recursive
echo "Submodules updated"

# Start postgres and check user/database

"${CWD}"/tools/setup_db.sh
service postgresql start

echo "Checking migrations..."
yes | sudo -u "${USER}" pipenv run python ../manage.py makemigrations
sudo -u "${USER}" pipenv run python ../manage.py migrate


# Load database with some data
echo "Loading database..."
sudo -u "${USER}" pipenv run python manage.py loaddata "${CWD}"/mavlink/fixtures/mavlinks.json


