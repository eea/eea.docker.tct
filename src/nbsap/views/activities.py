from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from nbsap import models
from nbsap.forms import EuStrategyActivityForm, EuStrategyActivityEditForm

from auth import auth_required


@auth_required
def view_eu_strategy_activity(request, target, pk):
    target = get_object_or_404(models.EuTarget, pk=target)
    activity = get_object_or_404(models.EuAction, pk=pk)
    return render(request, 'manager/activities/view_eu_strategy_target.html', {
        'target': target,
        'activity': activity,
    })


@auth_required
def edit_eu_strategy_activity(request, target, pk=None, parent=None):
    target = get_object_or_404(models.EuTarget, pk=target)

    if pk:
        activity = get_object_or_404(models.EuAction, pk=pk)
        template = 'manager/activities/edit_eu_strategy_activity.html'
        FormClass = EuStrategyActivityEditForm
    else:
        activity = None
        template = 'manager/activities/add_eu_strategy_activity.html'
        FormClass = EuStrategyActivityForm

    if parent:
        parent = get_object_or_404(models.EuAction, pk=parent)
    else:
        parent = activity and activity.parent

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = FormClass(
            request.POST, activity=activity, target=target, parent=parent,
        )
        if form.is_valid():
            form.save()
            if not pk:
                messages.success(request,
                                 _('Activity successfully added.') + "")
            else:
                messages.success(request, _('Saved changes.') + "")
            if activity:
                return redirect('view_eu_strategy_activity', target=target.pk,
                                pk=activity.pk)
            else:
                return redirect('view_eu_strategy_target', pk=target.pk)
    else:
        form = FormClass(
            activity=activity, target=target, lang=lang, parent=parent
        )

    return render(request, template, {
        'form': form,
        'activity': activity,
        'target': target,
        'lang': lang,
    })


@auth_required
def delete_eu_strategy_activity(request, target, pk=None):
    if request.method == 'POST':
        activity = get_object_or_404(models.EuAction, pk=pk)
        activity.delete()
        messages.success(request, _('Activity successfully deleted.') + "")
        return redirect('view_eu_strategy_target', pk=target)
