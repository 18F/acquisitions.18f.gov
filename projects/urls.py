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
    url(r'^buys/abpa/$', views.AgileBPAList.as_view(), name='abpa-list'),
    url(r'^buys/abpa/(?P<pk>[0-9]+)$',
        views.AgileBPADetail.as_view(),
        name='abpa-detail'),
    url(r'^buys/mp/$', views.MicropurchaseList.as_view(), name='mp-list'),
    url(r'^buys/mp/(?P<pk>[0-9]+)$',
        views.MicropurchaseDetail.as_view(),
        name='mp-detail'),
    url(r'^iaas/$', views.IAAList.as_view(), name='iaa-list'),
    url(r'^iaas/(?P<pk>[0-9]+)$',
        views.IAADetail.as_view(),
        name='iaa-detail'),
]

iaa_patterns = [
    url(r'^$', views.iaas, name='iaas'),
    url(r'(?P<iaa>\w+)', views.iaa, name='iaa'),
]

project_patterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'(?P<project>\w+)', views.project, name='project'),
]

buy_patterns = [
    url(r'^$', views.buys, name='buys'),
    url(r'(?P<buy>\d+)/$', views.buy, name='buy'),
    url(r'(?P<buy>\d+)/nda/$', views.buy_nda, name='buy_nda'),
    url(r'(?P<buy>\d+)/qasp/$', views.qasp, name='qasp'),
    url(
        r'(?P<buy>\d+)/qasp/download/(?P<doc_format>\w+)?$',
        views.qasp_download,
        name='qasp_download'
    ),
    url(
        r'(?P<buy>\d+)/acquisition_plan/$',
        views.acquisition_plan,
        name='acquisition_plan'
    ),
    url(
        r'(?P<buy>\d+)/acquisition_plan/download/$',
        views.acquisition_plan_download,
        name='acquisition_plan_download'
    ),
    url(
        r'(?P<buy>\d+)/market_research/$',
        views.market_research,
        name='market_research'
    ),
    url(
        r'(?P<buy>\d+)/market_research/download/$',
        views.market_research_download,
        name='market_research_download'
    ),
]

api_patterns = format_suffix_patterns(api_patterns)
