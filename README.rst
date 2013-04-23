1. Prerequisites TODO:

git clone git@mojito.edw.ro:nbsap.git nbsap

apt-get install mysql-server
apt-get install libmysqlclient-dev
apt-get install python-dev

pip install mysql-python
pip install -U distribute
pip install -r requirements.txt
pip install -e .

2. Assuming the root of your project is ROOT_PROJECT, add the following lines
in a ROOT_PROJECT/local_settings.py file:

ASSETS_ROOT = 'ROOT_PROJECT/src/nbsap/static'
TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = '/static/js/tiny_mce'

# depending your needs
EU_STRATEGY = True

