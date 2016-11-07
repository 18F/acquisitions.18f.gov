from django.conf.urls import include, url
from team import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/people/$', views.TeammateList.as_view()),
    url(r'^api/people/(?P<pk>[0-9]+)', views.TeammateDetail.as_view()),
    url(r'^api/roles/$', views.RoleList.as_view()),
    url(r'^api/roles/(?P<pk>[0-9]+)', views.RoleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
