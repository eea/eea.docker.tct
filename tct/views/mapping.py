from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from tct import models
from tct.forms import NationalStrategyForm, EuAichiStrategyForm

from auth import auth_required


@auth_required
def edit_national_strategy(request, pk=None):
    if pk:
        strategy = get_object_or_404(models.NationalStrategy, pk=pk)
        template = 'manager/nat_strategy/mapping/edit_national_strategy.html'
    else:
        strategy = None
        template = 'manager/nat_strategy/mapping/add_national_strategy.html'

    if request.method == 'POST':
        form = NationalStrategyForm(request.POST, strategy=strategy)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request, _(
                    'Mapping successfully added.') + "")
            return redirect('list_national_strategy')
    else:
        form = NationalStrategyForm(strategy=strategy)
    return render(request, template, {'form': form, 'strategy': strategy})


@auth_required
def delete_national_strategy(request, strategy=None):
    strategy = get_object_or_404(models.NationalStrategy, pk=strategy)
    strategy.delete()
    messages.success(request, _('Mapping successfully deleted.') + "")
    return redirect('list_national_strategy')


@auth_required
def list_national_strategy(request):
    strategies = models.NationalStrategy.objects.all()
    return render(request,
                  'manager/nat_strategy/mapping/list_national_strategy.html',
                  {'strategies': strategies})


@auth_required
def list_eu_aichi_strategy(request):
    strategies = models.EuAichiStrategy.objects.all()
    return render(request,
                  'manager/eu_strategy/mapping/list_eu_aichi_strategy.html', {
                      'strategies': strategies
                  })


@auth_required
def edit_eu_aichi_strategy(request, pk=None):
    if pk:
        strategy = get_object_or_404(models.EuAichiStrategy, pk=pk)
        template = 'manager/eu_strategy/mapping/edit_eu_aichi_strategy.html'
    else:
        strategy = None
        template = 'manager/eu_strategy/mapping/add_eu_aichi_strategy.html'

    if request.method == 'POST':
        form = EuAichiStrategyForm(request.POST, strategy=strategy)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes'))
            else:
                messages.success(request, _('Mapping successfully added.'))
            return redirect('list_eu_aichi_strategy')
    else:
        form = EuAichiStrategyForm(strategy=strategy)
    return render(request, template, {'form': form, 'strategy': strategy})


@auth_required
def delete_eu_aichi_strategy(request, pk=None):
    if request.method == 'POST':
        strategy = get_object_or_404(models.EuAichiStrategy, pk=pk)
        strategy.delete()
        messages.success(request, _('Mapping successfully deleted.'))
        return redirect('list_eu_aichi_strategy')
