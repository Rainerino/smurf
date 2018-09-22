#!/bin/bash

set -e

# Make sure script is run as root
if [ "${EUID}" -ne 0 ]; then
    echo "Error: Please run with root."
    exit 1
fi

# Check programs are installed
if [ ! -x "$(command -v git)" ]; then
    echo "Git is not installed. Installing..."
    apt install git -qq -y
    echo "Git installed"
fi
if [ ! -x "$(command -v python3.6)" ]; then
    echo "Python 3.6 is not installed. Installing..."
    apt install python3.6 -qq -y
    echo "Python 3.6 installed"
fi
if [ ! -x "$(command -v pip3)" ]; then
    echo "Python3-pip is not installed. Installing..."
    apt install python3-pip -qq -y
    echo "Python3-pip installed"
fi
if [ ! -x "$(command -v pipenv)" ]; then
    echo "Pipenv is not installed. Installing..."
    pip3 install pipenv
    echo "Pipenv installed"
fi
if [ ! -x "$(command -v npm)" ]; then
    echo "npm not installed. Installing..."
    apt install curl software-properties-common -qq -y
    curl -sL https://deb.nodesource.com/setup_8.x | bash -
    apt install nodejs -qq -y
    echo "Nodejs installed"
fi
apt install python-dev libpq-dev postgresql postgresql-contrib -qq -y

# Get root directory of project
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && cd .. && pwd)"

# Start setup
echo "Checking submodules..."
cd "${CWD}"

git submodule update --init --recursive
echo "Submodules updated"

# Create settings and env file if not existent
SETTINGS_FILE="${CWD}"/Smurf/settings.py
if [ ! -f "${SETTINGS_FILE}" ]; then
    echo "Creating settings file..."
    cp "${SETTINGS_FILE}".example "${SETTINGS_FILE}"
    echo "Created "${SETTINGS_FILE}""
fi


# Install dependences
echo "Checking Python dependencies..."
pipenv install --dev --3.6
pipenv install
echo "Checking JavaScript dependencies..."
npm install

# Start postgres and check user/database
service postgresql start
"${CWD}"/tools/setup_db.sh

# Make migrations if necessary
echo "Checking migrations..."
yes | pipenv run python manage.py makemigrations --merge
pipenv run python manage.py migrate

# Load database with some data
echo "Loading database..."
pipenv run python manage.py loaddata "${CWD}"/mavlink/fixtures/mavlinks.json

# Create symlink for gcom-run use
#GCOM_RUN_BIN=/usr/local/bin/gcom-run
#
#echo "Creating symlink for gcom-run..."
#if [ -h "${GCOM_RUN_BIN}" ]; then
#    echo "Symlink already exists, replacing..."
#    rm "${GCOM_RUN_BIN}"
#fi
#
#ln -s "${PWD}"/tools/gcom-run.sh "${GCOM_RUN_BIN}"
#echo "Created symlink in "${GCOM_RUN_BIN}" for "${PWD}"/tools/gcom-run.sh"

# Generate staticfiles/mediafiles directories
