from django.conf.urls import include, url
from projects import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'iaa', views.IAAViewSet, base_name='iaa')
router.register(r'projects', views.ProjectViewSet, base_name='projects')

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/', include(router.urls))
]
