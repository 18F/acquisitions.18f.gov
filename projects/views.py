from django.shortcuts import render
from rest_framework import viewsets
from projects.models import IAA, Project
from projects.serializers import IAASerializer, ProjectSerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


class IAAViewSet(viewsets.ModelViewSet):
    """
    API method to view IAAs
    """
    serializer_class = IAASerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return IAA.objects.all()
        else:
            return IAA.objects.exclude(signed_on=null)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API method to view projects
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Project.objects.all()
        else:
            return Project.objects.filter(public=True)
