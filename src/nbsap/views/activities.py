
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from nbsap import models
from nbsap.forms import EuStrategyActivityForm

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
def edit_eu_strategy_activity(request, target, pk=None):
    target = get_object_or_404(models.EuTarget, pk=target)

    if pk:
        activity = get_object_or_404(models.EuAction, pk=pk)
        template = 'manager/activities/edit_eu_strategy_activity.html'
    else:
        activity = None
        template = 'manager/activities/add_eu_strategy_activity.html'

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = EuStrategyActivityForm(request.POST,
                                      activity=activity,
                                      target=target)
        if form.is_valid():
            form.save()
            if not pk:
                messages.success(request,
                                 _('Activity successfully added.') + "")
            else:
                messages.success(request,  _('Saved changes.') + "")
            return redirect('view_eu_strategy_target', pk=target.pk)
    else:
        form = EuStrategyActivityForm(activity=activity,
                                      target=target,
                                      lang=lang)

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
