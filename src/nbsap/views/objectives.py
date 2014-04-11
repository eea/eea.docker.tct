from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from transmeta import TransMeta
import tablib

from nbsap import models
from nbsap.forms import NationalObjectiveForm, NationalObjectiveEditForm

from auth import auth_required

def nat_strategy(request, code=None):

    objectives = models.NationalObjective.objects.all()
    if len(objectives) == 0:
        return render(request, 'objectives/empty_nat_strategy.html')

    if code is None:
        code = objectives[0].code

    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).order_by('id').all()

    current_objective.objectives_tree = current_objective.get_all_objectives()
    actions = [i for i in current_objective.actions.all()]
    for subobj in current_objective.objectives_tree:
        actions.extend([i for i in subobj.actions.all()])

    return render(request, 'objectives/nat_strategy.html',
                  {'objectives': objectives,
                   'current_objective': current_objective,
                   'actions': actions,})


def nat_strategy_download(request):
    eu_strategy = getattr(settings, 'EU_STRATEGY', False)
    headers = ['Objective', 'Goal', 'Most Relevant Targets',
               'Other Relevant Targets']
    if eu_strategy:
        headers.extend(['EU Targets', 'EU Actions'])
    data = tablib.Dataset(headers=headers)

    for strategy in models.NationalStrategy.objects.all():
        target = strategy.relevant_target
        row = [
            strategy.objective.code,
            target.get_parent_goal().code,
            target.code,
            ', '.join(t.code for t in strategy.other_targets.all()),
        ]
        if eu_strategy:
            row.extend([
                ', '.join(t.code for t in strategy.eu_targets.all()),
                ', '.join(t.code for t in strategy.eu_actions.all()),
            ])
        data.append(row)

    return HttpResponse(data.xlsx, content_type='application/vnd.ms-excel')


def implementation(request, code=None):
    objectives = models.NationalObjective.objects.all()
    if len(objectives) == 0:
        return render(request, 'objectives/empty_nat_strategy.html')

    if code is None:
        code = objectives[0].code

    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.actions_tree = list(current_objective.actions.all())
    for objective in current_objective.get_all_objectives():
        for action in objective.actions.all():
            current_objective.actions_tree.append(action)

    lang = request.LANGUAGE_CODE
    data = {'body_%s' % lang: ''}
    is_empty_page = models.NbsapPage.objects.filter(handle='implementation') \
                          .exclude(**data).exists()
    return render(request, 'implementation.html', {
        'current_objective': current_objective,
        'objectives': objectives,
        'is_empty_page': is_empty_page,
    })


def implementation_page(request):
    page = get_object_or_404(models.NbsapPage, handle='implementation')
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'implementation_page.html', {
        'is_empty_page': True,
        'page': page,
        'objectives': objectives,
    })


@auth_required
def view_national_objective(request, pk):
    objective = get_object_or_404(models.NationalObjective, pk=pk)
    return render(request, 'objectives/view_national_objective.html',
                  {'objective': objective,
                  })


@auth_required
def list_national_objectives(request):
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'objectives/list_national_objectives.html',{
        'objectives': objectives,
    })


@auth_required
def edit_national_objective(request, pk=None, parent=None):
    if parent:
        parent_objective = get_object_or_404(models.NationalObjective, pk=parent)
    else:
        parent_objective = None

    if pk:
        objective = get_object_or_404(models.NationalObjective, pk=pk)
        template = 'objectives/edit_national_objective.html'
        FormClass = NationalObjectiveEditForm
    else:
        objective = None
        template = 'objectives/add_national_objectives.html'
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
                 messages.success(request, _('Objective successfully added.') + "")

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
    return render(request, template,{
        'form': form,
        'objective': objective,
        'parent': parent_objective,
        'lang': lang,
    })


@auth_required
def delete_national_objective(request, pk):
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
    return HttpResponse('Objective ' + objective.code + ': ' + objective.title)
