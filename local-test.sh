#!/bin/bash

set -a
source .env.graphnet
set +a

python ./manage.py migrate

python ./manage.py createsuperuser --noinput

python ./manage.py ensure_admins
python ./manage.py collectstatic --no-input

python ./manage.py runserver localhost:8000
