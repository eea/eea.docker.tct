from django.contrib import messages
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.conf import settings
from django.core.management import call_command

def create_admin(app, created_models, verbosity, **kwargs):
    if settings.DEBUG:
        try:
            auth_models.User.objects.get(username='jadmin')
        except auth_models.User.DoesNotExist:
            print '*' * 50
            print 'Creating admin user "admin" with password "qC@rn3l"'
            print '*' * 50
            assert auth_models.User.objects.create_superuser('jadmin',
                                                             'jadmin@example.com',
                                                             'qC@rn3l')
        else:
            print '*' * 50
            print 'Admin user is "jadmin" with password "qC@rn3l".'
            print '*' * 50

def load_data(sender, **kwargs):
    if settings.EU_STRATEGY:
        call_command('loaddata', 'initial_data_eu_and_aichi.json')
    else:
        call_command('loaddata', 'initial_data_aichi.json')

signals.post_syncdb.connect(
    create_admin,
    sender=auth_models,
    dispatch_uid='apps.auth.models.create_admin')


signals.post_syncdb.connect(
    load_data,
    sender=auth_models,
    dispatch_uid='apps.auth.models.load_data')
