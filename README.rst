Product owner:
-------
    * Franz Daffner
    * franz.daffner@eea.europa.eu

Min. hardware resources
-------

    * [CPU] Single Core >= 2.5 GHz
    * [RAM] 1024 MB
    * [Hard disc] current necessary < 1 GB
    * [Hard disc] 6 months forecast <= 20 GB
    * [NIC] 100 Mbit

About
-------
National Biodiversity Strategies and Action Plan (or simply NBSAP)
is a platform for organizing the implementation of a country's
national biodiversity strategy after AICHI (and by case after EU Strategy).
It consists of two panels each corresponding an operation: viewing and editing.

The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its
own strategy in terms of objectives and actions) and its implementation.

The second panel(Admin), authentication-available only, allows an user to actually define
the national strategy. (e.g. add/modify/delete an objective, action or even
elements from AICHI) in the purpose of building it.

NBSAP Quick Installation Guide
=====
0. Prerequisites packages if missing::

    python-setuptools python-dev mysql-server libmysqlclient-dev virtualenv
    Python 2.7.3 - compiled or by native system


1. Clone the repository::

    git clone git@mojito.edw.ro:nbsap.git nbsap
    cd nbsap


2. Create & activate a virtual environment (with Pyhon 2.7.3)::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    . sandbox/bin/activate


3. Install dependecies & others::

    pip install -U distribute
    pip install -r requirements.txt
    pip install -e .


4. Assuming the root of your project is ROOT_PROJECT, add the following lines in a ROOT_PROJECT/instance/local_settings.py file::

    ASSETS_ROOT = 'ROOT_PROJECT/src/nbsap/static'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    # define your language preference
    ugettext = lambda s: s
    LANGUAGE_CODE = 'en'
    LANGUAGES = (
       ('en', ugettext('English')),
       ('fr', ugettext('French')),
       ('nl', ugettext('Dutch')),

    # if application is EU dependent
    EU_STRATEGY = False
    SITE_HEADER = 'Your site header'

    DEBUG = False

