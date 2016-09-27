from django import template
from nbsap.utils import sort_by_code, sort_by_type, sort_by_type_and_code
from nbsap.utils import sort_by_code_tuplets

register = template.Library()

register.filter('sort_by_code', sort_by_code)
register.filter('sort_by_code_tuplets', sort_by_code_tuplets)
register.filter('sort_by_type', sort_by_type)
register.filter('sort_by_type_and_code', sort_by_type_and_code)


@register.simple_tag(takes_context=True)
def active(context, *args):
    if context['request'].resolver_match.url_name in args:
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
    targets = []
    for s in strategies:
        targets.extend(s.relevant_targets.all())
    targets = list(set(targets))
    try:
        targets.sort(cmp=lambda a, b: int(
            10 * (float(a.code) - float(b.code))))
    except:
        pass
    return targets


@register.assignment_tag
def get_other_targets_for_strategies(strategies):
    targets = []
    for s in strategies:
        targets.extend([i for i in s.other_targets.all()])
    return set(targets)
