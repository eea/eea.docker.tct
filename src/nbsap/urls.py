from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # homepage URLs
    url(r'^$', 'nbsap.views.goals', {'code': 'a'}, name='goals'),
    url(r'^goals/(?P<code>[\w\-]+)$', 'nbsap.views.goals', name='goals'),

    url(r'^implementation$', 'nbsap.views.implementation', {'code' : '1'}, name='implementation'),
    url(r'^implementation/(?P<code>[\w\-]+)$', 'nbsap.views.implementation', name='implementation'),

    url(r'^eu_targets$', 'nbsap.views.eu_targets', {'code': '1'}, name='eu_targets'),
    url(r'^eu_targets/(?P<code>[\w\-]+)$', 'nbsap.views.eu_targets', name='eu_targets'),

    url(r'^indicators/$', 'nbsap.views.indicators', name='indicators'),

    url(r'^objectives$', 'nbsap.views.nat_strategy', name='nat_strategy'),
    url(r'^objectives/(?P<code>[\w\-]+)$', 'nbsap.views.nat_strategy', name='nat_strategy'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    # othe URLs
    url(r'^tinymce/', include('tinymce.urls')),

    # authentication URLs
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'nbsap.views.logout_view', name='logout'),

    # administration URLs
    url(r'^administration/objectives/$',
            'nbsap.views.list_national_objectives',
            name='list_national_objectives'),

    url(r'^administration/$',
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

    url(r'^administration/objectives/(?P<pk>[\w\-]+)/delete',
            'nbsap.views.delete_national_objective',
             name='delete_national_objective'),

    url(r'^administration/objectives/(?P<objective>[\w\-]+)/actions/add',
            'nbsap.views.edit_national_action',
             name='edit_national_action'),

    url(r'^administration/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/edit',
            'nbsap.views.edit_national_action',
            name='edit_national_action'),

    url(r'^administration/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/$',
            'nbsap.views.view_national_action',
            name='view_national_action'),

    url(r'^administration/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/delete',
            'nbsap.views.delete_national_action',
            name='delete_national_action'),

    url(r'^administration/mapping/$',
            'nbsap.views.mapping_national_objectives',
            name='mapping_national_objectives'),
)
