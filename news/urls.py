from django.conf.urls import include, url
from news import views

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^(?P<slug>[a-z\-]+)$', views.post, name='post'),
]
