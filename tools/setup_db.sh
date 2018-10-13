#!/usr/bin/env bash
if ! sudo -u postgres psql gcomv2 -c ''; then
    sudo -u postgres psql -c "CREATE DATABASE gcomv2;"
fi
if ! sudo -u postgres psql -t -c '\du' | cut -d \| -f 1 | grep -qw admin; then
    sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'ubcuas';"

    sudo -u postgres psql -c "ALTER ROLE admin SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE admin SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE admin SET timezone TO 'UTC';"
    sudo -u postgres psql -c 'ALTER USER admin CREATEDB;'

    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE gcomv2 TO admin;"
fi
