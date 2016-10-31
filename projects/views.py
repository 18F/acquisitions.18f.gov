from django.shortcuts import render
from rest_framework import viewsets
from projects.models import IAA, Project
from projects.serializers import IaaSerializer, ProjectSerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


class IaaViewSet(viewsets.ModelViewSet):
    """
    API method to view IAAs
    """
    queryset = IAA.objects.all()
    serializer_class = IaaSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API method to view projects
    """
    queryset = Project.objects.filter(public=True)
    serializer_class = ProjectSerializer
