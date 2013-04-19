from django.conf import settings

def eu_strategy(request):
    return {
        'EU_STRATEGY': getattr(settings, 'EU_STRATEGY', '')
    }
