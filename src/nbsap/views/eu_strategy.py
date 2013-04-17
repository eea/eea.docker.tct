from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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

def get_eu_target_title(request, pk=None):
    if not pk:
        return HttpResponse('Eu target not found')

    target = get_object_or_404(models.EuTarget, pk=pk)
    return HttpResponse("Target %s: %s" % (target.code, target.title))

def get_action_title(request, pk=None):
    if not pk:
        return HttpResponse('Action not found')

    action = get_object_or_404(models.EuAction, pk=pk)
    return HttpResponse('<h5>Action %s:</h5>%s' % (action.code, action.description))

def get_actions_for_target(request, pk=None):
    target = get_object_or_404(models.EuTarget, pk=pk)
    result = []
    for action in target.actions.all():
        result.extend([{'id': subaction.id,
                        'value': ' '.join(['Action', subaction.code])}
                            for subaction in action.get_all_actions()])

    import json
    return HttpResponse(json.dumps(result))
