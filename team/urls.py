from django.conf.urls import include, url
from team import views
from rest_framework import routers

# TODO: convert from viewsets to views for greater control
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'people/?', views.TeammateViewSet)
router.register(r'roles/?', views.RoleViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/', include(router.urls))
]
