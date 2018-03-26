import os
import sys
# Fixes bug that is being thrown by postgres interacting with ldap (see http://stackoverflow.com/questions/38740631/need-to-pre-import-module-to-avoid-error)
import ldap
from getenv import env
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = env('DEBUG', False)

ASSETS_ROOT = os.path.join(BASE_DIR, 'static')
ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]


LANGUAGE_CODE = 'en'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASES_NAME', 'demo'),
        'USER': env('DATABASES_USER', 'demo'),
        'PASSWORD': env('DATABASES_PASSWORD', 'password'),
        'HOST': 'postgres',
        'PORT': '',
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

ALL_LANGUAGES = (
    ('en', 'English'),
    ('cs', 'Czech'),
    ('sq-al', 'Albanian'),
    ('lt', 'Lithuanian'),
    ('hy', 'Armenian'),
    ('fr', 'French'),
    ('nl', 'Dutch'),
    ('ru', 'Russian'),
    ('tr', 'Turkish'),
    ('pl', 'Polish'),
    ('ky', 'Kyrgyz'),
    ('bg', 'Bulgaria'),
    ('de-at', 'German'),
    ('az-az', 'Azeri'),
    ('uk', 'Ukrainian'),
    ('tk', 'Turkmen'),
    ('be-by', 'Belarusian'),
    ('se-se', 'Sami'),
    ('uz', 'Uzbek'),
    ('sk', 'Slovak'),
    ('fi', 'Finnish'),
    ('no', 'Norwegian'),
    ('is', 'Icelandic'),
    ('de-de', 'German'),
    ('fr-ch', 'French'),
    ('de-ch', 'German'),
    ('it-ch', 'Italian'),
    ('ro', 'Romanian'),
    ('de-li', 'German'),
    ('hu', 'Hungarian'),
    ('bs-ba', 'Bosnian'),
    ('lv', 'Latvian'),
    ('it-it', 'Italian'),
    ('fr-mc', 'French'),
    ('sl', 'Slovenian'),
    ('ka', 'Georgian'),
    ('hr-hr', 'Croatian'),
    ('mk', 'Macedonian'),
    ('me', 'Montenegrin'),
    ('ca', 'Catalan'),
    ('sr', 'Serbian'),
    ('sq', 'Albanian'),
    ('tg', 'Tajik'),
    ('kk', 'Kazakh'),
    ('pt-pt', 'Portuguese'),
    ('mt', 'Maltese'),
    ('et', 'Estonian'),
    ('fr-lu', 'French'),
    ('de-lu', 'German'),
    ('es-es', 'Spanish'),
    ('md', 'Moldavian'),
    ('da-dk', 'Danish'),
    ('el-gr', 'Greek'),
)


def get_languages(ENV_LANGUAGES):
    LANGUAGES = filter(lambda language:
                       language[0] in ENV_LANGUAGES.split(','), ALL_LANGUAGES)
    utext_languages = ()
    for lang in LANGUAGES:
        utext_languages += ((lang[0], _(lang[1])),)
    return utext_languages


# define your language preference
LANGUAGES = get_languages(env('LANGUAGES')) if env('LANGUAGES') else (
    ('en', _('English')),
    ('fr', _('French')),
    ('nl', _('Dutch')),
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
SECRET_KEY = env('SECRET_KEY', '8u6d#h7cga4a!&qya#-e2ct%%&$1u^ce5rub$9#1zcn=n$j@^h')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tct', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'tct.context_processors.sentry',
                'tct.context_processors.tct_admin',
                'tct.context_processors.tct_navbar_link',
                'tct.context_processors.google_analytics',
                'tct.context_processors.login',
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
    'tct.middleware.LoginRequiredMiddleware',
)

ASSETS_DEBUG = True

ROOT_URLCONF = 'tct.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tct.wsgi.application'


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
    'tct',
    'chosen',
    'gunicorn',
    'rosetta',
    'graypy',
    'mptt',
    'hijack',
    'compat',
    'hijack_admin',

)

# sentry configuration
SENTRY_PUBLIC_DSN = env('SENTRY_PUBLIC_DSN', '')
if env('SENTRY_DSN', ''):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {'dsn': env('SENTRY_DSN')}

GOOGLE_ANALYTICS_PROPERTY_ID = env('GOOGLE_ANALYTICS_PROPERTY_ID', '')

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

# TCT special variables
LOGIN_REDIRECT_URL = '/'

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/'
HIJACK_ALLOW_GET_REQUESTS = True

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
TINYMCE_JS_URL = 'js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = 'js/tiny_mce'

CSS_ASSETS = ()


# Main config
EU_STRATEGY = env('EU_STRATEGY', False)
EU_STRATEGY_ADD = env('EU_STRATEGY_ADD', False)
NAT_STRATEGY = env('NAT_STRATEGY', True)
SITE_HEADER = env('SITE_HEADER', 'Reporting tool towards the AICHI targets,')
INFO_HEADER = env('INFO_HEADER', False)
LAYOUT_HEADER_LOGO_VISIBLE = env('LAYOUT_HEADER_LOGO_VISIBLE', False)
LAYOUT_FOOTER_LOGO_VISIBLE = env('LAYOUT_FOOTER_LOGO_VISIBLE', False)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=tct',
]

# Set the variable below to allow only certain users to use the application
# ALLOWED_USERS = ['admin']

# LDAP login
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)

AUTH_LDAP_SERVER_URI = "ldap://ldap.eionet.europa.eu"
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=Users,o=EIONET,l=Europe"

# Set to True if REG is a valid National Indicator value
ENABLE_REG_INDICATORS = env('ENABLE_REG_INDICATORS', False)

# Set the following variables to enable communication with the CBD API
# CBD_API_USERNAME = ''
# CBD_API_PASSWORD = ''
# CBD_API_REALM = 'CHM-DEV'
# CBD_API_LANGUAGES = ['ar', 'zh', 'en', 'fr', 'ru', 'es']
# CBD_API_BASE_URL = 'https://api.cbddev.xyz/api/v2013/'
# CBD_AUTH_URL = CBD_API_BASE_URL + 'authentication/token'
# CBD_SAVE_URL = CBD_API_BASE_URL + \
#     'documents/{uid}/versions/draft?schema={schema}'
# CBD_WORKFLOW_URL = CBD_API_BASE_URL + 'workflows'
# CBD_VERIFY_SSL = True


FACILITY = env('FACILITY', 'tct')
INSTANCE_NAME = env('INSTANCE_NAME', 'Testing Instance')

LOGGING['handlers']['graypy']['facility'] = FACILITY

if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass
