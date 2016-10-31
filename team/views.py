from django.shortcuts import render
from rest_framework import viewsets
from team.models import Teammate, Role
from team.serializers import TeammateSerializer, RoleSerializer


# Create your views here.
def home(request):
    return render(request, "team/index.html")


class TeammateViewSet(viewsets.ModelViewSet):
    """
    API method to view teammates
    """
    queryset = Teammate.objects.all()
    serializer_class = TeammateSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    API method to view roles on the team
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
