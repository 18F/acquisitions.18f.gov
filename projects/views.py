from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from projects.models import IAA, Project
from projects.serializers import IAASerializer, ProjectSerializer


# Create your views here.
def home(request):
    return render(request, "projects/index.html")


# class IAAViewSet(viewsets.ModelViewSet):
#     """
#     API method to view IAAs
#     """
#     serializer_class = IAASerializer
#
#     def get_queryset(self):
#         if self.request.user.is_authenticated():
#             return IAA.objects.all()
#         else:
#             return IAA.objects.exclude(signed_on=null)


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
        if project.public:
            return project
        elif self.request.user.has_perm('projects.view_private'):
            return project
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
