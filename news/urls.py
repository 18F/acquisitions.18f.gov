from django.conf.urls import include, url
from news import views
from news.feeds import LatestPosts

urlpatterns = [
    url(r'^$', views.posts, name='posts'),
    url(r'^rss/$', LatestPosts(), name='rss'),
    url(r'^(?P<slug>[a-z\-]+)$', views.post, name='post'),
]
