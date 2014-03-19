===============================================
NBSAP Quick Installation Guide for TODO
===============================================

.. contents ::

Following this readme will create an isolated environment for running NBSAP platform.
There are three configurations available for running this buildout::
  1. production (production)
  2. testing (staging)
  3. development (devel)

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
This buildout was tested on linux (debian based and RHEL based)

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


Debian based systems
~~~~~~~~~~~~~~~~~~~
::
TODO

Product directory
~~~~~~~~~~~~~~~~
::

  $ mkdir -p /var/local/nbsap
  $ chown -R [USER]:[USER] /var/local/nbsap
  $ exit


Build production
----------------
TODO

Build staging
-------------
TODO

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
  $ pip install -r requirements.txt
  $ pip install -e .
  $ cp instance/local_settings.py.example instance/local_settings.py

Prepare database::
  mysql> create database nbsap DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
  mysql> grant all on nbsap.* to nbsap@localhost identified by 'nbsap';

Tune up manage.py script::
  The first line should define the python executable used to run the script. This should be the path to your virtualenv's python. In this particular case it should be:
  #!/var/local/nbsap/django/sandbox/bin/python

Continue build devel by syncing database model and loading fixtures::
  $ ./instance/manage.py syncdb
  $ ./instance/manage.py load_fixtures

Configure supervisord::
  $ cp supervisord.conf.sample sandbox/supervisord.conf
  # edit sandbox/supervisord.conf with corresponding PROJECT_ROOT path
  $ supervisord
  # double check system is running with no errors
  $ supervisorctl


=================
Translation files
=================
You will need to update translations from time to time as new i18n:translate tags
are added to the project. There are 2 places translation tags are picked from:
 * the zpt files found in the Product source files
 * the ZODB (either DTMLs or Page Templates)


Updating translations
---------------------

Updating po files will assume that you have acces to the Products.Reportek source
So will we do this from staging. If for any reason there are translation tags in
the production ZODB that are not in the bdr-test then you need to find a way
to import them in the bdr-test ZODB.

In order to regenerare translation files got to buzzardNT and::

  $ sudo su - zope
  $ cd /var/local/bdr/staging/zope
  $ ./bin/supervisorctl stop instance
  $ cd src/Products.Reportek/extras
  $ /var/local/bdr/staging/zope/bin/instance debug
  >>> import zodb_scripts
  >>> zodb_scripts.dump_code(app)
  >>> CTRL+d
  $ /var/local/bdr/staging/zope/bin/supervisorctl start instance
  $ cd /var/local/bdr/staging/zope/src/Products.Reportek/Products/Reportek/locales
  $ ./update.sh [path/to/i18ndude - default buzzardNT staging deployment bin dir]
  - commit changes

Update translations - alternative
--------------------------------
This is done on the developer's machine.

 * Get backups from production
 * put them on dev machine on an instalation of bdr
 * use staging or development deployment to have the sources, checkout at a specific date in order to match the egg on production if required
 * follow the steps above with the fs paths of your machine.
Note that you will probably not be able to login not having a local ldap of your own, but that is not required


Generate xliff files
--------------------
::

  $ sudo su - zope
  $ cd /var/local/bdr/staging/zope/src/
  $ ./Products.Reportek/Products/Reportek/locales/generate-xliff.sh <name of output dir>

The output dir must not already exist
The result will be an archive <name of output dir>.tar.gz, on the same level
with the designated dir output dir. Its structure will mimic the one of locales dir


Generate po from xlf
--------------------
Start with the result of upacking an arhive like the one obtained at the
previous step::

  $ xliff2po locales.xlf.dir locales.po.dir

The result dir will have the structure of the source dir and beable to substitue
the language code dirs found in source Products.Reportek/Products/Reportek/locales


========
Contacts
========
The project owner is Søren Roug (soren.roug at eaa.europa.eu)

Other people involved in this project are::
 - Cornel Nițu (cornel.nitu at eaudeweb.ro)
 - Miruna Bădescu (miruna.badescu at eaudeweb.ro)
 - Daniel Mihai Bărăgan (daniel.baragan at eaudeweb.ro)


=========
Resources
=========
Minimum requirements:
 * 2048MB RAM
 * 2 CPU 1.8GHz or faster
 * 4GB hard disk space

Recommended:
 * 4096MB RAM
 * 4 CPU 2.4GHz or faster
 * 8GB hard disk space


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

