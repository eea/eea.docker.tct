import json
from cStringIO import StringIO

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

from nbsap import models
from nbsap.models import sort_by_code
from indicators import get_indicators_pages


def list_goals(request):
    goals = models.AichiGoal.objects.order_by('code').all()
    list_goals = True
    list_targets = False
    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'goals': goals,
                'list_goals': list_goals,
                'list_targets': list_targets,
            })
    )


def list_targets(request, code=None):
    if code:
        current_goal = models.AichiGoal.objects.get(code=code)
        targets = models.AichiGoal.objects.get(code=code).targets.all()
    else:
        current_goal = None
        targets = models.AichiTarget.objects.all()

    goals = models.AichiGoal.objects.order_by('code').all()
    list_goals = False
    list_targets = True

    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'current_goal': current_goal,
                'goals': goals,
                'list_goals': list_goals,
                'list_targets': list_targets,
                'targets': targets,
            })
    )


def goals(request, code=None, aichi_target_id=None):
    if not code and aichi_target_id:
        code = models.AichiTarget.objects.get(
            pk=aichi_target_id).get_parent_goal().code
    if code:
        current_goal = models.AichiGoal.objects.get(code=code)
        targets = current_goal.targets.all()
    else:
        current_goal = None
        targets = models.AichiTarget.objects.all()

    goals = models.AichiGoal.objects.order_by('code').all()

    indicators_list = models.AichiIndicator.objects.all()

    if not aichi_target_id:
        target = sort_by_code(current_goal.targets.all())[0]
    else:
        target = current_goal.targets.get(pk=aichi_target_id)

    paginator = Paginator(indicators_list, 20)
    info_header = settings.INFO_HEADER

    return render_to_response(
        'aichi/aichi.html',
        context_instance=RequestContext(
            request, {
                'code': code,
                'goals': goals,
                'targets': targets,
                'target': target,
                'indicators_pages': get_indicators_pages(paginator),
                'info_header': info_header,
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
