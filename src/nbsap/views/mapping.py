from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from nbsap import models


def nat_strategy(request, code):
    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.objectives_tree = current_objective.get_all_objectives()

    return render(request, 'mapping/nat_strategy.html',
                  {'objectives': objectives,
                   'current_objective': current_objective,
                  })


@login_required
def mapping_national_objectives(request):
    pass

