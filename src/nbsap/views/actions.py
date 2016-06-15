from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from nbsap import models
from nbsap.forms import NationalActionForm

from auth import auth_required


@auth_required
def view_national_action(request, objective, pk):
    objective = get_object_or_404(models.NationalObjective, pk=objective)
    action = get_object_or_404(models.NationalAction, pk=pk)
    actions = action.children.all().order_by('region', 'code')
    return render(
        request,
        'manager/actions/view_national_action.html',
        {'objective': objective, 'action': action, 'actions': actions}
    )


@auth_required
def edit_national_action(request, objective, pk=None, parent=None):
    objective = get_object_or_404(models.NationalObjective, pk=objective)
    if parent:
        parent_action = get_object_or_404(models.NationalAction, pk=parent)
    else:
        parent_action = None
    if pk:
        action = get_object_or_404(models.NationalAction, pk=pk)
        template = 'manager/actions/edit_national_action.html'
    else:
        action = None
        template = 'manager/actions/add_national_action.html'

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = NationalActionForm(request.POST, action=action,
                                  objective=objective,
                                  parent_action=parent_action)
        if form.is_valid():
            form.save()
            if not pk:
                messages.success(request, _('Action successfully added.') + "")
            else:
                messages.success(request, _('Saved changes.') + "")
            return redirect('view_national_objective', pk=objective.pk)
    else:
        form = NationalActionForm(action=action, objective=objective,
                                  lang=lang, parent_action=parent_action)

    return render(request, template, {
        'form': form,
        'action': action,
        'objective': objective,
        'lang': lang,
    })


@auth_required
def delete_national_action(request, objective, pk=None):
    if request.method == 'POST':
        action = get_object_or_404(models.NationalAction, pk=pk)
        action.delete()
        messages.success(request, _('Action successfully deleted.') + "")
        return redirect('view_national_objective', pk=objective)
