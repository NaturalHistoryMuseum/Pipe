#!/bin/sh

echo "Waiting for MySQL..."

while ! mysqladmin ping -h "$TEST_DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

echo "MySQL started"

cd /opt/app || exit

python -m pytest --cov=annette tests/
