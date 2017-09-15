from django.conf import settings
from tct.models import NavbarLink
from getenv import env


def tct_admin(request):
    default_lang = settings.LANGUAGE_CODE
    return {
        'EU_STRATEGY': settings.EU_STRATEGY,
        'EU_STRATEGY_ADD': settings.EU_STRATEGY_ADD,
        'NAT_STRATEGY': settings.NAT_STRATEGY,
        'SITE_HEADER': settings.SITE_HEADER,
        'WARNING_MESSAGE': getattr(settings, 'WARNING_MESSAGE', ''),
        'DEFAULT_LANGUAGE': default_lang,
        'DEFAULT_LANGUAGE_LABEL': dict(settings.LANGUAGES)[default_lang],
        'DEBUG': settings.DEBUG,
        'INSTANCE_NAME': getattr(settings, 'INSTANCE_NAME', ''),
    }


def tct_navbar_link(request):
    return {
        'navbar_links': NavbarLink.objects.all(),
        'LAYOUT_FOOTER_LOGO': settings.LAYOUT_FOOTER_LOGO_VISIBLE,
        'LAYOUT_HEADER_LOGO': settings.LAYOUT_HEADER_LOGO_VISIBLE,
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


def login(request):
    return {'RESTRICTED_ACCESS': bool(getattr(settings, 'ALLOWED_USERS', []))}


def sentry(request):
    sentry_id = ''
    if hasattr(request, 'sentry'):
        sentry_id = request.sentry['id']
    return {
        'sentry_id': sentry_id,
        'sentry_public_id': getattr(settings, 'SENTRY_PUBLIC_DSN', ''),
    }
