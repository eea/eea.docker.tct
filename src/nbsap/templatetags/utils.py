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


def key(d, key_name):
    return d[key_name]
key = register.filter('key', key)


def get_page(id):
    if id%20 != 0:
        return int(id/20) + 1
    else:
        return int(id/20)
key = register.filter('get_page', get_page)


@register.filter('sort_by_code')
def sort_by_code(value):
    return sorted(value, key=lambda i: map(int, i.code.split('.')))


@register.assignment_tag
def assign(value):
    return value
