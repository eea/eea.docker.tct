#!/bin/bash

args=("$@")

python manage.py collectstatic --noinput
python manage.py migrate

case $1 in
    manage)
        exec python manage.py ${args[@]:1}
        ;;
    run)
        exec gunicorn nbsap.wsgi:application \
            --name nbsap \
            --bind 0.0.0.0:8000 \
            --workers 3 \
            --access-logfile - \
            --error-logfile -
        ;;
    *)
esac
