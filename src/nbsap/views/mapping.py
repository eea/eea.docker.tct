from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response

from nbsap import models
from nbsap.forms import NationalStrategyForm


@login_required
def edit_national_strategy(request, pk=None):
    if pk:
        strategy = get_object_or_404(models.NationalStrategy, pk=pk)
        template = 'mapping/edit_national_strategy.html'
    else:
        strategy = None
        template = 'mapping/add_national_strategy.html'

    if request.method == 'POST':
        form = NationalStrategyForm(request.POST,
                                    strategy=strategy)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, 'Saved changes')
            else:
                messages.success(request, 'Objects succesfuly added.')
            return redirect('list_national_strategy')
    else:
        form = NationalStrategyForm(strategy=strategy)
    return render_to_response(template,
                              context_instance=RequestContext(request, {
                                'form': form,
                                'strategy': strategy,
                              })
    )


@login_required
def delete_national_strategy(request, strategy=None):
    strategy = get_object_or_404(models.NationalStrategy, pk=strategy)
    strategy.delete()
    messages.success(request, 'Mapping successfully deleted.')
    return redirect('list_national_strategy')


@login_required
def list_national_strategy(request):
    strategies = models.NationalStrategy.objects.all()

    return render_to_response('mapping/list_national_strategy.html',
                              context_instance=RequestContext(request, {
                                'strategies': strategies,
                                })
    )
