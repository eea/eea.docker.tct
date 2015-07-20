import re
from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.filter('field_verbose_name')
def get_field_verbose_name(instance, arg):
    return instance._meta.get_field(arg).verbose_name


@register.filter('key')
def key(d, key_name):
    return d[key_name]


@register.filter('get_page')
def get_page(id):
    if id % 20 != 0:
        return int(id / 20) + 1
    else:
        return int(id / 20)


@register.filter('sort_by_code')
def sort_by_code(value):
    return sorted(value, key=lambda i: map(int, i.code.split('.')))


@register.assignment_tag
def assign(value):
    return value


@register.assignment_tag
def get_goals_for_strategies(strategies):
    goals = set(
        [
            target.get_parent_goal()
            for s in strategies
            for target in s.relevant_targets.all()
        ]
    )
    return goals


@register.assignment_tag
def get_targets_for_strategies(strategies):
    targets = set([s.relevant_target for s in strategies])
    return targets


@register.assignment_tag
def get_other_targets_for_strategies(strategies):
    targets = []
    for s in strategies:
        targets.extend([i for i in s.other_targets.all()])
    return set(targets)
