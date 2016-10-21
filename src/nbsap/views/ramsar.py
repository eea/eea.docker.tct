from django.shortcuts import render, get_object_or_404
from django.http import Http404
from nbsap import models
from nbsap.utils import sort_by_code, get_adjacent_objects


def list_ramsar_goals(request):
    goals = models.RamsarGoal.objects.order_by('code').all()
    return render(request, 'ramsar/ramsar.html', {
        'goals': goals,
        'list_goals': True,
    })


def list_ramsar_targets(request, code=None):
    if code:
        current_goal = get_object_or_404(models.RamsarGoal, code=code)
        targets = current_goal.targets.all()
    else:
        current_goal = None
        targets = models.RamsarTarget.objects.all()

    goals = models.RamsarGoal.objects.order_by('code').all()
    return render(request, 'ramsar/ramsar.html', {
        'current_goal': current_goal,
        'goals': goals,
        'list_targets': True,
        'targets': targets,
    })


def ramsar_target_detail(request, ramsar_target_id, code=None):
    target = get_object_or_404(models.RamsarTarget, pk=ramsar_target_id)
    target.related_targets = target.aichi_targets.all()

    if not code:
        code = target.get_parent_goal().code

    goals = models.RamsarGoal.objects.order_by('code').all()
    current_goal = get_object_or_404(models.RamsarGoal, code=code)
    all_targets = sort_by_code(models.RamsarTarget.objects.all())
    targets = sort_by_code(current_goal.targets.all())

    if target not in targets:
        raise Http404

    previous_target, next_target = get_adjacent_objects(all_targets, target)

    return render(request, 'ramsar/ramsar.html', {
        'goals': goals,
        'targets': targets,
        'all_targets': all_targets,
        'target': target,
        'previous_target': previous_target,
        'next_target': next_target,
    })
