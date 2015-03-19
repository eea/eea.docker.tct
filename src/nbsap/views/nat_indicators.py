from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from auth import auth_required
from nbsap import models
from nbsap.forms import (
    EuIndicatorForm, EuIndicatorEditForm, EuIndicatorMapForm,
    NationalIndicatorEditForm, NationalIndicatorForm,
    NationalIndicatorMapForm
)


def nat_indicators(request):
    indicators = models.NationalIndicator.objects.filter(parents=None).all()
    return render(request, 'nat_strategy/nat_indicators.html', {
        'indicators': indicators,
    })


@auth_required
def list_nat_indicators(request):
    indicators = models.NationalIndicator.objects.filter(parents=None).all()
    return render(request, 'manager/nat_indicators/list_nat_indicators.html', {
        'indicators': indicators,
    })


@auth_required
def view_nat_indicator(request, pk):
    ind = get_object_or_404(models.NationalIndicator, pk=pk)
    return render(request, 'manager/nat_indicators/view_nat_indicator.html', {
        'indicator': ind,
    })


@auth_required
def edit_nat_indicator(request, pk=None):
    if pk:
        indicator = get_object_or_404(models.NationalIndicator, pk=pk)
        print indicator
        template = 'manager/nat_indicators/edit_nat_indicator.html'
        form_cls = NationalIndicatorEditForm
    else:
        indicator = None
        template = 'manager/nat_indicators/add_nat_indicator.html'
        form_cls = NationalIndicatorForm

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = form_cls(request.POST, indicator=indicator)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request,
                                 _('Indicator successfully added.') + "")

            if not indicator:
                return redirect('list_nat_indicators')
            else:
                return redirect('view_nat_indicator', pk=indicator.pk)
    else:
        form = form_cls(indicator=indicator, lang=lang)
    return render(request, template, {
        'form': form,
        'indicator': indicator,
        'lang': lang,
    })


@auth_required
def delete_nat_indicator(request, pk):
    if request.method == 'POST':
        ind = get_object_or_404(models.NationalIndicator, pk=pk)
        ind.delete()
        messages.success(request, _('Indicator successfully deleted.') + "")
        return redirect('list_nat_indicators')


@auth_required
def map_nat_indicator(request, pk):
    ind = get_object_or_404(models.NationalIndicator, pk=pk)

    if request.method == 'POST':
        form = NationalIndicatorMapForm(request.POST, indicator=ind)
        if form.is_valid():
            form.save()
            messages.success(request, _('Saved changes'))
            return redirect('view_nat_indicator', pk=pk)
    else:
        form = NationalIndicatorMapForm(indicator=ind)

    return render(request, 'manager/nat_indicators/map_nat_indicator.html', {
        'form': form,
        'indicator': ind,
    })
