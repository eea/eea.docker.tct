from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from auth import auth_required
from nbsap import models


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
    return render(request, 'eu_indicators/indicator_details.html', {
        'indicator': indicator,
    })


def eu_indicators(request):
    indicators = models.EuIndicator.objects.exclude(targets=None).all()
    subindicators = models.EuIndicator.objects.filter(targets=None).all()
    return render(request, 'eu_indicators.html', {
        'indicators': indicators,
        'subindicators': subindicators,
    })


@auth_required
def list_eu_indicators(request):
    indicators = models.EuIndicator.objects.all()
    return render(request, 'eu_indicators/list_eu_indicators.html', {
        'indicators': indicators,
    })


@auth_required
def view_eu_indicator(request, pk):
    ind = get_object_or_404(models.EuIndicator, pk=pk)
    return render(request, 'eu_indicators/view_eu_indicator.html', {
        'indicator': ind,
    })
