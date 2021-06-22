#!/bin/sh

echo "Waiting for MySQL..."

while ! mysqladmin ping -h "$DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

while ! mysqladmin ping -h "$TEST_DATABASE_HOST" --silent > /dev/null 2> /dev/null; do
    sleep 1
done

echo "MySQL started"

cd /opt/app || exit

if [ -f "/opt/app/deploy/backend/.cache/.epitator.sqlitedb" ]; then
  cp /opt/app/deploy/backend/.cache/.epitator.sqlitedb /root/
elif [ ! -f "/root/.epitator.sqlitedb" ]; then
  # this doesn't work if you put it in the Dockerfile but
  # it takes ages so we only want to do it once
  echo "Importing epitator"
  python -m epitator.importers.import_all
  cp /root/.epitator.sqlitedb /opt/app/deploy/backend/.cache/.epitator.sqlitedb
fi

if [ -f "annette/.credentials/gmail-credentials.json" ]; then
  python setup.py develop
  #jupyter notebook --ip=0.0.0.0 --allow-root --no-browser &&
  python -m annette.src.runme
else
  echo "Now run:\n\tdocker run -it annette_backend python /opt/app/deploy/backend/scripts/auth.py --noauth_local_webserver"
fi
