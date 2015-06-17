from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings
from nbsap.models import NbsapPage, NationalStrategy
from nbsap.forms import NbsapPageForm
from auth import auth_required


@auth_required
def admin_export(request):
    resp = render(request, 'manager/bise_export.html',
                  {'strategies': NationalStrategy.objects.all()})
    content = resp.content
    return render(request, 'manager/export.html', {'content': content})


@auth_required
def admin_pages(request):
    pages = NbsapPage.objects.all()
    return render(request, 'page/admin_pages.html', {'pages': pages})


@auth_required
def admin_page(request, handle):
    page = get_object_or_404(NbsapPage, handle=handle)
    lang = request.GET.get('lang', request.LANGUAGE_CODE)
    if request.method == 'POST':
        form = NbsapPageForm(request.POST, page=page, lang=lang)
        if form.is_valid():
            form.save()
            messages.success(request, _('Page %s saved') % handle)
    else:
        form = NbsapPageForm(page=page, lang=lang)
    return render(request, 'page/admin_page.html',
                  {'page': page, 'form': form})


@auth_required
def admin_home(request):
    if settings.NAT_STRATEGY:
        return redirect('list_national_objectives')
    return redirect('list_eu_targets')
