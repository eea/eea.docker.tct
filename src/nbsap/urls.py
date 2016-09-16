from django.conf.urls import url, i18n, include
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.contrib import admin
from tinymce import urls as tinymce_urls
from . import views


admin.autodiscover()

urlpatterns = [
    # homepage URLs
    url(r'^$', views.user_homepage, name='user_homepage'),
    url(r'^aichi/goals/$', views.aichi_goals, name='list_goals'),
    url(r'^aichi/$', views.aichi_target_detail,
        {'code': 'a',
         'aichi_target_id': '1'},
        name='aichi_home'),
    url(r'^aichi/goals/(?P<code>[\w\-]+)/targets/$',
        views.list_targets,
        name='list_targets'),
    url(r'^aichi/targets/$', views.list_targets, name='list_targets'),
    url(r'^aichi/goals/targets/$', views.list_targets, name='list_targets'),
    url(r'^aichi/goals/(?P<code>[\w\-]+)$', views.list_targets, name='list_targets'),
    url(r'^aichi/goals/(?P<code>[\w\-]+)/targets/(?P<aichi_target_id>[\w\-]+)$',
        views.aichi_target_detail,
        name='goals'),
    url(r'^aichi/goals/targets/(?P<aichi_target_id>[\w\-]+)$',
        views.aichi_target_detail,
        name='aichi_target_detail'),
    url(r'^crashme$', views.crashme, name='crashme'),
    url(r'^ping/me$', views.pingme, name='pingme'),

    url(r'^national-strategy/implementation/$', views.implementation, name='implementation'),
    url(r'^national-strategy/implementation/intro$', views.implementation_page,
        name='implementation_page'),
    url(r'^national-strategy/implementation/(?P<code>((\d+\.)*\d+$))$',
        views.implementation, name='implementation'),

    url(r'^european-strategy/$', views.eu_targets, name='eu_targets'),
    url(r'^european-strategy/targets/$', views.eu_targets, name='eu_targets'),
    url(r'^european-strategy/targets/(?P<pk>(\d+))$',
        views.eu_target_detail, name='eu_target_detail'),

    url(r'^eu_targets/(?P<target_id>[\w\-]+)/objectives/export/preview/$',
        views.eu_target_nat_strategy_export_preview, name='nat_strategy_export_preview'),
    url(r'^eu_targets/(?P<target_id>[\w\-]+)/objectives/export/$',
        views.eu_target_nat_strategy_export, name='nat_strategy_export'),

    url(r'^indicator/(?P<pk>(\d+))$', views.indicator,
        name='indicator'),
    url(r'^european-strategy/indicators/$', views.eu_indicators,
        name='eu_indicators'),
    url(r'^european-strategy/indicators/(?P<pk>[\w\-]+)$', views.indicator_details,
        name='eu_indicator_details'),
    url(r'^national-strategy/indicators/$', views.nat_indicators,
        name='nat_indicators'),
    url(r'^national-strategy/indicators/(?P<pk>[\w\-]+)$', views.nat_indicator_detail,
        name='nat_indicator_detail'),

    url(r'^national-strategy/$', views.nat_strategy, name='nat_strategy'),
    url(r'^national-strategy/objectives$', views.nat_strategy, name='nat_strategy'),
    url(r'^download/xslx$', views.nat_strategy_download,
        name='nat_strategy_download'),
    url(r'^national-strategy/objectives/(?P<pk>[\w\-]+)$',
        views.nat_strategy, name='nat_strategy'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^send_to_cbd/(?P<model_name>[\w\-]+)/(?P<pk>(\d+))/$',
        views.send_to_cbd, name='send_to_cbd'),

    # Django generic view classes
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    # Disallow search engines to index data
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    # URLs for mapping form
    url(r'^goals/title$',
        views.get_goal_title,
        name='goal_title'),
    url(r'^goals/title/(?P<pk>[\w\-]+)$',
        views.get_goal_title,
        name='goal_title'),

    url(r'^actions/title$',
        views.get_action_title,
        name='action_title'),
    url(r'^actions/title/(?P<pk>[\w\-]+)$',
        views.get_action_title,
        name='action_title'),

    url(r'^eu_targets/title$',
        views.get_eu_target_title,
        name='eu_target_title'),
    url(r'^eu_targets/title/(?P<pk>[\w\-]+)$',
        views.get_eu_target_title,
        name='eu_target_title'),
    url(r'^eu_targets/actions/(?P<pk>[\w\-]+)$',
        views.get_actions_for_target,
        name='target_action'),

    url(r'^aichi_targets/title$',
        views.get_aichi_target_title,
        name='aichi_target_title'),
    url(r'^aichi_targets/title/(?P<pk>[\w\-]+)$',
        views.get_aichi_target_title,
        name='aichi_target_title'),

    url(r'^eu_indicator/title$',
        views.get_eu_indicator_title,
        name='eu_indicator_title'),
    url(r'^eu_indicator/title/(?P<pk>[\w\-]+)$',
        views.get_eu_indicator_title,
        name='eu_indicator_title'),

    # TODO
    url(r'^objectives/title$',
        views.get_national_objective_title,
        name='objective_title'),
    url(r'^objectives/title/(?P<pk>[\w\-]+)$',
        views.get_national_objective_title,
        name='objective_title'),

    # othe URLs
    url(r'^tinymce/', include('tinymce.urls')),

    # authentication URLs
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),

    # administration URLs
    url(r'^dashboard/$',
        views.admin_home,
        name='admin_home'),

    url(r'^dashboard/eu-strategy/$',
        views.list_eu_targets,
        name='list_eu_targets'),

    url(r'^dashboard/eu-strategy/targets/$',
        views.list_eu_targets,
        name='list_eu_targets'),

    url(r'^dashboard/eu-strategy/regions/$',
        views.list_regions,
        name='list_regions'),

    url(r'^dashboard/eu-strategy/regions/add/$',
        views.edit_region,
        name='add_region'),

    url(r'^dashboard/eu-strategy/regions/(?P<pk>[\w\-]+)/edit/$',
        views.edit_region,
        name='edit_region'),

    url(r'^dashboard/eu-strategy/regions/(?P<pk>\d+)/delete/$',
        views.delete_region,
        name='delete_region'),

    url(r'^dashboard/eu-strategy/targets/(?P<parent>[\w\-]+)/add$',
        views.edit_eu_strategy_target,
        name='edit_eu_target_with_parent'),

    url(r'^dashboard/eu-strategy/targets/add/',
        views.edit_eu_strategy_target,
        name='edit_eu_target'),

    url(r'^dashboard/eu-strategy/targets/(?P<pk>[\w\-]+)/$',
        views.view_eu_strategy_target,
        name='view_eu_strategy_target'),

    url(r'^dashboard/eu-strategy/targets/(?P<pk>[\w\-]+)/edit/$',
        views.edit_eu_strategy_target,
        name='edit_eu_strategy_target'),

    url(r'^dashboard/eu-strategy/targets/(?P<target>[\w\-]+)/activities/add/$',
        views.edit_eu_strategy_activity,
        name='edit_eu_strategy_activity'),

    url(r'^dashboard/eu-strategy/targets/(?P<target>[\w\-]+)/activities/add/(?P<parent>[\w\-]+)/$',
        views.edit_eu_strategy_activity,
        name='edit_eu_strategy_activity'),

    url(r'^dashboard/eu-strategy/targets/(?P<target>[\w\-]+)/activities/(?P<pk>[\w\-]+)/$',
        views.view_eu_strategy_activity,
        name='view_eu_strategy_activity'),

    url(r'^dashboard/eu-strategy/targets/(?P<target>[\w\-]+)/activities/(?P<pk>[\w\-]+)/edit/$',
        views.edit_eu_strategy_activity,
        name='edit_eu_strategy_activity'),

    url(r'^dashboard/eu-strategy/targets/(?P<target>[\w\-]+)/activities/(?P<pk>[\w\-]+)/delete/$',
        views.delete_eu_strategy_activity,
        name='delete_eu_strategy_activity'),

    url(r'^dashboard/eu-strategy/targets/(?P<pk>[\w\-]+)/delete/$',
        views.delete_eu_strategy_target,
        name='delete_eu_strategy_target'),

    url(r'^dashboard/eu-strategy/indicators/$',
        views.list_eu_indicators,
        name='list_eu_indicators'),

    url(r'^dashboard/eu-strategy/indicator/(?P<pk>\d+)/$',
        views.view_eu_indicator,
        name='view_eu_indicator'),

    url(r'^dashboard/eu-strategy/indicators/add/$',
        views.edit_eu_indicator,
        name='edit_eu_indicator'),

    url(r'^dashboard/eu-strategy/indicators/(?P<pk>\d+)/edit/$',
        views.edit_eu_indicator,
        name='edit_eu_indicator'),

    url(r'^dashboard/eu-strategy/indicators/(?P<pk>\d+)/delete/$',
        views.delete_eu_indicator,
        name='delete_eu_indicator'),

    url(r'^dashboard/eu-strategy/indicators/(?P<pk>\d+)/mapping/$',
        views.map_eu_indicator,
        name='map_eu_indicator'),

    url(r'^dashboard/nat-indicators/$',
        views.list_nat_indicators,
        name='list_nat_indicators'),

    url(r'^dashboard/nat-indicator/(?P<pk>\d+)/$',
        views.view_nat_indicator,
        name='view_nat_indicator'),

    url(r'^dashboard/nat-indicators/add/$',
        views.edit_nat_indicator,
        name='edit_nat_indicator'),

    url(r'^dashboard/nat-indicators/(?P<pk>\d+)/edit/$',
        views.edit_nat_indicator,
        name='edit_nat_indicator'),

    url(r'^dashboard/nat-indicators/(?P<pk>\d+)/delete/$',
        views.delete_nat_indicator,
        name='delete_nat_indicator'),

    url(r'^dashboard/nat-indicators/(?P<pk>\d+)/mapping/$',
        views.map_nat_indicator,
        name='map_nat_indicator'),

    url(r'^dashboard/objectives/$',
        views.list_national_objectives,
        name='list_national_objectives'),

    url(r'^dashboard/objectives/(?P<pk>[\w\-]+)$',
        views.view_national_objective,
        name='view_national_objective'),

    url(r'^dashboard/objectives/(?P<pk>[\w\-]+)/edit$',
        views.edit_national_objective,
        name='edit_national_objective'),

    url(r'^dashboard/objectives/(?P<parent>[\w\-]+)/add$',
        views.edit_national_objective,
        name='edit_national_objective'),

    url(r'^dashboard/objectives/add/$',
        views.edit_national_objective,
        name='edit_national_objective'),

    url(r'^dashboard/objectives/(?P<pk>[\w\-]+)/delete',
        views.delete_national_objective,
        name='delete_national_objective'),

    url(r'^dashboard/objectives/(?P<objective>[\w\-]+)/actions/add',
        views.edit_national_action,
        name='edit_national_action'),

    url(r'^dashboard/objectives/(?P<objective>[\w\-]+)/actions/(?P<parent>[\w\-]+)/add',
        views.edit_national_action,
        name='edit_national_action'),

    url(r'^dashboard/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/edit',
        views.edit_national_action,
        name='edit_national_action'),

    url(r'^dashboard/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/$',
        views.view_national_action,
        name='view_national_action'),

    url(r'^dashboard/objectives/(?P<objective>[\w\-]+)/actions/(?P<pk>[\w\-]+)/delete',
        views.delete_national_action,
        name='delete_national_action'),

    url(r'^dashboard/mapping/$',
        views.list_national_strategy,
        name='list_national_strategy'),

    url(r'^dashboard/mapping/add$',
        views.edit_national_strategy,
        name='edit_national_strategy'),

    url(r'^dashboard/mapping/(?P<pk>[\w\-]+)/add$',
        views.edit_national_strategy,
        name='edit_national_strategy'),

    url(r'^dashboard/mapping/(?P<strategy>[\w\-]+)/delete$',
        views.delete_national_strategy,
        name='delete_national_strategy'),

    url(r'^dashboard/eu-aichi-mapping/$',
        views.list_eu_aichi_strategy,
        name='list_eu_aichi_strategy'),

    url(r'^dashboard/eu-aichi-mapping/add/$',
        views.edit_eu_aichi_strategy,
        name='edit_eu_aichi_strategy'),


    url(r'^dashboard/eu-aichi-mapping/(?P<pk>\d+)/edit/$',
        views.edit_eu_aichi_strategy,
        name='edit_eu_aichi_strategy'),


    url(r'^dashboard/eu-aichi-mapping/(?P<pk>\d+)/delete/$',
        views.delete_eu_aichi_strategy,
        name='delete_eu_aichi_strategy'),

    url(r'^dashboard/pages$', views.admin_pages, name='admin_pages'),
    url(r'^dashboard/export$', views.admin_export, name='admin_export'),
    url(r'^dashboard/page/(?P<handle>[\w\-]+)/edit$',
        views.admin_page, name='admin_page')
]

# Django Rosetta support for translation
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^translate/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
