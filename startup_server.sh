#!/bin/bash

ENVIRONMENT=${1:-local}

### WAITING FOR POSTGRES START ###
until /usr/bin/pg_isready -h postgres -U postgres
do
  sleep .5;
done
python3 ./manage.py collectstatic --no-input --settings=edlight.settings.$ENVIRONMENT
python3 ./manage.py runserver 0.0.0.0:8000 --settings=edlight.settings.$ENVIRONMENT

