"""acquisitions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from web import views as web_views
from team import urls as team_urls
from projects import urls as projects_urls
from django.conf import settings


urlpatterns = [
    url(r'^$', web_views.index),
    url(r'^guides$', web_views.guides),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^team/', include(team_urls, namespace='team')),
    url(r'^projects/', include(projects_urls, namespace='projects')),
    url(r'^auth/', include('uaa_client.urls', namespace='uaa_client')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^', include('fake_uaa_provider.urls',
                          namespace='fake_uaa_provider'))
        ]
