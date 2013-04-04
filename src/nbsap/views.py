from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from nbsap import models

def get_indicators_pages(paginator):

    indicators_pages = {}
    for i in paginator.page_range:
      indicators_pages[i] = '{0} to {1}'.format(
                            paginator.page(i).start_index(),
                            paginator.page(i).end_index())
    return indicators_pages


def goals(request, code):
    current_goal = get_object_or_404(models.AichiGoal, code=code)
    goals = models.AichiGoal.objects.order_by('code').all()
    indicators_list = models.AichiIndicator.objects.all()

    paginator = Paginator(indicators_list, 20)

    return render(request, 'goals.html',
                  {'goals': goals,
                   'current_goal': current_goal,
                   'indicators_pages': get_indicators_pages(paginator),
                  })


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

    return render(request, 'indicators.html',
                  {'goals': goals,
                   'indicators_pages': get_indicators_pages(paginator),
                   'indicators': indicators,
                   'page': int(page),
                  })


def eu_targets(request, pk):
    current_target = get_object_or_404(models.EuTarget, pk=pk)
    targets = models.EuTarget.objects.all()

    current_target.actions_tree = []
    for action in current_target.actions.all():
        current_target.actions_tree.extend(action.get_all_actions())

    return render(request, 'eu_targets.html',
                  {'targets': targets,
                   'current_target': current_target,
                  })


def national_strategy(request):
    return HttpResponse("national_strategy")


def implementation(request):
    return HttpResponse("implementation")
