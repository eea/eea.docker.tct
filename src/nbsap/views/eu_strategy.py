import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _


from nbsap import models
from auth import auth_required

from nbsap.forms import EuTargetForm, EuTargetEditForm, RegionForm


def eu_targets(request, pk=None):
    if pk:
        current_target = models.EuTarget.objects.get(pk=pk)
        current_target.actions_tree = []
        for action in current_target.actions.order_by('code'):
            current_target.actions_tree.extend(action.get_all_actions())
    else:
        current_target = None

    targets = models.EuTarget.objects.all()

    return render(request, 'eu_strategy/eu_targets.html',
                  {'targets': targets,
                   'current_target': current_target
                   })


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
                       for subaction in action.get_all_actions()])
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
                messages.success(request, _('Saved changes') + "")
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
        messages.success(request, _('Region successfully deleted.') + "")
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
                messages.success(request, _('Saved changes') + "")
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
        messages.success(request, _('Target successfully deleted.') + "")
        return redirect('list_eu_targets')
