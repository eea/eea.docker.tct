from django.conf import settings
from nbsap.models import NavbarLink
import re


def nbsap_admin(request):
    default_lang = settings.LANGUAGE_CODE
    return {
        'EU_STRATEGY': getattr(settings, 'EU_STRATEGY', False),
        'SITE_HEADER': getattr(settings, 'SITE_HEADER', 'NBSAP'),
        'WARNING_MESSAGE': getattr(settings, 'WARNING_MESSAGE', ''),
        'DEFAULT_LANGUAGE': default_lang,
        'DEFAULT_LANGUAGE_LABEL': dict(settings.LANGUAGES)[default_lang],
    }


def nbsap_navbar_link(request):
    return {'navbar_links': NavbarLink.objects.all()}


def google_analytics(request):
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}
