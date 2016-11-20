from django.conf.urls import include, url
from team import views
from rest_framework.urlpatterns import format_suffix_patterns

api_patterns = [
    url(r'^team/$', views.TeammateList.as_view()),
    url(r'^team/(?P<pk>[0-9]+)', views.TeammateDetail.as_view()),
    url(r'^roles/$', views.RoleList.as_view()),
    url(r'^roles/(?P<pk>[0-9]+)', views.RoleDetail.as_view()),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'(?P<teammate>\w+)', views.teammate),
]

api_patterns = format_suffix_patterns(api_patterns)
