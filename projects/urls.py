from django.conf.urls import include, url
from projects import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/$', views.api_root),
    url(r'^api/projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^api/projects/(?P<pk>[0-9]+)$',
        views.ProjectDetail.as_view(),
        name='project-detail'),
    url(r'^api/buys/$', views.BuyList.as_view(), name='buy-list'),
    url(r'^api/buys/(?P<pk>[0-9]+)$',
        views.BuyDetail.as_view(),
        name='buy-detail'),
    url(r'^api/iaas/$', views.IAAList.as_view(), name='iaa-list'),
    url(r'^api/iaas/(?P<pk>[0-9]+)$',
        views.IAADetail.as_view(),
        name='iaa-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
