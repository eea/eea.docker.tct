from django.shortcuts import render
from django.http import HttpResponse

from nbsap import models


def goals(request, code):
    goals = models.AichiGoal.objects.order_by('code').all()
    return render(request, 'goals.html',
                  {'goals': goals,
                   'current_page': code})

def eu_strategy(request):
    return HttpResponse("eu_strategy")

def national_strategy(request):
    return HttpResponse("national_strategy")

def implementation(request):
    return HttpResponse("implementation")
