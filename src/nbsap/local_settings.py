DEBUG = True
TEMPLATE_DEBUG = DEBUG

ugettext = lambda s: s

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', ugettext('English')),
    ('fr', ugettext('French')),
)

EU_STRATEGY = True

SITE_HEADER = 'Test'
ASSETS_ROOT = '/Work/sandbox/nbsap/src/nbsap/static'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'raven.contrib.django.middleware.Sentry404CatchMiddleware',
)
