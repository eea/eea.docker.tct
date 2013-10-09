from django.conf import settings
import re

def nbsap_admin(request):
    return {
        'EU_STRATEGY': getattr(settings, 'EU_STRATEGY', False),
        'SITE_HEADER': getattr(settings, 'SITE_HEADER', 'NBSAP'),
        'DEFAULT_LANGUAGE': settings.LANGUAGE_CODE,
    }
