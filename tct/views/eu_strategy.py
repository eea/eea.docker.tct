import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from tct import models
from tct.forms import EuTargetForm, EuTargetEditForm, RegionForm
from tct.utils import sort_by_code, get_adjacent_objects

from auth import auth_required


def get_most_relevant_aichi_targets(target):
    if not target:
        return []
    most_relevant_aichi_targets = []
    for strategy in target.eu_aichi_strategy.all():
        for aichi_target in strategy.aichi_targets.all():
            most_relevant_aichi_targets.append(aichi_target)
    return sort_by_code(list(set(most_relevant_aichi_targets)))


def get_other_relevant_aichi_targets(target):
    if not target:
        return []
    other_relevant_aichi_targets = []
    for strategy in target.eu_aichi_strategy.all():
        for aichi_target in strategy.other_aichi_targets.all():
            other_relevant_aichi_targets.append(aichi_target)
    return sort_by_code(other_relevant_aichi_targets)


def eu_target_detail(request, pk):
    current_target = get_object_or_404(models.EuTarget, pk=pk)
    current_target.actions_tree = []
    current_target.actions_tree = current_target.actions.order_by('code')

    current_target.most_relevant_aichi_targets = \
        get_most_relevant_aichi_targets(current_target)
    current_target.other_relevant_aichi_targets = \
        get_other_relevant_aichi_targets(current_target)

    targets = sort_by_code(
        models.EuTarget.objects.all().prefetch_related('parent'))
    previous_target, next_target = get_adjacent_objects(
        targets, current_target)

    return render(request, 'eu_strategy/eu_target_detail.html',
                  {'targets': targets,
                   'current_target': current_target,
                   'previous_target': previous_target,
                   'next_target': next_target
                   })


def eu_targets(request):
    targets = sort_by_code(models.EuTarget
                           .objects.select_related('parent').all())
    return render(request, 'eu_strategy/eu_targets.html',
                  {'targets': targets})


def get_eu_target_title(request, pk=None):
    if not pk:
        return HttpResponse('Eu target not found')

    target = get_object_or_404(models.EuTarget, pk=pk)
    return HttpResponse(json.dumps(
        [{'code': target.code, 'value': target.title}]))


def get_action_title(request, pk=None):
    if not pk:
        return HttpResponse('Action not found')

    action = get_object_or_404(models.EuAction, pk=pk)
    return HttpResponse(json.dumps([{'code': action.code,
                                     'value': action.description,
                                     'title': action.title}]))


def get_actions_for_target(request, pk=None):
    target = get_object_or_404(models.EuTarget, pk=pk)
    result = []
    for action in target.actions.all():
        result.extend([{'id': subaction.id,
                        'value': ' '.join(['Action', subaction.code])}
                       for subaction in action.get_actions()])
    return HttpResponse(json.dumps(result))


@auth_required
def list_eu_targets(request):
    targets = models.EuTarget.objects.filter(parent=None)
    return render(request, 'manager/eu_strategy/list_eu_targets.html', {
        'targets': targets,
    })


@auth_required
def list_regions(request):
    regions = models.Region.objects.all()
    return render(request, 'manager/eu_strategy/list_regions.html',
                  {'regions': regions})


@auth_required
def edit_region(request, pk=None):
    if pk:
        region = get_object_or_404(models.Region, pk=pk)
        template = 'manager/eu_strategy/edit_region.html'
    else:
        region = None
        template = 'manager/eu_strategy/add_region.html'

    FormClass = RegionForm
    if request.method == 'POST':
        form = FormClass(request.POST, region=region)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes'))
            else:
                messages.success(request, _('Region successfully added.'))
    else:
        form = FormClass(region=region)

    return render(request,
                  template,
                  {'region': region, 'form': form})


@auth_required
def delete_region(request, pk):
    if request.method == 'POST':
        region = get_object_or_404(models.Region, pk=pk)
        region.delete()
        messages.success(request, _('Region successfully deleted.'))
        return redirect('list_regions')


@auth_required
def view_eu_strategy_target(request, pk):
    target = get_object_or_404(models.EuTarget, pk=pk)
    actions = target.actions.filter(parent=None).order_by('region', 'code')
    return render(request,
                  'manager/eu_strategy/view_eu_strategy_target.html',
                  {'target': target, 'actions': actions})


@auth_required
def edit_eu_strategy_target(request, pk=None, parent=None):
    if parent:
        parent_target = get_object_or_404(models.EuTarget, pk=parent)
    else:
        parent_target = None

    if pk:
        target = get_object_or_404(models.EuTarget, pk=pk)
        template = 'manager/eu_strategy/edit_eu_strategy_targets.html'
        FormClass = EuTargetEditForm
    else:
        target = None
        template = 'manager/eu_strategy/add_eu_strategy_targets.html'
        FormClass = EuTargetForm

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = FormClass(
            request.POST, target=target, parent_target=parent_target)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes'))
            else:
                messages.success(request, _('Target successfully added.'))
            if target:
                return redirect('view_eu_strategy_target', pk=target.pk)
            else:
                return redirect('list_eu_targets')
    else:
        form = FormClass(target=target, lang=lang, parent_target=parent_target)
    return render(request, template, {
        'form': form,
        'target': target,
        'lang': lang,
    })


@auth_required
def delete_eu_strategy_target(request, pk):
    if request.method == 'POST':
        target = get_object_or_404(models.EuTarget, pk=pk)
        target.delete()
        messages.success(request, _('Target successfully deleted.'))
        return redirect('list_eu_targets')
