from django.conf import settings
import re

def nbsap_admin(request):
    default_lang = settings.LANGUAGE_CODE
    return {
        'EU_STRATEGY': getattr(settings, 'EU_STRATEGY', False),
        'SITE_HEADER': getattr(settings, 'SITE_HEADER', 'NBSAP'),
        'DEFAULT_LANGUAGE': default_lang,
        'DEFAULT_LANGUAGE_LABEL': dict(settings.LANGUAGES)[default_lang],
    }
