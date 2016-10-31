from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^oauth/authorize$', views.authorize, name='auth'),
    url(r'^oauth/token$', views.access_token, name='token'),
]
