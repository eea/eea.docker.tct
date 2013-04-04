from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'nbsap.views.goals', {'code': 'a'}, name='goals'),
    url(r'^goals/(?P<code>[\w\-]+)$', 'nbsap.views.goals', name='goals'),
    url(r'^eu_strategy$', 'nbsap.views.eu_strategy', name='eu_strategy'),
    url(r'^national_strategy$', 'nbsap.views.national_strategy', name='national_strategy'),
    url(r'^implementation$', 'nbsap.views.implementation', name='implementation'),

    url(r'^indicators/$', 'nbsap.views.indicators', name='indicators'),

    url(r'^admin/', include(admin.site.urls)),
)
