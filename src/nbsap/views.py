from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict 

from nbsap import models
from nbsap.forms import NationalObjectiveForm

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


def nat_strategy(request, pk):
    current_objective = get_object_or_404(models.NationalObjective, pk=pk)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.objectives_tree = current_objective.get_all_objectives()

    return render(request, 'nat_strategy.html',
                  {'objectives': objectives,
                   'current_objective': current_objective,
                  })


def implementation(request):
    return HttpResponse("implementation")


def list_national_objectives(request):
    objectives = models.NationalObjective.objects.filter(parent=None).all()
    return render(request, 'list_national_objectives.html',
                  {'objectives': objectives,
                  })

def view_national_objective(request, code):
    objective = get_object_or_404(models.NationalObjective, code=code)
    return render(request, 'view_national_objective.html',
                  {'objective': objective,
                  })

def edit_national_objective(request, code=None, parent=None):
    if parent:
        parent_objective = get_object_or_404(models.NationalObjective, code=parent)
    else:
        parent_objective = None

    if code:
        objective = get_object_or_404(models.NationalObjective, code=code)
        template = 'edit_national_objective.html'
    else:
        objective = None
        template = 'add_national_objectives.html'

    lang = request.GET.get('lang', 'en')

    if request.method == 'POST':
        form = NationalObjectiveForm(request.POST,
                                     objective=objective,
                                     parent_objective=parent_objective)
        if form.is_valid():
            form.save()
    else:
        form = NationalObjectiveForm(objective=objective, lang=lang)
    return render(request, template,
                  {'form': form,
                   'objective': objective,
                   'lang': lang,
                  })
