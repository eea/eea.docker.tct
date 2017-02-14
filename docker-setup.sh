#!/bin/bash

args=("$@")

case $1 in
    manage)
        exec python manage.py ${args[@]:1}
        ;;
    run)
        exec gunicorn nbsap.wsgi:application \
            --name nbsap_it \
            --bind 0.0.0.0:8000 \
            --workers 3 \
            --access-logfile - \
            --error-logfile -
        ;;
    *)
esac