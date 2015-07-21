DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    }
}

SOUTH_TESTS_MIGRATE = False

NAT_STRATEGY = True
EU_STRATEGY = True

import logging
logging.getLogger("factory").setLevel(logging.ERROR)
