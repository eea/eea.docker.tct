import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _


from nbsap import models
from auth import auth_required

from nbsap.forms import EuTargetForm, EuTargetEditForm


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
    return HttpResponse(json.dumps(
        [{'code': target.code, 'value': target.title}]))


def get_action_title(request, pk=None):
    if not pk:
        return HttpResponse('Action not found')

    action = get_object_or_404(models.EuAction, pk=pk)
    return HttpResponse(json.dumps(
        [{'code': action.code, 'value': action.description}]))


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
    targets = models.EuTarget.objects.all()
    return render(request, 'eu_strategy/list_eu_targets.html', {
        'targets': targets,
    })


@auth_required
def view_eu_strategy_target(request, pk):
    target = get_object_or_404(models.EuTarget, pk=pk)
    return render(request, 'eu_strategy/view_eu_strategy_target.html', {
        'target': target,
    })


@auth_required
def edit_eu_strategy_target(request, pk=None):
    if pk:
        target = get_object_or_404(models.EuTarget, pk=pk)
        template = 'eu_strategy/edit_eu_strategy_targets.html'
        FormClass = EuTargetEditForm
    else:
        target = None
        template = 'eu_strategy/add_eu_strategy_targets.html'
        FormClass = EuTargetForm

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = FormClass(request.POST, target=target)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request,
                                 _('Objective successfully added.') + "")

            return redirect('list_eu_targets')
    else:
        form = FormClass(target=target, lang=lang)
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
