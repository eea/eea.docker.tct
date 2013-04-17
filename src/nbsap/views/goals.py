from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
import json

from nbsap import models

from indicators import get_indicators_pages


def goals(request, code):
    current_goal = get_object_or_404(models.AichiGoal, code=code)
    goals = models.AichiGoal.objects.order_by('code').all()
    indicators_list = models.AichiIndicator.objects.all()

    paginator = Paginator(indicators_list, 20)

    return render(request, 'goals.html',
                  {'goals': goals,
                   'current_goal': current_goal,
                   'indicators_pages': get_indicators_pages(paginator),
                  })


def get_goal_title(request, pk=None):
    if not pk:
        return HttpResponse('Goal not found')

    goal = get_object_or_404(models.AichiGoal, pk=pk)
    targets = [{'pk': target.pk, 'value': target.pk} for target in goal.targets.all()]

    return HttpResponse(json.dumps([{'goal':goal.description,'targets':targets}]))

def get_aichi_target_title(request, pk=None):
    if not pk:
        return HttpResponse('Aichi target not found')

    target = get_object_or_404(models.AichiTarget, pk=pk)
    return HttpResponse(json.dumps([{'code': target.code, 'value':target.description}]))


