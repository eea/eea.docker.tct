import re
from django import template


register = template.Library()


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

def get_field_verbose_name(instance, arg):
    return instance._meta.get_field(arg).verbose_name
register.filter('field_verbose_name', get_field_verbose_name)
