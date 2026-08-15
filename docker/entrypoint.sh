#!/bin/sh

set -eu

echo "Starting CuraMind AI..."

python manage.py check

python manage.py migrate --noinput

python manage.py collectstatic --noinput --clear

exec "$@"