from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from projects.models import IAA, Project, Buy
from projects.serializers import IAASerializer, ProjectSerializer, BuySerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('projects:project-list', request=request, format=format),
        'buys': reverse('projects:buy-list', request=request, format=format),
        'iaas': reverse('projects:iaa-list', request=request, format=format)
    })


class IAAList(mixins.ListModelMixin,
              generics.GenericAPIView):
    """
    List all IAAs
    """
    serializer_class = IAASerializer

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return IAA.objects.all()
        else:
            return IAA.objects.exclude(signed_on=null)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class IAADetail(mixins.RetrieveModelMixin,
              generics.GenericAPIView):
    """
    Retrieve details of one IAA
    """
    serializer_class = IAASerializer

    def get_queryset(self):
        iaa = IAA.objects.get(pk=self.kwargs['pk'])
        if iaa.signed_on:
            return IAA.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.is_authenticated():
            return IAA.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProjectList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all projects
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Project.objects.all()
        else:
            return Project.objects.filter(public=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProjectDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve details of one project
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        if project.public is True:
            return Project.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_private'):
            return Project.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BuyList(mixins.ListModelMixin,
              generics.GenericAPIView):
    """
    List all buys
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        if self.request.user.has_perm('projects.view_private'):
            return Buy.objects.all()
        else:
            return Buy.objects.select_related('project').filter(public=True, project__public=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BuyDetail(mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    """
    Retrieve details of one buy
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        buy = Buy.objects.get(pk=self.kwargs['pk'])
        if buy.public is True:
            return Buy.objects.filter(pk=self.kwargs['pk'])
        elif self.request.user.has_perm('projects.view_private'):
            return Buy.objects.filter(pk=self.kwargs['pk'])
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
