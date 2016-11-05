from django.shortcuts import render
from rest_framework import viewsets
from team.models import Teammate, Role
from team.serializers import TeammateSerializer, \
    TeammatePlusSerializer, RoleSerializer


# Create your views here.
def home(request):
    return render(request, "team/index.html")


class TeammateViewSet(viewsets.ModelViewSet):
    """
    API method to view teammates
    """
    queryset = Teammate.objects.all()

    def get_serializer_class(self):
        if self.request.user.has_perm('team.view_private'):
            return TeammatePlusSerializer
        else:
            return TeammateSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    API method to view roles on the team
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
