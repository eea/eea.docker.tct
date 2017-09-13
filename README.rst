Target Cross Linking Tool (TCT)
===============================

The project name is Target Cross Linking Tool, a platform for organizing the implementation of a country's national biodiversity strategy after AICHI (and by case after EU Strategy).

It consists of two panels each corresponding an operation: viewing and editing.
The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its own strategy in terms of objectives and actions) and its implementation.

The second panel(Admin), authentication-available only, allows an user to actually define the national strategy. (e.g. add/modify/delete an objective, action or even elements from AICHI) in the purpose of building it.

.. image:: https://travis-ci.org/eea/eea.docker.tct.svg?branch=master
    :target: https://travis-ci.org/eea/eea.docker.tct 
.. image:: https://coveralls.io/repos/github/eea/eea.docker.tct/badge.svg?branch=master
    :target: https://coveralls.io/github/eea/eea.docker.tct?branch=master

Installation
------------

* Install `Docker <https://docker.com>`_
* Install `Docker Compose <https://docs.docker.com/compose>`_


Usage
-----

1. Clone the repository::

    $ git clone https://github.com/eea/eea.docker.tct
    $ cd eea.docker.tct

2. Customize env files::

    $ cp docker/postgres.env.example docker/postgres.env
    $ vim docker/postgres.env
    $ cp docker/demo.env.example docker/demo.env
    $ vim docker/demo.env
    $ cp docker/init.sql.example docker/init.sql
    $ vim docker/init.sql

3. Start application stack::

    $ docker-compose up -d
    $ docker-compose logs

4. Create a superuser::

    $ docker exec -it tct.app sh
    $ ./manage.py createsuperuser

5. Run tests::

    $ docker exec -it tct.app sh
    $ apk add --no-cache libxslt-dev libffi-dev
    $ pip install -r requirements-dev.txt
    $ ./manage.py test

6. Type: http://localhost:8000

LDAP integration
----------------

Set *ALLOWED_USERS* in settings to restrict access to a specific set of usernames.

Set AUTH_LDAP_SERVER_URI and AUTH_LDAP_USER_DN_TEMPLATE from settings.py for LDAP Authentication configuration. Add 'django_auth_ldap.backend.LDAPBackend' value in AUTHENTICATION_BACKENDS.


Translations
------------

1. Manual translation

Run over the entire source tree and pull out all strings marked for translation, add/edit/delete translations for each file in tct/locale/[LANGUAGE]/LC_MESSAGE/django.po, compile the po files and restart the server::

    $ docker exec -it tct.app sh
    # cd tct
    # django-admin.py makemessages -a
    # django-admin.py compilemessages
    $ docker-compose restart demo

2. Automatic translation

Translate the messages using the Rosetta tool for translation (http://localhost:8000/translate) and restart the server when ready::

    $ docker-compose restart app
