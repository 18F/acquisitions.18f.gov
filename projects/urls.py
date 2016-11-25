from django.conf.urls import include, url
from projects import views
from rest_framework.urlpatterns import format_suffix_patterns


api_patterns = [
    # url(r'^api/$', views.api_root),
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)$',
        views.ProjectDetail.as_view(),
        name='project-detail'),
    url(r'^buys/$', views.BuyList.as_view(), name='buy-list'),
    url(r'^buys/(?P<pk>[0-9]+)$',
        views.BuyDetail.as_view(),
        name='buy-detail'),
    url(r'^iaas/$', views.IAAList.as_view(), name='iaa-list'),
    url(r'^iaas/(?P<pk>[0-9]+)$',
        views.IAADetail.as_view(),
        name='iaa-detail'),
]

project_patterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'(?P<project>\w+)', views.project, name='project'),
]

buy_patterns = [
    url(r'^$', views.buys, name='buys'),
    url(r'(?P<buy>\d+)/$', views.buy, name='buy'),
    url(r'(?P<buy>\d+)/qasp/$', views.qasp, name='qasp'),
    url(r'(?P<buy>\d+)/qasp/download/$', views.qasp_download, name='qasp_download'),
    url(r'(?P<buy>\d+)/acquisition_plan/$', views.acquisition_plan, name='acquisition_plan'),
    url(r'(?P<buy>\d+)/acquisition_plan/download/$', views.acquisition_plan_download, name='acquisition_plan_download'),
]

api_patterns = format_suffix_patterns(api_patterns)
