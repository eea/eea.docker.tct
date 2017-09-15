from django import http
from django.template import TemplateDoesNotExist
from django.template import loader

from tct.context_processors import sentry


def handler500(request, template_name='errors/500.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>',
                                            content_type='text/html')

    return http.HttpResponseServerError(
        template.render(context=sentry(request)))
