from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

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
