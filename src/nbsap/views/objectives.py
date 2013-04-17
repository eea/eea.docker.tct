from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from nbsap import models
from nbsap.forms import NationalObjectiveForm


@login_required
def view_national_objective(request, pk):
    objective = get_object_or_404(models.NationalObjective, pk=pk)
    return render(request, 'objectives/view_national_objective.html',
                  {'objective': objective,
                  })


@login_required
def list_national_objectives(request):
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'objectives/list_national_objectives.html',
                  {'objectives': objectives,
                  })


@login_required
def edit_national_objective(request, pk=None, parent=None):
    if parent:
        parent_objective = get_object_or_404(models.NationalObjective, pk=parent)
    else:
        parent_objective = None

    if pk:
        objective = get_object_or_404(models.NationalObjective, pk=pk)
        template = 'objectives/edit_national_objective.html'
    else:
        objective = None
        template = 'objectives/add_national_objectives.html'

    lang = request.GET.get('lang', 'en')

    if request.method == 'POST':
        form = NationalObjectiveForm(request.POST,
                                     objective=objective,
                                     parent_objective=parent_objective)
        if form.is_valid():
            form.save()
            if template.split('_', 1)[0] == 'add':
                messages.success(request, 'Objective successfully added.')
            elif template.split('_', 1)[0] == 'edit':
                messages.success(request, 'Saved changes.')

            if parent_objective:
                return redirect('view_national_objective',
                                pk=parent_objective.pk)
            else:
                return redirect('list_national_objectives')
    else:
        form = NationalObjectiveForm(objective=objective, lang=lang)


    return render(request, template,
                  {'form': form,
                   'objective': objective,
                   'lang': lang,
                   # used by add_national_objective.html Cancel button
                   'parent': parent_objective,
                  })


@login_required
def delete_national_objective(request, pk):
    objective = get_object_or_404(models.NationalObjective, pk=pk)
    parent = objective.parent
    objective.delete()
    messages.success(request, 'Objective successfully deleted.')

    if parent:
        return redirect('view_national_objective', pk=parent.pk)
    else:
        return redirect('list_national_objectives')

def get_national_objective_title(request, pk=None):
    if not pk:
        return HttpResponse('Object not found')

    objective = get_object_or_404(models.NationalObjective, pk=pk)
    return HttpResponse('Objective ' + objective.code + ': ' + objective.title)
