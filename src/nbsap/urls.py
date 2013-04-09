from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'nbsap.views.goals', {'code': 'a'}, name='goals'),
    url(r'^goals/(?P<code>[\w\-]+)$', 'nbsap.views.goals', name='goals'),
    
    url(r'^implementation$', 'nbsap.views.implementation', {'pk' : '1'}, name='implementation'),
    url(r'^implementation/(?P<pk>[\w\-]+)$', 'nbsap.views.implementation', name='implementation'),

    url(r'^eu_targets$', 'nbsap.views.eu_targets', {'pk': '1'}, name='eu_targets'),
    url(r'^eu_targets/(?P<pk>[\w\-]+)$', 'nbsap.views.eu_targets', name='eu_targets'),

    url(r'^indicators/$', 'nbsap.views.indicators', name='indicators'),

    url(r'^objectives$', 'nbsap.views.nat_strategy', {'pk': '1'}, name='nat_strategy'),
    url(r'^objectives/(?P<pk>[\w\-]+)$', 'nbsap.views.nat_strategy', name='nat_strategy'),

    url(r'^admin/', include(admin.site.urls)),

    # authentication URLs
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^administration/objectives/$',
            'nbsap.views.list_national_objectives',
            name='list_national_objectives'),

    url(r'^administration/objectives/(?P<pk>[\w\-]+)$',
            'nbsap.views.view_national_objective',
            name='view_national_objective'),

    url(r'^administration/objectives/(?P<pk>[\w\-]+)/edit$',
            'nbsap.views.edit_national_objective',
            name='edit_national_objective'),

    url(r'^administration/objectives/(?P<parent>[\w\-]+)/add$',
            'nbsap.views.edit_national_objective',
            name='edit_national_objective'),

    url(r'^administration/objectives/add/$',
            'nbsap.views.edit_national_objective',
             name='edit_national_objective'),

    url(r'^administration/mapping/$',
            'nbsap.views.mapping_national_objectives',
            name='mapping_national_objectives'),
)
