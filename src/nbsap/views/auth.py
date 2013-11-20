from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import login
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from functools import wraps


def logout_view(request):
    messages.success(request, _("Successfully logged out") + "")
    logout(request)
    return redirect('goals')


def login_view(request, *args, **kwargs):
    response = login(request, *args, **kwargs)
    if request.user.is_authenticated():
        messages.success(request, _("Successfully logged in") + "")
    return response


def stuff_test(user):
    return user.is_staff


def auth_required(view):
    """
    Decorator for views to check that the user is both logged in and
    also a staff member. Login required Django decorator checks only
    that the user is authenticated. So we've added an auxiliary
    'is_staff' condition through the user_pass_test Djangodecorator
    """
    @wraps(view)
    @user_passes_test(stuff_test)
    @login_required
    def wrapper(*args, **kwargs):
        return view(*args, **kwargs)

    return wrapper

def crashme(request):
    if request.user.is_superuser:
        raise RuntimeError("Crashing as requested")
    else:
        return HttpResponse("Must be administrator")
