from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^callback$', views.oauth2_callback, name='callback'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
]
