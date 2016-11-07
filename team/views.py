from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from team.models import Teammate, Role
from team.serializers import TeammateSerializer, \
    TeammatePlusSerializer, RoleSerializer


# Create your views here.
def home(request):
    return render(request, "team/index.html")


def teammate(request, teammate):
    # Since we only want to show a page if the person exists, this can't
    # quite be an API-only thing. But most of the page is built via API.
    teammate = get_object_or_404(Teammate, user__username=teammate)
    return render(request, "team/teammate.html", {"teammate": teammate})


def refresh_token(request, teammate):
    teammate = get_object_or_404(Teammate, user__username=teammate)
    if request.user == teammate.user:
        # TODO: Updating in place seems better, but couldn't get that to work.
        # Commented lines below are what I tried.
        token = Token.objects.get_or_create(user=request.user)[0]
        # token.key = token.generate_key()
        # token.save(update_fields=['key'])
        token.delete()
        Token.objects.create(user=request.user)
    return redirect("/team/"+teammate.user.username)


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


class RoleList(mixins.ListModelMixin,
               generics.GenericAPIView):
    """
    List all roles
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RoleDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    """
    Retrive details for a role
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
