from tct.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

NAT_STRATEGY = True
EU_STRATEGY = True
SECRET_KEY = 'test-secret'

MIGRATION_MODULES = {
    'tct': None,
}

import logging
logging.getLogger("factory").setLevel(logging.ERROR)
