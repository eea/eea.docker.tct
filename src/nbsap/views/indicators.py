from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from auth import auth_required
from nbsap import models
from nbsap.forms import EuIndicatorForm, EuIndicatorMapForm


def get_indicators_pages(paginator):

    indicators_pages = {}
    for i in paginator.page_range:
        indicators_pages[i] = _('%(start)s to %(end)s') % {
            'start': paginator.page(i).start_index(),
            'end': paginator.page(i).end_index()}
    return indicators_pages


def indicator(request, pk):
    indicator = get_object_or_404(models.AichiIndicator, pk=pk)
    indicator.relevant_target_ob = indicator.relevant_target.all()[0]
    indicator.strategic_goal_ob = indicator.relevant_target_ob.goals.all()[0]
    indicator.other_targets_list = indicator.other_targets.all()
    return render(request, 'nat_strategy/indicator_details.html', {
        'indicator': indicator,
    })


def eu_indicators(request):
    indicators = models.EuIndicator.objects.filter(parents=None).all()
    subindicators = models.EuIndicator.objects.exclude(parents=None).all()
    return render(request, 'eu_strategy/eu_indicators.html', {
        'indicators': indicators,
        'subindicators': subindicators,
    })


@auth_required
def list_eu_indicators(request):
    indicators = models.EuIndicator.objects.filter(
        parents=None).all().order_by('title_' + settings.LANGUAGE_CODE)
    return render(request, 'manager/eu_indicators/list_eu_indicators.html', {
        'indicators': indicators,
    })


@auth_required
def view_eu_indicator(request, pk):
    ind = get_object_or_404(models.EuIndicator, pk=pk)
    return render(request, 'manager/eu_indicators/view_eu_indicator.html', {
        'indicator': ind,
    })


@auth_required
def edit_eu_indicator(request, pk=None):
    if pk:
        indicator = get_object_or_404(models.EuIndicator, pk=pk)
        template = 'manager/eu_indicators/edit_eu_indicator.html'
    else:
        indicator = None
        template = 'manager/eu_indicators/add_eu_indicator.html'

    FormClass = EuIndicatorForm
    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = FormClass(request.POST, indicator=indicator)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request,
                                 _('Indicator successfully added.') + "")

            if not indicator:
                return redirect('list_eu_indicators')
            else:
                return redirect('view_eu_indicator', pk=indicator.pk)
    else:
        form = FormClass(indicator=indicator, lang=lang)
    return render(request, template, {
        'form': form,
        'indicator': indicator,
        'lang': lang,
    })


@auth_required
def delete_eu_indicator(request, pk):
    if request.method == 'POST':
        ind = get_object_or_404(models.EuIndicator, pk=pk)
        ind.delete()
        messages.success(request, _('Indicator successfully deleted.') + "")
        return redirect('list_eu_indicators')


@auth_required
def map_eu_indicator(request, pk):
    ind = get_object_or_404(models.EuIndicator, pk=pk)

    if request.method == 'POST':
        form = EuIndicatorMapForm(request.POST, indicator=ind)
        if form.is_valid():
            form.save()
            messages.success(request, _('Saved changes'))
            return redirect('view_eu_indicator', pk=pk)
    else:
        form = EuIndicatorMapForm(indicator=ind)

    return render(request, 'manager/eu_indicators/map_eu_indicator.html', {
        'form': form,
        'indicator': ind,
    })
