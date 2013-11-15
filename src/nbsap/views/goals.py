import json
from cStringIO import StringIO

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import Template, context, RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.contrib import messages

from nbsap import models
from indicators import get_indicators_pages
from auth import auth_required
from nbsap.forms import AichiGoalForm


def goals(request, code):
    current_goal = get_object_or_404(models.AichiGoal, code=code)
    goals = models.AichiGoal.objects.order_by('code').all()
    indicators_list = models.AichiIndicator.objects.all()

    paginator = Paginator(indicators_list, 20)

    return render_to_response('goals.html',
                              context_instance=RequestContext(request, {
                                'goals': goals,
                                'current_goal': current_goal,
                                'indicators_pages': get_indicators_pages(paginator),
                              })
    )


def eu_target_nat_strategy_export_preview(request, target_id):
    target = get_object_or_404(models.AichiTarget, pk=target_id)
    return render(request, 'objectives/nat_strategy_export_preview.html', {
        'target': target,
    })


def eu_target_nat_strategy_export(request, target_id):
    target = get_object_or_404(models.AichiTarget, pk=target_id)
    template = 'objectives/nat_strategy_export_preview.html'
    contents = StringIO(render_to_string(template, {
        'target': target, 'download': True
    }))
    resp = HttpResponse(contents.getvalue(), content_type='application/msword')
    resp['Content-Disposition'] = 'attachment; filename=nat_strategy.doc'
    return resp


def get_goal_title(request, pk=None):
    if not pk:
        return HttpResponse('Goal not found')

    goal = get_object_or_404(models.AichiGoal, pk=pk)
    targets = [{'pk': target.pk, 'value': target.pk} for target in goal.targets.all()]

    return HttpResponse(json.dumps([{'goal':goal.description,'targets':targets}]))

def get_aichi_target_title(request, pk=None):
    if not pk:
        return HttpResponse('Aichi target not found')

    target = get_object_or_404(models.AichiTarget, pk=pk)
    return HttpResponse(json.dumps([{'code': target.code, 'value':target.description}]))


@auth_required
def edit_goal(request, code=None):
    goal = get_object_or_404(models.AichiGoal, pk=code)

    lang = request.GET.get('lang', request.LANGUAGE_CODE)

    if request.method == 'POST':
        form = AichiGoalForm(request.POST, goal=goal, lang=lang)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved changes.')
            return redirect('list_goals')
        else:
            form = None
    else:
        form = AichiGoalForm(goal=goal, lang=lang)

    return render(request, 'goals/edit_goals.html',
                  {'form': form,
                   'goal': goal,
                   'lang': lang,
                  })

@auth_required
def list_goals(request):
    goals = models.AichiGoal.objects.all()

    return render(request, 'goals/list_goals.html',
                  {'goals': goals,
                  })
