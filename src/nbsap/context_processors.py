from django.conf import settings
from nbsap.models import NavbarLink


def nbsap_admin(request):
    default_lang = settings.LANGUAGE_CODE
    return {
        'EU_STRATEGY': settings.EU_STRATEGY,
        'NAT_STRATEGY': settings.NAT_STRATEGY,
        'SITE_HEADER': settings.SITE_HEADER,
        'WARNING_MESSAGE': getattr(settings, 'WARNING_MESSAGE', ''),
        'DEFAULT_LANGUAGE': default_lang,
        'DEFAULT_LANGUAGE_LABEL': dict(settings.LANGUAGES)[default_lang],
    }


def nbsap_navbar_link(request):
    return {
        'navbar_links': NavbarLink.objects.all(),
        'LAYOUT_FOOTER_LOGO': settings.LAYOUT_FOOTER_LOGO_VISIBLE,
        'LAYOUT_HEADER_LOGO': settings.LAYOUT_HEADER_LOGO_VISIBLE,
        'HEADER_BACKGROUND_IMG': settings.HEADER_BACKGROUND_IMG,
    }


def google_analytics(request):
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)
    if not settings.DEBUG and ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}
