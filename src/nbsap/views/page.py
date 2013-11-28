from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from nbsap.models import NbsapPage
from nbsap.forms import NbsapPageForm
from auth import auth_required


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
    return render(request, 'page/admin_page.html', {'page': page, 'form': form})
