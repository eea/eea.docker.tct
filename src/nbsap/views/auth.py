from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

from django.utils.translation import ugettext_lazy as _

def logout_view(request):
    messages.success(request, _("Successfully logged out") + "")
    logout(request)
    return redirect('goals')
