#!/usr/bin/env bash

if ! sudo -u postgres psql remote -c ''; then
    sudo -u postgres psql -c "CREATE DATABASE remote;"
fi
if ! sudo -u postgres psql -t -c '\du' | cut -d \| -f 1 | grep -qw drone; then
    sudo -u postgres psql -c "CREATE USER drone WITH PASSWORD 'ubcuas';"

    sudo -u postgres psql -c "ALTER ROLE drone SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE drone SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE drone SET timezone TO 'UTC';"
    sudo -u postgres psql -c 'ALTER USER drone CREATEDB;'

    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE remote TO drone;"
fi
