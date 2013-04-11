from django.shortcuts import render, get_object_or_404

from nbsap import models

from indicators import get_indicators_pages


def implementation(request, code):
    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.actions_tree = []

    for objective in current_objective.get_all_objectives():
        for action in objective.actions.all():
            current_objective.actions_tree.append(action)
    return render(request, 'implementation.html',
                  {'current_objective': current_objective,
                   'objectives': objectives,
                  })
