DEBUG = True
TEMPLATE_DEBUG = DEBUG

ASSETS_ROOT = 'src/nbsap/static'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# define your language preference
ugettext = lambda s: s
LANGUAGE_CODE = 'en'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'nbsap',
#         'USER': 'nbsap',
#         'PASSWORD': 'nbsap',
#         'HOST': '',
#         'PORT': '',
#         'TEST_CHARSET': 'utf8',
#         'TEST_COLLATION': 'utf8_general_ci',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'nbsap.de',
    }
}


# please use full mappings
LANGUAGES = (
  ('en', ugettext('English')),
)

# Set to True if your application is EU dependent
EU_STRATEGY = True
# Allow adding new targets
EU_STRATEGY_ADD = False

# Set to False for EU intance
NAT_STRATEGY = True

# Template settings
SITE_HEADER = 'Reporting tool towards the AICHI targets, contribution by Italy'

# Set to True for information header
#INFO_HEADER = False

# Set to True to show layout footer logo
#LAYOUT_FOOTER_LOGO_VISIBLE = False

# Set to True to show layout header logo
#LAYOUT_HEADER_LOGO_VISIBLE = False

# Set the path to the image to be used as background
#HEADER_BACKGROUND_IMG = '/static/header.png'

# Set the variable below to allow only certain users to use the application
# ALLOWED_USERS = ['admin']

# LDAP login
#AUTHENTICATION_BACKENDS = (
#    'django.contrib.auth.backends.ModelBackend',
#    'django_auth_ldap.backend.LDAPBackend',
#)
#AUTH_LDAP_SERVER_URI = "ldap://nas.edw.lan"
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,cn=users,dc=edw,dc=lan"

#Set to True if REG is a valid National Indicator value
#ENABLE_REG_INDICATORS = False

# Set the following variables to enable communication with the CBD API
# CBD_API_USERNAME = ''
# CBD_API_PASSWORD = ''
# CBD_API_REALM = 'CHM-DEV'
# CBD_API_LANGUAGES = ['ar', 'zh', 'en', 'fr', 'ru', 'es']
# CBD_API_BASE_URL = 'https://api.cbddev.xyz/api/v2013/'
# CBD_AUTH_URL = CBD_API_BASE_URL + 'authentication/token'
# CBD_SAVE_URL = CBD_API_BASE_URL + 'documents/{uid}/versions/draft?schema={schema}'
# CBD_WORKFLOW_URL = CBD_API_BASE_URL + 'workflows'
# CBD_VERIFY_SSL = True

FACILITY = 'tct_it'

INSTANCE_NAME = 'Contribution by Italy'

