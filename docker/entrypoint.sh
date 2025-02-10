#!/bin/bash

./manage.py migrate --noinput
./manage.py collectstatic --noinput
./manage.py init

exec "$@"
