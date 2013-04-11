from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _

from nbsap import models


def get_indicators_pages(paginator):

    indicators_pages = {}
    for i in paginator.page_range:
      indicators_pages[i] = _('%(start)s to %(end)s') % {
                                'start': paginator.page(i).start_index(),
                                'end': paginator.page(i).end_index()}
    return indicators_pages


def indicators(request):

    goals = models.AichiGoal.objects.order_by('code').all()
    indicators_list = models.AichiIndicator.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(indicators_list, 20)

    try:
      indicators = paginator.page(page)
    except PageNotAnInteger:
      indicators = paginator.page(1)
    except EmptyPage:
      indicators = paginator.page(paginator.num_pages)

    for obj in indicators:
        obj.relevant_target_ob = obj.relevant_target.all()[0]
        obj.strategic_goal_ob = obj.relevant_target_ob.goals.all()[0]
        obj.other_targets_list = obj.other_targets.all()

    return render(request, 'indicators/indicators.html',
                  {'goals': goals,
                   'indicators_pages': get_indicators_pages(paginator),
                   'indicators': indicators,
                   'page': int(page),
                  })

