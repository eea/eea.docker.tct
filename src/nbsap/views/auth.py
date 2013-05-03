from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from functools import wraps

def logout_view(request):
    logout(request)
    return redirect('goals')


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
