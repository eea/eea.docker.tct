from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from tct.forms import TCTPageForm
from tct.models import TCTPage, NationalStrategy

from auth import auth_required


@auth_required
def admin_export(request):
    resp = render(request, 'manager/bise_export.html',
                  {'strategies': NationalStrategy.objects.all()})
    content = resp.content
    return render(request, 'manager/export.html', {'content': content})


@auth_required
def admin_pages(request):
    pages = TCTPage.objects.all()
    return render(request, 'page/admin_pages.html', {'pages': pages})


@auth_required
def admin_page(request, handle):
    page = get_object_or_404(TCTPage, handle=handle)
    lang = request.GET.get('lang', request.LANGUAGE_CODE)
    if request.method == 'POST':
        form = TCTPageForm(request.POST, page=page, lang=lang)
        if form.is_valid():
            form.save()
            messages.success(request, _('Page %s saved') % handle)
    else:
        form = TCTPageForm(page=page, lang=lang)
    return render(request, 'page/admin_page.html',
                  {'page': page, 'form': form})


@auth_required
def admin_home(request):
    return render(request, 'layout-admin.html')
