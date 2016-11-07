from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from team.models import Teammate, Role
from team.serializers import TeammateSerializer, \
    TeammatePlusSerializer, RoleSerializer


# Create your views here.
def home(request):
    return render(request, "team/index.html")


class TeammateList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    List all teammates
    """
    queryset = Teammate.objects.all()

    def get_serializer_class(self):
        if self.request.user.has_perm('team.view_private'):
            return TeammatePlusSerializer
        else:
            return TeammateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TeammateDetail(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    """
    Retrieve details for one teammate
    """
    queryset = Teammate.objects.all()

    def get_serializer_class(self):
        if self.request.user.has_perm('team.view_private'):
            return TeammatePlusSerializer
        else:
            return TeammateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RoleViewSet(viewsets.ModelViewSet):
    """
    API method to view roles on the team
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
