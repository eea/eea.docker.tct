from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import json
import tablib

from nbsap import models
from nbsap.forms import NationalObjectiveForm, NationalObjectiveEditForm
from nbsap.utils import remove_tags

from auth import auth_required


def nat_strategy(request, code=None):
    objectives = (
        models.NationalObjective.objects
        .filter(parent=None).order_by('id').all()
    )
    if not objectives.exists():
        return render(request, 'objectives/empty_nat_strategy.html')
    code = code or objectives[0].code
    current_objective = models.NationalObjective.objects.get(code=code)

    obj_actions = []
    current_objective.objectives_tree = current_objective.get_all_objectives()
    actions = [i for i in current_objective.actions.all()]
    if actions:
        obj_actions.append({current_objective: actions})

    for subobj in current_objective.objectives_tree:
        actions = [i for i in subobj.actions.all()]
        if actions:
            obj_actions.append({subobj: actions})

    return render(request, 'objectives/nat_strategy.html',
                  {'objectives': objectives,
                   'current_objective': current_objective,
                   'actions_by_objectives': obj_actions})


def nat_strategy_download(request):
    eu_strategy = settings.EU_STRATEGY
    headers = ['Title', 'Subtitle', 'Objective', 'Aichi Goal', 'Most Relevant Aichi Targets',
               'Other Relevant Aichi Targets', 'Objective description']
    if eu_strategy:
        headers.extend(['EU Targets', 'EU Actions'])
    data = tablib.Dataset(headers=headers)
    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    for strategy in models.NationalStrategy.objects.all():
        if strategy.objective.children.count():
            objectives = strategy.objective.children.all()
            title = strategy.objective.title
        else:
            objectives = (strategy.objective,)
            title = None
        for objective in objectives:
            row = [
                objective.title if title is None else title,
                objective.title if title is not None else '',
                objective.code,
                ', '.join(g.code for g in strategy.goals_list) or '',
                ', '.join(t.code for t in strategy.relevant_targets.all()) or '',
                ', '.join(t.code for t in strategy.other_targets.all()),
                remove_tags(getattr(strategy.objective,
                                    'description_' + lang).rstrip(), 'p'),
            ]
            if eu_strategy:
                row.extend([
                    ', '.join(t.code for t in strategy.eu_targets.all()),
                    ', '.join(t.code for t in strategy.eu_actions.all()),
                ])
        data.append(row)

    response = HttpResponse(
        data.xlsx,
        content_type='application/vnd.openxmlformats-officedocument'
                     '.spreadsheetml.sheet;charset=utf-8'
    )
    response['Content-Disposition'] = "attachment; filename=objectives.xlsx"
    return response


def implementation(request, code=None):
    objectives = models.NationalObjective.objects.all()
    if len(objectives) == 0:
        return render(request, 'objectives/empty_nat_strategy.html')

    if code is None:
        code = objectives[0].code

    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.objectives_tree = current_objective.get_all_objectives()

    current_objective.actions_tree = list(current_objective.actions.all())
    for objective in current_objective.get_all_objectives():
        for action in objective.actions.all():
            current_objective.actions_tree.append(action)

    lang = request.LANGUAGE_CODE
    data = {'body_%s' % lang: ''}
    is_empty_page = models.NbsapPage.objects.filter(handle='implementation') \
        .exclude(**data).exists()
    return render(request, 'nat_strategy/implementation.html', {
        'current_objective': current_objective,
        'objectives': objectives,
        'is_empty_page': is_empty_page,
    })


def implementation_page(request):
    page = get_object_or_404(models.NbsapPage, handle='implementation')
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'nat_strategy/implementation_page.html', {
        'is_empty_page': True,
        'page': page,
        'objectives': objectives,
    })


@auth_required
def view_national_objective(request, pk):
    objective = get_object_or_404(models.NationalObjective, pk=pk)
    return render(request, 'manager/objectives/view_national_objective.html',
                  {'objective': objective})


@auth_required
def list_national_objectives(request):
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'manager/objectives/list_national_objectives.html',
                  {'objectives': objectives})


@auth_required
def edit_national_objective(request, pk=None, parent=None):
    if parent:
        parent_objective = get_object_or_404(models.NationalObjective,
                                             pk=parent)
    else:
        parent_objective = None

    if pk:
        objective = get_object_or_404(models.NationalObjective, pk=pk)
        template = 'manager/objectives/edit_national_objective.html'
        FormClass = NationalObjectiveEditForm
    else:
        objective = None
        template = 'manager/objectives/add_national_objectives.html'
        FormClass = NationalObjectiveForm

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = FormClass(request.POST, objective=objective,
                         parent_objective=parent_objective)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request,
                                 _('Objective successfully added.') + "")

            if parent_objective:
                return redirect('view_national_objective',
                                pk=parent_objective.pk)
            elif objective:
                return redirect('view_national_objective',
                                pk=objective.pk)
            else:
                return redirect('list_national_objectives')
    else:
        form = FormClass(objective=objective, lang=lang)
    return render(request, template, {
        'form': form,
        'objective': objective,
        'parent': parent_objective,
        'lang': lang,
    })


@auth_required
def delete_national_objective(request, pk):
    if request.method == 'POST':
        objective = get_object_or_404(models.NationalObjective, pk=pk)
        parent = objective.parent
        objective.delete()
        messages.success(request, _('Objective successfully deleted.') + "")
        if parent:
            return redirect('view_national_objective', pk=parent.pk)
        else:
            return redirect('list_national_objectives')


def get_national_objective_title(request, pk=None):
    if not pk:
        return HttpResponse('Object not found')

    objective = get_object_or_404(models.NationalObjective, pk=pk)
    return HttpResponse(json.dumps([
        {'code': objective.code, 'value': objective.title}]))
