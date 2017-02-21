from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render


class LoginRequiredMiddleware(object):
    def process_request(self, request):
        allowed_users = getattr(settings, 'ALLOWED_USERS', None)
        if not allowed_users:
            return
        if request.path in (reverse('login'), reverse('logout')):
            return
        if request.user.is_anonymous():
            return redirect('login')
        if request.user.username not in allowed_users:
            return render(request, 'registration/not_allowed.html')
