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

def eu_strategy(request):
    return HttpResponse("eu_strategy")

def national_strategy(request):
    return HttpResponse("national_strategy")

def implementation(request):
    return HttpResponse("implementation")
