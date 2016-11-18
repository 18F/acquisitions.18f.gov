from django.conf.urls import include, url
from projects import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'^api/projects/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view()),
    url(r'^api/buys/$', views.BuyList.as_view()),
    url(r'^api/buys/(?P<pk>[0-9]+)$', views.BuyDetail.as_view()),
    url(r'^api/iaas/$', views.IAAList.as_view()),
    url(r'^api/iaas/(?P<pk>[0-9]+)$', views.IAADetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
