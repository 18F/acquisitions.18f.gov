from django.conf.urls import include, url
from projects import views
from rest_framework.urlpatterns import format_suffix_patterns


api_patterns = [
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)$',
        views.ProjectDetail.as_view(),
        name='project-detail'),
    url(r'^buys/$', views.BuyList.as_view(), name='buy-list'),
    url(r'^buys/abpa/$', views.BuyList.as_view(), name='abpa-list'),
    url(r'^buys/abpa/(?P<pk>[0-9]+)$',
        views.BuyDetail.as_view(),
        name='abpa-detail'),
    url(r'^iaas/$', views.IAAList.as_view(), name='iaa-list'),
    url(r'^iaas/(?P<pk>[0-9]+)$',
        views.IAADetail.as_view(),
        name='iaa-detail'),
    url(r'^clients/$', views.ClientList.as_view(), name='client-list'),
    url(r'^clients/(?P<pk>[0-9]+)$',
        views.ClientDetail.as_view(),
        name='client-detail'),
]

iaa_patterns = [
    url(r'^$', views.iaas, name='iaas'),
    url(r'^create/$', views.edit_iaa, name='edit_iaa'),
    url(r'(?P<iaa>\w+)/$', views.iaa, name='iaa'),
    url(r'(?P<iaa>\w+)/edit/$', views.edit_iaa, name='edit_iaa'),
]

project_patterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^create/$', views.create_project, name='create_project'),
    url(r'(?P<project>\d+)/$', views.project, name='project'),
    url(r'(?P<project>\d+)/edit/$', views.edit_project, name='edit_project'),
]

buy_patterns = [
    url(r'^$', views.buys, name='buys'),
    url(r'^create/$', views.create_buy, name='create_buy'),
    url(r'(?P<buy>\d+)/$', views.buy, name='buy'),
    url(r'(?P<buy>\d+)/edit/$', views.edit_buy, name='edit_buy'),
    url(r'(?P<buy>\d+)/nda/$', views.buy_nda, name='buy_nda'),
    url(r'(?P<buy>\d+)/(?P<doc_type>\w+)/$', views.document, name='document'),
    url(
        r'(?P<buy>\d+)/(?P<doc_type>\w+)/download/(?P<doc_format>\w+)?$',
        views.download,
        name='download'
    ),
]

client_patterns = [
    url(r'^$', views.clients, name='clients'),
    url(r'^create/$', views.edit_client, name='edit_client'),
    url(r'^(?P<client>\w+)/$', views.client, name='client'),
    url(r'(?P<client>\d+)/edit/$', views.edit_client, name='edit_client'),
]

api_patterns = format_suffix_patterns(api_patterns)
