from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'nbsap.views.goals', {'code': 'a'}, name='goals'),
    url(r'^goals/(?P<code>[\w\-]+)$', 'nbsap.views.goals', name='goals'),
    url(r'^national_strategy$', 'nbsap.views.national_strategy', name='national_strategy'),
    url(r'^implementation$', 'nbsap.views.implementation', name='implementation'),

    url(r'^eu_targets$', 'nbsap.views.eu_targets', {'pk': '1'}, name='eu_targets'),
    url(r'^eu_targets/(?P<pk>[\w\-]+)$', 'nbsap.views.eu_targets', name='eu_targets'),

    url(r'^indicators/$', 'nbsap.views.indicators', name='indicators'),

    url(r'^admin/', include(admin.site.urls)),
)
