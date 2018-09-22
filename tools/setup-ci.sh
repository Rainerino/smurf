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

echo "Checking submodules..."
cd "${CWD}"

git submodule update --init --recursive
echo "Submodules updated"


# Install dependences
echo "Checking Python dependencies..."
pipenv install --dev --skip-lock
pipenv install --skip-lock

# Start postgres and check user/database
service postgresql start

apt install python-dev libpq-dev postgresql-9.5 postgresql-contrib -y

if ! sudo -u postgres psql remote -c ''; then
    sudo -u postgres psql -c "CREATE DATABASE remote;"
fi
if ! sudo -u postgres psql -t -c '\du' | cut -d \| -f 1 | grep -qw remote; then
    sudo -u postgres psql -c "CREATE USER drone WITH PASSWORD 'ubcuas';"

    sudo -u postgres psql -c "ALTER ROLE drone SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE drone SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE drone SET timezone TO 'UTC';"
    sudo -u postgres psql -c 'ALTER USER drone CREATEDB;'

    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE remote TO drone;"
fi


echo "Checking migrations..."
yes | sudo -u "${USER}" pipenv run python ../manage.py makemigrations
sudo -u "${USER}" pipenv run python ../manage.py migrate


# Load database with some data
echo "Loading database..."
sudo -u "${USER}" pipenv run python manage.py loaddata "${CWD}"/mavlink/fixtures/mavlinks.json


