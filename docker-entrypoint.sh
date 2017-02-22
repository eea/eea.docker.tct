#!/bin/bash

args=("$@")

if [ -z "$MYSQL_ADDR" ]; then
  MYSQL_ADDR="mysql"
fi

while ! nc -z $MYSQL_ADDR 3306; do
  echo "Waiting for MySQL server at '$MYSQL_ADDR' to accept connections on port 3306..."
  sleep 1s
done

if ! mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD -e "use $DATABASES_NAME;"; then
  echo "CREATE DATABASE $DATABASES_NAME"
  mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE $DATABASES_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
  mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE USER '$DATABASES_USER'@'%' IDENTIFIED BY '$DATABASES_PASSWORD';"
  mysql -h mysql -u root -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON $DATABASES_NAME.* TO '$DATABASES_USER'@'%';"
fi

python manage.py collectstatic --noinput
python manage.py migrate

case $1 in
    manage)
        exec python manage.py ${args[@]:1}
        ;;
    run)
        exec gunicorn tct.wsgi:application \
            --name tct \
            --bind 0.0.0.0:8000 \
            --workers 3 \
            --access-logfile - \
            --error-logfile -
        ;;
    *)
esac
