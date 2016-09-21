import json
from cStringIO import StringIO

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

from nbsap import models
from nbsap.utils import sort_by_code, get_adjacent_objects


def get_most_relevant_targets(target):
    most_relevant_targets = []
    if target.eu_aichi_strategy.count():
        for strategy in target.eu_aichi_strategy.all():
            most_relevant_targets.extend(list(strategy.eu_targets.all()))
    return sort_by_code(most_relevant_targets)


def get_other_relevant_targets(target):
    other_relevant_targets = []
    if target.eu_other_aichi_strategy.count():
        for strategy in target.eu_other_aichi_strategy.all():
            other_relevant_targets.extend(list(strategy.eu_targets.all()))
    return sort_by_code(other_relevant_targets)


def get_most_relevant_indicators(target):
    most_relevant_indicators = []
    if target.eu_indicator_aichi_strategy.count():
        for strategy in target.eu_indicator_aichi_strategy.all():
            most_relevant_indicators.append(strategy.eu_indicator)
    return most_relevant_indicators


def user_homepage(request):
    return render(request, 'user_homepage.html')


def list_goals(request):
    goals = models.AichiGoal.objects.order_by('code').all()
    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'goals': goals,
                'list_goals': True,
                'list_targets': False,
            })
    )


def list_targets(request, code=None):
    if code:
        current_goal = get_object_or_404(models.AichiGoal, code=code)
        targets = current_goal.targets.all()
    else:
        current_goal = None
        targets = models.AichiTarget.objects.all()
    goals = models.AichiGoal.objects.order_by('code').all()
    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'current_goal': current_goal,
                'goals': goals,
                'list_goals': False,
                'list_targets': True,
                'targets': targets,
            })
    )


def aichi_goals(request, code=None):
    if not code:
        return list_goals(request)
    else:
        aichi_target_id = sort_by_code(get_object_or_404(
            models.AichiGoal, code=code).targets.all())[0].pk
        return aichi_target_detail(request, code, aichi_target_id)


def aichi_target_detail(request, aichi_target_id, code=None):
    if not code:
        code = get_object_or_404(models.AichiTarget,
                                 pk=aichi_target_id).get_parent_goal().code

    goals = models.AichiGoal.objects.order_by('code').all()
    current_goal = get_object_or_404(models.AichiGoal, code=code)
    all_targets = sort_by_code(models.AichiTarget.objects.all())
    targets = sort_by_code(current_goal.targets.all())
    target = get_object_or_404(models.AichiTarget,
                               pk=aichi_target_id)

    if target not in current_goal.targets.all():
        raise Http404

    previous_target, next_target = get_adjacent_objects(all_targets, target)

    info_header = settings.INFO_HEADER

    target.most_relevant_targets = get_most_relevant_targets(target)
    target.other_relevant_targets = get_other_relevant_targets(target)
    target.most_relevant_indicators = get_most_relevant_indicators(target)

    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'goals': goals,
                'targets': targets,
                'all_targets': all_targets,
                'target': target,
                'info_header': info_header,
                'previous_target': previous_target,
                'next_target': next_target
            })
    )


def eu_target_nat_strategy_export_preview(request, target_id):
    target = get_object_or_404(models.AichiTarget, pk=target_id)
    return render(request, 'objectives/nat_strategy_export_preview.html', {
        'target': target,
    })


def eu_target_nat_strategy_export(request, target_id):
    target = get_object_or_404(models.AichiTarget, pk=target_id)
    template = 'objectives/nat_strategy_export_preview.html'
    contents = StringIO(render_to_string(template, {
        'target': target, 'download': True
    }))
    resp = HttpResponse(contents.getvalue(), content_type='application/msword')
    resp['Content-Disposition'] = 'attachment; filename=nat_strategy.doc'
    return resp


def get_goal_title(request, pk=None):
    if not pk:
        return HttpResponse('Goal not found')

    goal = get_object_or_404(models.AichiGoal, pk=pk)
    targets = [{'pk': target.pk, 'value': target.pk}
               for target in goal.targets.all()]

    return HttpResponse(json.dumps([
        {'goal': goal.description, 'targets': targets, 'code': pk}]))


def get_aichi_target_title(request, pk=None):
    if not pk:
        return HttpResponse('Aichi target not found')

    target = get_object_or_404(models.AichiTarget, pk=pk)
    return HttpResponse(json.dumps(
        [{'code': target.code, 'value': target.description}]))


def get_eu_indicator_title(request, pk=None):
    if not pk:
        return HttpResponse('EU Indicator not found')

    indicator = get_object_or_404(models.EuIndicator, pk=pk)
    return HttpResponse(json.dumps(
        [{'code': indicator.code, 'title': indicator.title,
          'indicator_type': indicator.indicator_type}]))
