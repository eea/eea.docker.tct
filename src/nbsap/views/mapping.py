from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _

from nbsap import models
from nbsap.forms import NationalStrategyForm

from auth import auth_required


@auth_required
def edit_national_strategy(request, pk=None):
    if pk:
        strategy = get_object_or_404(models.NationalStrategy, pk=pk)
        template = 'mapping/edit_national_strategy.html'
    else:
        strategy = None
        template = 'mapping/add_national_strategy.html'

    if request.method == 'POST':
        form = NationalStrategyForm(request.POST, strategy=strategy)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, _('Saved changes') + "")
            else:
                messages.success(request, _('Mapping successfully added.') + "")
            return redirect('list_national_strategy')

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
    return render(request, 'mapping/list_national_strategy.html',{
        'strategies': strategies
    })
