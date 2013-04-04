from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from nbsap import models


def goals(request, code):
    current_goal = get_object_or_404(models.AichiGoal, code=code)
    goals = models.AichiGoal.objects.order_by('code').all()
    return render(request, 'goals.html',
                  {'goals': goals,
                   'current_page': code,
                   'current_goal': current_goal,
                  })

def indicators(request):
    page = int(request.GET.get('page', 1))
    if page not in range(1, 6):
        page = 1

    # Use some math to generate the index intervals from the page number.
    start_index = lambda (x): 20 * x - 19

    # Render 20 indicators per page.
    start = start_index(page)
    end = start + 19

    goals = models.AichiGoal.objects.order_by('code').all()
    indicators = models.AichiIndicator.objects.all()[start:end]

    indicators_range = indicators[0].id + len(indicators) - 1

    for obj in indicators:
        obj.relevant_target_ob = obj.relevant_target.all()[0]
        obj.strategic_goal_ob = obj.relevant_target_ob.goals.all()[0]
        obj.other_targets_list = obj.other_targets.all()

    return render(request, 'indicators.html',
                  {'goals': goals,
                   'indicators': indicators,
                   'indicators_range': indicators_range,
                   'page': page,
                  })

def eu_strategy(request):
    return HttpResponse("eu_strategy")

def national_strategy(request):
    return HttpResponse("national_strategy")

def implementation(request):
    return HttpResponse("implementation")
