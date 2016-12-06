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
from nda import views as nda_views
from team import urls as team_urls
from projects import urls as projects_urls
from news import urls as news_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_docs.views import DRFDocsView


api_patterns = projects_urls.api_patterns + team_urls.api_patterns


urlpatterns = [
    url(r'^$', web_views.index),
    url(r'^guides$', web_views.guides),
    url(r'^api/$', DRFDocsView.as_view(), name='api_docs'),
    url(r'^api/', include(api_patterns, namespace='api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^team/', include(team_urls.urlpatterns, namespace='team')),
    url(
        r'^projects/',
        include(projects_urls.project_patterns, namespace='projects')
    ),
    url(
        r'^buys/',
        include(projects_urls.buy_patterns, namespace='buys')
    ),
    url(
        r'^news/',
        include(news_urls.urlpatterns, namespace='news')
    ),
    url(r'^profile/$', web_views.profile),
    url(r'^profile/refresh_token/$', web_views.refresh_token),
    url(r'^profile/sign_nda/$', nda_views.sign_nda),
    url(r'^auth/', include('uaa_client.urls', namespace='uaa_client')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^', include('fake_uaa_provider.urls',
                          namespace='fake_uaa_provider'))
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
