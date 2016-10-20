from django.shortcuts import render, get_object_or_404
from django.http import Http404
from nbsap import models
from nbsap.utils import sort_by_code, get_adjacent_objects


def list_cms_goals(request):
    goals = models.CMSGoal.objects.order_by('code').all()
    return render(request, 'cms/cms.html', {
        'goals': goals,
        'list_goals': True,
    })


def list_cms_targets(request, code=None):
    if code:
        current_goal = get_object_or_404(models.CMSGoal, code=code)
        targets = current_goal.targets.all()
    else:
        current_goal = None
        targets = models.CMSTarget.objects.all()

    goals = models.CMSGoal.objects.order_by('code').all()
    return render(request, 'cms/cms.html', {
        'current_goal': current_goal,
        'goals': goals,
        'list_targets': True,
        'targets': targets,
    })


def cms_target_detail(request, cms_target_id, code=None):
    target = get_object_or_404(models.CMSTarget, pk=cms_target_id)
    target.related_targets = target.aichi_targets.all()

    if not code:
        code = target.get_parent_goal().code

    goals = models.CMSGoal.objects.order_by('code').all()
    current_goal = get_object_or_404(models.CMSGoal, code=code)
    all_targets = sort_by_code(models.CMSTarget.objects.all())
    targets = sort_by_code(current_goal.targets.all())

    if target not in targets:
        raise Http404

    previous_target, next_target = get_adjacent_objects(all_targets, target)

    return render(request, 'cms/cms.html', {
        'goals': goals,
        'targets': targets,
        'all_targets': all_targets,
        'target': target,
        'previous_target': previous_target,
        'next_target': next_target,
    })
