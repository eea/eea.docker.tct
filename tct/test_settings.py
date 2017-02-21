DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

NAT_STRATEGY = True
EU_STRATEGY = True

import logging
logging.getLogger("factory").setLevel(logging.ERROR)
