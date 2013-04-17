from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from nbsap import models
from nbsap.forms import NationalActionForm


@login_required
def view_national_action(request, objective, pk):
    objective = get_object_or_404(models.NationalObjective, pk=objective)
    action = get_object_or_404(models.NationalAction, pk=pk)
    return render(request, 'actions/view_national_action.html',
                  {'objective': objective,
                   'action': action,
                  })


@login_required
def edit_national_action(request, objective, pk=None):
    objective = get_object_or_404(models.NationalObjective, pk=objective)
    lang = request.GET.get('lang', 'en')

    if pk:
        action = get_object_or_404(models.NationalAction, pk=pk)
        template = 'actions/edit_national_action.html'
    else:
        action = None
        template = 'actions/add_national_action.html'

    if request.method == 'POST':
        form = NationalActionForm(request.POST,
                                  action=action,
                                  objective=objective)
        if form.is_valid():
            form.save()
            if template.split('_', 1)[0] == 'add':
                messages.success(request, 'Action successfully added.')
            elif template.split('_', 1)[0] == 'edit':
                messages.success(request, 'Saved changes.')
            return redirect('view_national_objective', pk=objective.pk)
    else:
        form = NationalActionForm(action=action,
                                  objective=objective,
                                  lang=lang)

    return render(request, template,
                  {'form': form,
                   'action': action,
                   'lang': lang,
                   'objective': objective,
                  })


@login_required
def delete_national_action(request, objective, pk=None):
    action = get_object_or_404(models.NationalAction, pk=pk)
    action.delete()
    messages.success(request, 'Action successfully deleted.')
    return redirect('view_national_objective', pk=objective)



