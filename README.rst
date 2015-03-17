===============================================
Quick Installation Guide for NBSAP platform
===============================================

.. contents ::

Following this readme will create an isolated environment for running NBSAP platform.
There are three configurations available for running this buildout::
  1. production (production)
  2. testing (staging)
  3. development (development)


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


Prerequisites - System packages
-------------------------------
These should be installed by the sysadmin (needs root)
This buildout was tested on RHEL based-linux.


RHEL based systems
~~~~~~~~~~~~~~~~~
We will need pip to install some python related packages for versions greater
than the python shipped with RHEL 6.5. We will also need additional repos: PUIAS

Install prerequisites::

  $ yum install openssl-devel vim wget

Bring out puias repo for python 2.7::

  $ touch /etc/yum.repos.d/puias-computational.repo

Copy the following lines into the above mentioned file::

  [PUIAS_6_computational]
  name=PUIAS computational Base $releasever - $basearch
  mirrorlist=http://puias.math.ias.edu/data/puias/computational/$releasever/$basearch/mirrorlist
  #baseurl=http://puias.math.ias.edu/data/puias/computational/$releasever/$basearch
  gpgcheck=1
  gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias

Download and import the Repo GPG key::

  $ cd /etc/pki/rpm-gpg/
  $ wget -q http://springdale.math.ias.edu/data/puias/6/x86_64/os/RPM-GPG-KEY-puias
  $ rpm --import RPM-GPG-KEY-puias

Install python packages::

  $ sudo bash
  $ yum install python27 python27-devel python27-libs python27-setuptools git
  $ yum install mysql-devel mysql-server
  $ service mysqld restart
  $ easy_install-2.7 virtualenv


Product directory
~~~~~~~~~~~~~~~~
::

  $ mkdir -p /var/local/nbsap
  $ chown -R [USER]:[USER] /var/local/nbsap
  $ exit


Build production
----------------
::

  # copy and adjust env dict in fabfile.py.sample
  # then define own Fabric file
  $ cp fabfile.py.sample fabfile.py

Deploy code on remote host::

  $ fab install:target=production

Login on remote machine::

  # activate production-venv virtualenv

Prepare database on remote machine::

  mysql> create database nbsap DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
  mysql> grant all on nbsap.* to nbsap@localhost identified by 'nbsap';

Configure supervisord on remote machine::

  $ cp supervisord.conf.sample production-venv/supervisord.conf
  # edit production-venv/supervisord.conf with corresponding PROJECT_ROOT path
  $ supervisord
  # double check system is running with no errors
  $ supervisorctl

Tune Django to serve static files::

 $ cd /var/local/project-root
 $ mkdir static
 $ echo "STATIC_ROOT = '/var/local/project-root/static'" >> instance/local_settings.py
 $ ./instance/manage.py collectstatic --noinput

Tune Apache to proxy-pass and serve static files for the app::

  # Add the following entry to http conf files
  #    <VirtualHost *:80>
  #      ServerName nbsap...
  #      Alias /static /var/local/project-root/static
  #      ProxyPass /static !
  #      ProxyPass / http://localhost:[PORT]/
  #      ProxyPassReverse / http://localhost:[PORT]/
  #    </VirtualHost>


Restart Apache to load new changes::

  $ service httpd reload


Build staging
-------------
::

  # copy and adjust env dict in fabfile.py.sample
  # then define own Fabric file
  $ cp fabfile.py.sample fabfile.py

Deploy code on remote host::

  $ fab install

Login on remote machine::

  # activate staging-venv virtualenv

Prepare database on remote machine::

  mysql> create database nbsap DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
  mysql> grant all on nbsap.* to nbsap@localhost identified by 'nbsap';

Configure supervisord on remote machine::

  $ cp supervisord.conf.sample staging-venv/supervisord.conf
  # edit staging-venv/supervisord.conf with corresponding PROJECT_ROOT path
  $ supervisord
  # double check system is running with no errors
  $ supervisorctl

Tune Django to serve static files::

 $ cd /var/local/project-root
 $ mkdir static
 $ echo "STATIC_ROOT = '/var/local/project-root/static'" >> instance/local_settings.py
 $ ./instance/manage.py collectstatic --noinput

Tune Apache to proxy-pass and serve static files for the app::

  # Add the following entry to http conf files
  #    <VirtualHost *:80>
  #      ServerName nbsap...
  #      Alias /static /var/local/project-root/static
  #      ProxyPass /static !
  #      ProxyPass / http://localhost:[PORT]/
  #      ProxyPassReverse / http://localhost:[PORT]/
  #    </VirtualHost>


Restart Apache to load new changes::

  $ service httpd reload



Build devel
-------------
::

  $ cd /var/local/nbsap
  $ git clone https://github.com/eea/nbsap.git django
  $ cd django
  $ virtualenv-2.7 --no-site-packages sandbox
  $ echo '*' > sandbox/.gitignore
  $ . sandbox/bin/activate
  $ pip install -U distribute
  $ pip install -r requirements-dev.txt
  $ pip install -e .
  $ cp instance/local_settings.py.example instance/local_settings.py

Select preferred languages::

  # edit instance/local_settings.py and filter the preferred languages

Prepare database::

  mysql> create database nbsap DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
  mysql> grant all on nbsap.* to nbsap@localhost identified by 'nbsap';

Tune up manage.py script::

  The first line should define the python executable used to run the script. This should be the path to your virtualenv's python. In this particular case it should be:
  #!/var/local/nbsap/django/sandbox/bin/python

Continue build devel by syncing database model and loading fixtures::

  $ ./instance/manage.py syncdb
  $ ./instance/manage.py load_fixtures

Run the tests to check the validity of your installation::

  $ ./instance/manage.py test nbsap

Start running development server::

  $ ./instance/manage.py runserver


Common configuration
--------------------

Set `ALLOWED_USERS` in settings to restrict access to a specific set of usernames.
See `local_settings.py.example` for LDAP Authentication configuration.


=================
Translation files
=================
For translations there are two methods.

1. Manual translation

Run over the entire source tree and pull out all strings marked for translation::

  $ cd src/nbsap
  $ django-admin.py makemessages -a

Edit <msgstr> for each <msgid> in nbsap/locale/_LANGUAGE_/LC_MESSAGE/django.po

Compile .po file created with previous command::

  $ cd src/nbsap
  $ django-admin.py compilemessages

Restart server::

  # if devel mode
  $ ./instance/manage.py runserver
  # otherwise
  $ supervisorctl
  supervisor> restart nbsap

2. Automatic translation

Make sure 'DEBUG=True' in instance/local_settings.py so that an admin user is
automatically generated when starting sever::

  $ ./instance/manage.py runserver
  # surf over [HOST]:[PORT]/translate to use Rosetta tool for translation
  # complete the forms within the correct translations
  # restart server when ready
  $ ./instance/manage.py runserver


========
Contacts
========
The project owner is Franz Daffner (franz.daffner at eaa.europa.eu)

Other people involved in this project are::
 - Cornel Nițu (cornel.nitu at eaudeweb.ro)
 - Miruna Bădescu (miruna.badescu at eaudeweb.ro)
 - Mihai Tabără (mihai.tabara at eaudeweb.ro)
 - Dragoș Catarahia (dragos.catarahia at eaudeweb.ro)


=========
Resources
=========
Minimum requirements:
 * [CPU] Single Core >= 2.5 GHz
 * [RAM] 2048 MB
 * [Hard disc] current necessary < 1 GB
 * [Hard disc] 6 months forecast <= 10 GB
 * [NIC] 100 Mbit


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

