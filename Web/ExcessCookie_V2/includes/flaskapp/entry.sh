#!/bin/bash

until nc -z -v -w30 $DB_HOST $DB_PORT
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

python3 seeding.py

gunicorn -w 2 --bind 0.0.0.0:5000 flaskapp:app --access-logfile -