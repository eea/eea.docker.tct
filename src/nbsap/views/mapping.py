from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from nbsap import models
from nbsap.forms import NationalObjectiveMappingForm

def nat_strategy(request, code):
    current_objective = get_object_or_404(models.NationalObjective, code=code)
    objectives = models.NationalObjective.objects.filter(parent=None).all()

    current_objective.objectives_tree = current_objective.get_all_objectives()

    return render(request, 'mapping/nat_strategy.html',
                  {'objectives': objectives,
                   'current_objective': current_objective,
                  })

@login_required
def edit_mapping(request, pk=None):
    if pk:
        strategy = get_object_or_404(models.NationalStrategy, pk=pk)
        template  = 'mapping/edit_mapping.html'
    else:
        strategy = None
        template = 'mapping/add_mapping.html'

    if request.method == 'POST':
        form = NationalObjectiveMappingForm(request.POST,
                                     strategy=strategy)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, 'Saved changes')
            else:
                messages.success(request, 'Objects succesfuly added.')
            return redirect('mapping_national_objectives')
    else:
        form = NationalObjectiveMappingForm(strategy=strategy)
    return render(request, template,
                  {'form': form,
                   'strategy': strategy,
                  })

@login_required
def delete_mapping(request, strategy=None):
    strategy = get_object_or_404(models.NationalStrategy, pk=strategy)
    strategy.delete()
    messages.success(request, 'Strategy successfully deleted.')
    return redirect('mapping_national_objectives')

@login_required
def mapping_national_objectives(request):
    strategies = models.NationalStrategy.objects.all()

    return render(request, 'mapping/admin_mapping.html',
                  {'strategies' : strategies,
                  })

