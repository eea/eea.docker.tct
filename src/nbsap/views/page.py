from django.shortcuts import render, get_object_or_404
from nbsap.models import NbsapPage
from nbsap.forms import NbsapPageForm


def admin_pages(request):
    pages = NbsapPage.objects.all()
    return render(request, 'page/admin_pages.html', {
        'pages': pages,
    })


def admin_page(request, handle):
    page = get_object_or_404(NbsapPage, handle=handle)
    lang = request.GET.get('lang', request.LANGUAGE_CODE)
    form = NbsapPageForm(page=page, lang=lang)
    return render(request, 'page/admin_page.html', {
        'page': page,
        'form': form,
    })
