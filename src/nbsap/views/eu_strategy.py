from django.shortcuts import render, get_object_or_404

from nbsap import models


def eu_targets(request, code):
    current_target = get_object_or_404(models.EuTarget, code=code)
    targets = models.EuTarget.objects.all()

    current_target.actions_tree = []
    for action in current_target.actions.all():
        current_target.actions_tree.extend(action.get_all_actions())

    return render(request, 'eu_targets.html',
                  {'targets': targets,
                   'current_target': current_target,
                  })


