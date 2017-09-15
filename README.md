Target Cross Linking Tool (TCT)
===============================

The project name is Target Cross Linking Tool, a platform for organizing the implementation of a country's national biodiversity strategy after AICHI (and by case after EU Strategy).

It consists of two panels each corresponding an operation: viewing and editing.
The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its own strategy in terms of objectives and actions) and its implementation.

The second panel(Admin), authentication-available only, allows an user to actually define the national strategy. (e.g. add/modify/delete an objective, action or even elements from AICHI) in the purpose of building it.

[![Travis](https://travis-ci.org/eea/eea.docker.tct.svg?branch=master)](https://travis-ci.org/eea/eea.docker.tct)
[![Coverage](https://coveralls.io/repos/github/eea/eea.docker.tct/badge.svg?branch=master)](https://coveralls.io/github/eea/eea.docker.tct?branch=master)
[![Docker]( https://dockerbuildbadges.quelltext.eu/status.svg?organization=eeacms&repository=tct-biodiversity)](https://hub.docker.com/r/eeacms/tct-biodiversity/builds)


### Prerequisites

* Install [Docker](https://docs.docker.com/engine/installation/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

### Installing the application

1. Get the source code:

        $ git clone https://github.com/eea/eea.docker.tct
        $ cd eea.docker.tct

2. Customize env files:

        $ cp docker/postgres.env.example docker/postgres.env
        $ vim docker/postgres.env
        $ cp docker/demo.env.example docker/demo.env
        $ vim docker/demo.env
        $ cp docker/init.sql.example docker/init.sql
        $ vim docker/init.sql

3. Start application stack:

        $ docker-compose up -d
        $ docker-compose logs

4. Create a superuser:

        $ docker exec -it tct.app sh
        $ ./manage.py createsuperuser

5. Run tests:

        $ docker exec -it tct.app sh
        # apk add --no-cache libxslt-dev libffi-dev
        # pip install -r requirements-dev.txt
        $ ./manage.py test

6. See it in action: [http://localhost:8000](http://localhost:8000)

### Upgrading the application

1. Get the latest version of source code:

        $ cd eea.docker.tct
        $ git pull origin master

2. Update the application stack, all services should be "Up":

        $ docker-compose up -d
        $ docker-compose ps

3. See it in action: [http://localhost:8000](http://localhost:8000)

### Development instructions
* Start stack, all services should be "Up" :

        $ docker-compose up -d
        $ docker-compose ps

* Check application logs:

        $ docker-compose logs

* When the image is modified you should update the stack:

        $ docker-compose up -d --build

* Cleanup containers, images and volumes:

        $ docker-compose down -v
        $ docker rm $(docker ps -aq)
        $ docker rmi $(docker images -q)
        $ docker volume rm $(docker volume ls -q)

### Debugging

* Please make sure that `DEBUG=True` in `settings.py`

* Update docker-compose `app` section with the following so that `docker-entrypoint.sh`
is not executed:

        entrypoint: ["/usr/bin/tail", "-f", "/dev/null"]

* Attach to docker container and start the server in debug mode:

        $ docker exec -it tct.app sh
        # gunicorn tct.wsgi:application \
            --name tct \
            --bind 0.0.0.0:80 \
            --workers 3 \
            --access-logfile - \
            --error-logfile -

* See it in action: [http://localhost:8000](http://localhost:8000)

### LDAP integration

Set *ALLOWED_USERS* in settings to restrict access to a specific set of usernames.

Set AUTH_LDAP_SERVER_URI and AUTH_LDAP_USER_DN_TEMPLATE from settings.py for LDAP
Authentication configuration. Add 'django_auth_ldap.backend.LDAPBackend' value in 
AUTHENTICATION_BACKENDS.


### Translations

1. Manual translation.

* Run over the entire source tree and pull out all strings marked for translation,
add/edit/delete translations for each file in tct/locale/[LANGUAGE]/LC_MESSAGE/django.po,
compile the po files and restart the server:

        $ docker exec -it tct.app sh
        # cd tct
        # django-admin.py makemessages -a
        # django-admin.py compilemessages
        $ docker-compose restart demo

2. Automatic translation

* Translate the messages using the Rosetta tool for translation
(http://localhost:8000/translate) and restart the server when ready:

        $ docker-compose restart app
