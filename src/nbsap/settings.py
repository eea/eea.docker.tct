import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),
    ('fr', ugettext('French')),
    ('nl', ugettext('Dutch')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8u6d#h7cga4a!&qya#-e2ct%%&$1u^ce5rub$9#1zcn=n$j@^h'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'nbsap', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.i18n',
                'nbsap.context_processors.nbsap_admin',
                'nbsap.context_processors.nbsap_navbar_link',
                'nbsap.context_processors.google_analytics',
                'nbsap.context_processors.login',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'nbsap.middleware.LoginRequiredMiddleware',
)

ASSETS_DEBUG = True

ROOT_URLCONF = 'nbsap.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'nbsap.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_assets',
    'django_webtest',
    'widget_tweaks',
    'transmeta',
    'tinymce',
    'nbsap',
    'chosen',
    'gunicorn',
    'rosetta',
    'graypy',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'graypy': {
            'level': 'WARNING',
            'class': 'graypy.GELFHandler',
            'host': 'logcentral.eea.europa.eu',
            'port': 12201,
            'facility': 'tct',
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'graypy'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# NBSAP special variables
LOGIN_REDIRECT_URL = '/'

TINYMCE_DEFAULT_CONFIG = {
    "theme_advanced_buttons1": ("formatselect,"
                                "separator, bold, italic, "
                                "underline, strikethrough, separator,"
                                "justifyleft,justifycenter, justifyright,"
                                "justifyfull, separator, bullist, numlist,"
                                "separator, link, code")
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = '/static/js/tiny_mce'

CSS_ASSETS = ()

ASSETS_ROOT = os.path.join(BASE_DIR, 'static')

# Main config
EU_STRATEGY = False
EU_STRATEGY_ADD = False
NAT_STRATEGY = True
SITE_HEADER = 'NBSAP'
INFO_HEADER = False
LAYOUT_FOOTER_LOGO_VISIBLE = False
LAYOUT_HEADER_LOGO_VISIBLE = False
HEADER_BACKGROUND_IMG = '/static/header.png'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=nbsap',
]

FACILITY = 'tct'


try:
    from local_settings import *
except ImportError:
    pass


LOGGING['handlers']['graypy']['facility'] = FACILITY

if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass
