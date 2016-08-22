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
from indicators import get_indicators_pages


def goals(request, code=None, aichi_target_id=None):
    if code:
        current_goal = models.AichiGoal.objects.get(code=code)
        targets = current_goal.targets.all()
    else:
        current_goal = None
        targets = models.AichiTarget.objects.all()
    goals = models.AichiGoal.objects.order_by('code').all()

    indicators_list = models.AichiIndicator.objects.all()

    if not aichi_target_id:
        target = None
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
                'current_goal': current_goal,
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
