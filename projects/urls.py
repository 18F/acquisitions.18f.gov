from django.conf.urls import include, url
from projects import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'iaa', views.IaaViewSet)
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/', include(router.urls))
]
