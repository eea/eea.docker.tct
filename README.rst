===============================================
Quick Installation Guide for TCT platform
===============================================

.. contents ::


Project name and whereabouts
----------------------------
The project name is National Biodiversity Strategies and Action Plan (or simply NBSAP).
It is a platform for organizing the implementation of a country's
national biodiversity strategy after AICHI (and by case after EU Strategy).
It consists of two panels each corresponding an operation: viewing and editing.
The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its
own strategy in terms of objectives and actions) and its implementation.
The second panel(Admin), authentication-available only, allows an user to actually define
the national strategy. (e.g. add/modify/delete an objective, action or even
elements from AICHI) in the purpose of building it.


Run in devel with Docker Compose
--------------------------------

**Create and edit the following files**::

Edit *mysql.env*::

  $ cp env-files/mysql.env.example env-files/mysql.env
  $ vim env-files/mysql.env

Edit *demo.env*. You can change the environment variables to suit your needs. In *demo.env.example* file you can see an example of how this variables should look like::

  $ cp env-files/demo.env.example env-files/demo.env
  $ vim env-files/demo.env

**Start the containers**::

  $ docker-compose up -d

**Copy apache.conf file to the Apache container**::

    $ docker cp conf-files/apache.conf tct_apache_1:/usr/local/apache2/conf/extra/vh-my-app.conf
    $ docker-compose restart apache


Common configuration
--------------------

Set *ALLOWED_USERS* in settings to restrict access to a specific set of usernames.

See *settings.py* for LDAP Authentication configuration.


=================
Translation files
=================
For translations there are two methods.

1. Manual translation

Run over the entire source tree and pull out all strings marked for translation::

  $ docker exec -it tct_demo_1 bash
  $ cd tct
  $ django-admin.py makemessages -a

Edit <msgstr> for each <msgid> in tct/locale/_LANGUAGE_/LC_MESSAGE/django.po

Compile .po file created with previous command::

  $ django-admin.py compilemessages

Restart server::

  $ docker-compose restart demo

2. Automatic translation

Enter the application container::

  $ docker exec -it tct_demo_1 bash

Create a superuser::

  $ ./manage.py createsuperuser
  # surf over /translate to use Rosetta tool for translation
  # complete the forms within the correct translations
  # restart server when ready
  $ docker-compose restart demo


========
Contacts
========
The project owner is EEA (European Environment Agency)

Technical development team: contact at eaudeweb.ro


=====================
Copyright and license
=====================
Copyright 2007 European Environment Agency (EEA)

Licensed under the EUPL, Version 1.1 or – as soon they will be approved
by the European Commission - subsequent versions of the EUPL (the "Licence");

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://joinup.ec.europa.eu/software/page/eupl/licence-eupl

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations under the Licence.

