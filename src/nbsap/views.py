from django.shortcuts import render
from django.http import HttpResponse

from nbsap.models import AichiIndicator


def goals(request):
    context = {'indicators': AichiIndicator.objects.all()}
    return render(request, 'goals.html', context)

def eu_strategy(request):
    return HttpResponse("eu_strategy")

def national_strategy(request):
    return HttpResponse("national_strategy")

def implementation(request):
    return HttpResponse("implementation")
